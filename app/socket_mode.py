"""
Socket Mode runner for Slacktable.
This enables running the app locally to receive real-time events via Socket Mode.
"""

import asyncio
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

from app.config import get_settings
from app.utils.logging import logger
from app.slack.handlers import handle_reaction_added, handle_reaction_removed, EMOJI_DESTINATION_MAP


def create_socket_mode_app() -> AsyncApp:
    """Create and configure the Socket Mode Slack app."""
    settings = get_settings()
    app = AsyncApp(
        token=settings.slack_bot_token,
        signing_secret=settings.slack_signing_secret,
    )

    @app.event("reaction_added")
    async def reaction_added_handler(event, say):
        """Handle reaction_added events."""
        reaction = event.get("reaction")
        logger.info(f"Received reaction: {reaction}")
        
        if reaction in EMOJI_DESTINATION_MAP:
            logger.info(f"Processing {reaction} reaction")
            try:
                success = handle_reaction_added(event)
                if success:
                    logger.info("Successfully processed reaction_added event")
                else:
                    logger.error("Failed to process reaction_added event")
            except Exception as e:
                logger.error(f"Error processing reaction_added: {e}")

    @app.event("reaction_removed")
    async def reaction_removed_handler(event, say):
        """Handle reaction_removed events."""
        logger.info(f"Received reaction_removed event: {event}")
        if event.get("reaction") in EMOJI_DESTINATION_MAP:
            try:
                success = handle_reaction_removed(event)
                if success:
                    logger.info("Successfully processed reaction_removed event")
                else:
                    logger.error("Failed to process reaction_removed event")
            except Exception as e:
                logger.error(f"Error processing reaction_removed: {e}")

    return app



async def run_socket_mode():
    """Run the app in Socket Mode."""
    settings = get_settings()
    if not settings.slack_app_token:
        logger.error("SLACK_APP_TOKEN is required for Socket Mode")
        return


    app = create_socket_mode_app()
    handler = AsyncSocketModeHandler(app, settings.slack_app_token)
    logger.info("Starting Slacktable in Socket Mode...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Target emoji: {settings.target_emoji}")
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(run_socket_mode())


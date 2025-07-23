"""
Slack client initialization and utilities.
Handles Slack API communication and authentication.
"""

from typing import Optional, Dict, Any
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from app.config import get_settings
from app.utils.logging import logger


class SlackClient:
    """Slack client wrapper with error handling."""
    
    def __init__(self):
        """Initialize Slack client with bot token."""
        settings = get_settings()
        self.client = WebClient(token=settings.slack_bot_token)
        self.bot_user_id = None
        self._get_bot_info()
    
    def _get_bot_info(self):
        """Get bot user information."""
        try:
            response = self.client.auth_test()
            self.bot_user_id = response["user_id"]
            logger.info("Slack client initialized successfully", {
                "bot_user_id": self.bot_user_id,
                "team_id": response.get("team_id")
            })
        except SlackApiError as e:
            logger.error("Failed to initialize Slack client", {
                "error": str(e),
                "error_code": e.response["error"]
            })
            raise
    
    def get_message_info(self, channel_id: str, message_ts: str) -> Optional[Dict[str, Any]]:
        """
        Get message information from Slack.
        
        Args:
            channel_id: The channel ID where the message is located
            message_ts: The timestamp of the message
            
        Returns:
            Message information or None if not found
        """
        try:
            response = self.client.conversations_history(
                channel=channel_id,
                inclusive=True,
                oldest=message_ts,
                limit=1
            )
            
            if response["messages"]:
                message = response["messages"][0]
                logger.debug("Retrieved message info", {
                    "channel_id": channel_id,
                    "message_ts": message_ts,
                    "user_id": message.get("user"),
                    "text_length": len(message.get("text", ""))
                })
                return message
            else:
                logger.warning("Message not found", {
                    "channel_id": channel_id,
                    "message_ts": message_ts
                })
                return None
                
        except SlackApiError as e:
            logger.error("Failed to get message info", {
                "channel_id": channel_id,
                "message_ts": message_ts,
                "error": str(e),
                "error_code": e.response["error"]
            })
            return None
    
    def get_user_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user information from Slack.
        
        Args:
            user_id: The user ID
            
        Returns:
            User information or None if not found
        """
        try:
            response = self.client.users_info(user=user_id)
            user_info = response["user"]
            logger.debug("Retrieved user info", {
                "user_id": user_id,
                "username": user_info.get("name"),
                "display_name": user_info.get("profile", {}).get("display_name")
            })
            return user_info
            
        except SlackApiError as e:
            logger.error("Failed to get user info", {
                "user_id": user_id,
                "error": str(e),
                "error_code": e.response["error"]
            })
            return None
    
    def get_channel_info(self, channel_id: str) -> Optional[Dict[str, Any]]:
        """
        Get channel information from Slack.
        
        Args:
            channel_id: The channel ID
            
        Returns:
            Channel information or None if not found
        """
        try:
            response = self.client.conversations_info(channel=channel_id)
            channel_info = response["channel"]
            logger.debug("Retrieved channel info", {
                "channel_id": channel_id,
                "channel_name": channel_info.get("name"),
                "is_private": channel_info.get("is_private", False)
            })
            return channel_info
            
        except SlackApiError as e:
            logger.error("Failed to get channel info", {
                "channel_id": channel_id,
                "error": str(e),
                "error_code": e.response["error"]
            })
            return None


# Lazy Slack client instance
_slack_client = None

def get_slack_client():
    """Get the global Slack client instance (lazy-loaded)."""
    global _slack_client
    if _slack_client is None:
        _slack_client = SlackClient()
    return _slack_client

# For backward compatibility
class SlackClientProxy:
    def __getattr__(self, name):
        return getattr(get_slack_client(), name)

slack_client = SlackClientProxy()

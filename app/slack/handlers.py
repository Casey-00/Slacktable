"""
Slack event handlers for emoji reactions.
Processes reaction events and triggers Airtable record creation.
"""

from typing import Dict, Any
from datetime import datetime

from app.config import get_settings
from app.utils.logging import logger
from app.slack.client import slack_client
from app.airtable.client import airtable_client


def handle_reaction_added(event: Dict[str, Any]) -> bool:
    """
    Handle reaction_added event from Slack.
    
    Args:
        event: The reaction event data from Slack
        
    Returns:
        True if processed successfully, False otherwise
    """
    try:
        # Extract event data
        reaction = event.get("reaction")
        user_id = event.get("user")
        item = event.get("item", {})
        channel_id = item.get("channel")
        message_ts = item.get("ts")
        thread_ts = item.get("thread_ts")  # Present if message is in a thread
        
        # Log the reaction event with full event data for debugging
        logger.info(f"🔍 FULL REACTION EVENT: {event}")
        logger.slack_event("reaction_added", user_id, channel_id, f"Reaction: {reaction}")
        
        # Check if this is the target emoji
        settings = get_settings()
        if reaction != settings.target_emoji:
            logger.debug(f"Ignoring reaction: {reaction} (not target emoji: {settings.target_emoji})")
            return True
        
        # Validate required fields
        if not all([user_id, channel_id, message_ts]):
            logger.error("Missing required fields in reaction event", {
                "user_id": user_id,
                "channel_id": channel_id,
                "message_ts": message_ts
            })
            return False
        
        # Get the original message (supporting both regular and threaded messages)
        message = slack_client.get_message_info(channel_id, message_ts, thread_ts)
        if not message:
            logger.error("Could not retrieve message", {
                "channel_id": channel_id,
                "message_ts": message_ts,
                "thread_ts": thread_ts,
                "is_threaded": thread_ts is not None
            })
            return False
        
        # Extract message text
        message_text = message.get("text", "")
        if not message_text:
            logger.warning("Message has no text content", {
                "channel_id": channel_id,
                "message_ts": message_ts
            })
            return False
        
        # Get additional context for logging
        message_user_id = message.get("user")
        user_info = slack_client.get_user_info(user_id)
        channel_info = slack_client.get_channel_info(channel_id)
        
        # Create context for logging
        context = {
            "reactor_user": user_info.get("name") if user_info else user_id,
            "message_author": message_user_id,
            "channel_name": channel_info.get("name") if channel_info else channel_id,
            "message_length": len(message_text),
            "is_threaded": thread_ts is not None,
            "thread_ts": thread_ts,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info("Processing fedex reaction", context)
        
        # Create Airtable record
        success = create_airtable_record(message_text, context)
        
        if success:
            logger.info("Successfully processed fedex reaction", context)
            return True
        else:
            logger.error("Failed to process fedex reaction", context)
            return False
            
    except Exception as e:
        logger.error("Error handling reaction event", {
            "error": str(e),
            "event": event
        })
        return False


def create_airtable_record(message_text: str, context: Dict[str, Any]) -> bool:
    """
    Create a record in Airtable with the message text.
    
    Args:
        message_text: The text content of the message
        context: Additional context for logging
        
    Returns:
        True if record created successfully, False otherwise
    """
    try:
        # Prepare record fields
        settings = get_settings()
        fields = {
            settings.airtable_field_name: message_text
        }
        
        # Create the record
        record = airtable_client.create_record(fields)
        
        if record:
            logger.info("Airtable record created successfully", {
                "record_id": record["id"],
                "message_preview": message_text[:100] + "..." if len(message_text) > 100 else message_text,
                **context
            })
            return True
        else:
            logger.error("Failed to create Airtable record", {
                "message_preview": message_text[:100] + "..." if len(message_text) > 100 else message_text,
                **context
            })
            return False
            
    except Exception as e:
        logger.error("Error creating Airtable record", {
            "error": str(e),
            "message_preview": message_text[:100] + "..." if len(message_text) > 100 else message_text,
            **context
        })
        return False


def handle_reaction_removed(event: Dict[str, Any]) -> bool:
    """
    Handle reaction_removed event from Slack.
    Currently just logs the event - no action taken.
    
    Args:
        event: The reaction event data from Slack
        
    Returns:
        True always (no processing needed)
    """
    reaction = event.get("reaction")
    user_id = event.get("user")
    channel_id = event.get("item", {}).get("channel")
    
    logger.slack_event("reaction_removed", user_id, channel_id, f"Reaction: {reaction}")
    
    # For now, we don't do anything when reactions are removed
    # This could be extended to remove records from Airtable if needed
    return True

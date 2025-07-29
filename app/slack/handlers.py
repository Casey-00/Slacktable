"""
Slack event handlers for emoji reactions.
Processes reaction events and triggers Airtable record creation.
"""

from typing import Dict, Any, List
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
        
        # Log the reaction event
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
        
        # Get the original message (supports both regular and threaded messages automatically)
        message = slack_client.get_message_info(channel_id, message_ts)
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
        success = create_airtable_record(message_text, message, context)
        
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


def extract_image_attachments(message: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Extract image attachments from Slack message.
    
    Args:
        message: The Slack message object
        
    Returns:
        List of attachment objects for Airtable
    """
    attachments = []
    files = message.get("files", [])
    
    for file in files:
        # Check if it's an image
        mimetype = file.get("mimetype", "")
        if mimetype.startswith("image/"):
            settings = get_settings()
            # Create URL with bot token for authentication
            auth_url = f"{file.get('url_private')}?token={settings.slack_bot_token}"
            attachments.append({
                "url": auth_url,
                "filename": file.get("name", "screenshot")
            })
            logger.info("Found image attachment", {
                "filename": file.get("name"),
                "mimetype": mimetype,
                "size": file.get("size")
            })
    
    return attachments


def create_airtable_record(message_text: str, message: Dict[str, Any], context: Dict[str, Any]) -> bool:
    """
    Create a record in Airtable with the message text and any image attachments.
    
    Args:
        message_text: The text content of the message
        message: The full Slack message object
        context: Additional context for logging
        
    Returns:
        True if record created successfully, False otherwise
    """
    try:
        # Prepare record fields
        settings = get_settings()
        fields = {
            settings.airtable_field_name: message_text,
            "Status": "Intake"
        }

        # Add image attachments if any are present
        image_attachments = extract_image_attachments(message)
        if image_attachments:
            fields["Screenshot"] = image_attachments
        
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

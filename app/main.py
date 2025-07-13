"""
Main FastAPI application for Slacktable.
Handles Slack events and webhooks.
"""

import hashlib
import hmac
import time
from typing import Dict, Any

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse

from app.config import settings
from app.utils.logging import logger
from app.slack.handlers import handle_reaction_added, handle_reaction_removed

# Initialize FastAPI app
app = FastAPI(
    title="Slacktable",
    description="A Slack app that sends tagged messages to Airtable",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Slacktable is running!", "status": "healthy"}


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "timestamp": time.time()}


def verify_slack_signature(request_body: bytes, timestamp: str, signature: str) -> bool:
    """
    Verify that the request came from Slack by validating the signature.
    
    Args:
        request_body: The raw request body
        timestamp: The X-Slack-Request-Timestamp header
        signature: The X-Slack-Signature header
        
    Returns:
        True if signature is valid, False otherwise
    """
    # Check if timestamp is too old (replay attack protection)
    if abs(time.time() - int(timestamp)) > 60 * 5:  # 5 minutes
        logger.warning("Request timestamp too old", {"timestamp": timestamp})
        return False
    
    # Create the signature base string
    sig_basestring = f"v0:{timestamp}:{request_body.decode('utf-8')}"
    
    # Create the expected signature
    expected_signature = 'v0=' + hmac.new(
        settings.slack_signing_secret.encode('utf-8'),
        sig_basestring.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Compare signatures
    return hmac.compare_digest(expected_signature, signature)


@app.post("/slack/events")
async def slack_events(request: Request):
    """
    Handle Slack Events API requests.
    
    This endpoint receives events from Slack when users react to messages.
    """
    # Get request body and headers
    body = await request.body()
    headers = request.headers
    
    # Verify the request came from Slack
    timestamp = headers.get("X-Slack-Request-Timestamp")
    signature = headers.get("X-Slack-Signature")
    
    if not timestamp or not signature:
        logger.error("Missing Slack signature headers")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing signature headers"
        )
    
    if not verify_slack_signature(body, timestamp, signature):
        logger.error("Invalid Slack signature")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid signature"
        )
    
    # Parse the JSON body
    try:
        event_data = await request.json()
    except Exception as e:
        logger.error("Failed to parse JSON body", {"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON"
        )
    
    # Handle URL verification challenge
    if event_data.get("type") == "url_verification":
        challenge = event_data.get("challenge")
        logger.info("URL verification challenge received", {"challenge": challenge})
        return {"challenge": challenge}
    
    # Handle actual events
    if event_data.get("type") == "event_callback":
        event = event_data.get("event", {})
        event_type = event.get("type")
        
        logger.info(f"Received Slack event: {event_type}")
        
        try:
            if event_type == "reaction_added":
                success = handle_reaction_added(event)
            elif event_type == "reaction_removed":
                success = handle_reaction_removed(event)
            else:
                logger.info(f"Unhandled event type: {event_type}")
                success = True  # Don't fail for unknown events
            
            if success:
                return {"status": "ok"}
            else:
                logger.error(f"Failed to process event: {event_type}")
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"error": "Failed to process event"}
                )
                
        except Exception as e:
            logger.error(f"Error processing event: {event_type}", {"error": str(e)})
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Internal server error"}
            )
    
    # Return OK for any other event types
    return {"status": "ok"}


@app.post("/slack/interactive")
async def slack_interactive(request: Request):
    """
    Handle Slack interactive components (buttons, modals, etc.).
    Currently not used but included for future extensibility.
    """
    logger.info("Interactive component received")
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting Slacktable server", {
        "environment": settings.environment,
        "log_level": settings.log_level
    })
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development"
    )

"""
Logging configuration for Slacktable app.
Provides structured logging with context.
"""

import logging
import sys
from typing import Optional, Dict, Any
from datetime import datetime

from app.config import settings


class StructuredLogger:
    """Structured logger with context support."""
    
    def __init__(self, name: str = "slacktable"):
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Configure the logger with appropriate handlers and formatting."""
        # Set log level from settings
        log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(handler)
        
        # Prevent duplicate logs
        self.logger.propagate = False
    
    def _log_with_context(self, level: str, message: str, context: Optional[Dict[str, Any]] = None):
        """Log message with optional context."""
        if context:
            context_str = " | ".join([f"{k}={v}" for k, v in context.items()])
            full_message = f"{message} | {context_str}"
        else:
            full_message = message
        
        log_method = getattr(self.logger, level.lower())
        log_method(full_message)
    
    def info(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log info message."""
        self._log_with_context("INFO", message, context)
    
    def error(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log error message."""
        self._log_with_context("ERROR", message, context)
    
    def warning(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log warning message."""
        self._log_with_context("WARNING", message, context)
    
    def debug(self, message: str, context: Optional[Dict[str, Any]] = None):
        """Log debug message."""
        self._log_with_context("DEBUG", message, context)
    
    def slack_event(self, event_type: str, user_id: str, channel_id: str, message: str = ""):
        """Log Slack event with structured context."""
        context = {
            "event_type": event_type,
            "user_id": user_id,
            "channel_id": channel_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.info(f"Slack event: {event_type} | {message}", context)
    
    def airtable_operation(self, operation: str, success: bool, record_id: str = "", error: str = ""):
        """Log Airtable operation with structured context."""
        context = {
            "operation": operation,
            "success": success,
            "record_id": record_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if success:
            self.info(f"Airtable operation successful: {operation}", context)
        else:
            context["error"] = error
            self.error(f"Airtable operation failed: {operation}", context)


# Global logger instance
logger = StructuredLogger()

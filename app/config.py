"""
Configuration management for Slacktable app.
Handles environment variables and app settings.
"""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings
# Note: In production, environment variables are set directly by the platform
# No .env file is used to avoid conflicts with placeholder values


class Settings(BaseSettings):
    """Application settings with validation."""
    
    # Slack Configuration
    slack_bot_token: str
    slack_signing_secret: Optional[str] = None
    slack_app_token: str
    
    # Airtable Configuration
    airtable_api_token: str
    airtable_base_id: str
    airtable_table_name: str
    airtable_field_name: str
    
    # App Configuration
    environment: str = "development"
    log_level: str = "INFO"
    
    # Emoji configuration
    target_emoji: str = "fedex"
    
    model_config = {"case_sensitive": True}


_settings = None

def get_settings() -> Settings:
    """Get application settings instance (singleton)."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


# Lazy-loaded settings instance
def get_settings_lazy():
    return get_settings()

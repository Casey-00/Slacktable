"""
Configuration management for Slacktable app.
Handles environment variables and app settings.
"""

import os
from typing import Optional
from pydantic import BaseSettings, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings with validation."""
    
    # Slack Configuration
    slack_bot_token: str = Field(..., env="SLACK_BOT_TOKEN")
    slack_signing_secret: str = Field(..., env="SLACK_SIGNING_SECRET")
    slack_app_token: str = Field(..., env="SLACK_APP_TOKEN")
    
    # Airtable Configuration
    airtable_api_token: str = Field(..., env="AIRTABLE_API_TOKEN")
    airtable_base_id: str = Field(..., env="AIRTABLE_BASE_ID")
    airtable_table_name: str = Field(..., env="AIRTABLE_TABLE_NAME")
    airtable_field_name: str = Field(..., env="AIRTABLE_FIELD_NAME")
    
    # App Configuration
    environment: str = Field(default="development", env="ENVIRONMENT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Emoji configuration
    target_emoji: str = Field(default="fedex", env="TARGET_EMOJI")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()

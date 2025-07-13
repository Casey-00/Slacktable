"""
Tests for Slack event handlers.
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from app.slack.handlers import handle_reaction_added, handle_reaction_removed, create_airtable_record


class TestHandleReactionAdded:
    """Test cases for handle_reaction_added function."""
    
    def test_ignores_non_fedex_reactions(self):
        """Test that non-fedex reactions are ignored."""
        event = {
            "reaction": "thumbsup",
            "user": "U12345",
            "item": {
                "channel": "C12345",
                "ts": "1234567890.123"
            }
        }
        
        result = handle_reaction_added(event)
        assert result is True
    
    def test_handles_missing_fields(self):
        """Test that missing required fields are handled gracefully."""
        event = {
            "reaction": "fedex",
            "user": "U12345",
            # Missing item field
        }
        
        result = handle_reaction_added(event)
        assert result is False
    
    @patch('app.slack.handlers.slack_client')
    @patch('app.slack.handlers.create_airtable_record')
    def test_successful_fedex_reaction(self, mock_create_record, mock_slack_client):
        """Test successful processing of fedex reaction."""
        # Mock Slack client responses
        mock_slack_client.get_message_info.return_value = {
            "text": "This is a test message",
            "user": "U67890"
        }
        mock_slack_client.get_user_info.return_value = {"name": "testuser"}
        mock_slack_client.get_channel_info.return_value = {"name": "general"}
        
        # Mock Airtable record creation
        mock_create_record.return_value = True
        
        event = {
            "reaction": "fedex",
            "user": "U12345",
            "item": {
                "channel": "C12345",
                "ts": "1234567890.123"
            }
        }
        
        result = handle_reaction_added(event)
        assert result is True
        
        # Verify Slack client was called
        mock_slack_client.get_message_info.assert_called_once_with("C12345", "1234567890.123")
        
        # Verify Airtable record creation was called
        mock_create_record.assert_called_once()


class TestHandleReactionRemoved:
    """Test cases for handle_reaction_removed function."""
    
    def test_logs_reaction_removal(self):
        """Test that reaction removal is logged."""
        event = {
            "reaction": "fedex",
            "user": "U12345",
            "item": {
                "channel": "C12345",
                "ts": "1234567890.123"
            }
        }
        
        result = handle_reaction_removed(event)
        assert result is True


class TestCreateAirtableRecord:
    """Test cases for create_airtable_record function."""
    
    @patch('app.slack.handlers.airtable_client')
    def test_successful_record_creation(self, mock_airtable_client):
        """Test successful Airtable record creation."""
        mock_airtable_client.create_record.return_value = {"id": "rec123"}
        
        context = {"test": "context"}
        result = create_airtable_record("Test message", context)
        
        assert result is True
        mock_airtable_client.create_record.assert_called_once_with({"Name": "Test message"})
    
    @patch('app.slack.handlers.airtable_client')
    def test_failed_record_creation(self, mock_airtable_client):
        """Test failed Airtable record creation."""
        mock_airtable_client.create_record.return_value = None
        
        context = {"test": "context"}
        result = create_airtable_record("Test message", context)
        
        assert result is False
    
    @patch('app.slack.handlers.airtable_client')
    def test_exception_handling(self, mock_airtable_client):
        """Test exception handling in record creation."""
        mock_airtable_client.create_record.side_effect = Exception("API Error")
        
        context = {"test": "context"}
        result = create_airtable_record("Test message", context)
        
        assert result is False


if __name__ == "__main__":
    pytest.main([__file__])

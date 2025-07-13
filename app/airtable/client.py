"""
Airtable client and operations.
Handles interaction with Airtable API to create records.
"""

from typing import Optional, Dict, Any
from pyairtable import Table

from app.config import settings
from app.utils.logging import logger


class AirtableClient:
    """Airtable client to handle record creation/management."""
    
    def __init__(self):
        """Initialize Airtable client with API token and configuration from settings."""
        self.table = Table(settings.airtable_api_token, settings.airtable_base_id, settings.airtable_table_name)
    
    def create_record(self, fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create a new record in the Airtable with specified fields.
        
        Args:
            fields: A dictionary representing the fields of the record to create.
            
        Returns:
            The created record or None if an error occurred.
        """
        try:
            record = self.table.create(fields)
            logger.airtable_operation("create_record", success=True, record_id=record["id"])
            return record
            
        except Exception as e:
            logger.airtable_operation("create_record", success=False, error=str(e))
            return None


# Global Airtable client instance
airtable_client = AirtableClient()

"""
Airtable client and operations.
Handles interaction with Airtable API to create records.
"""

import io
import requests
from typing import Optional, Dict, Any, List
from pyairtable import Table

from app.config import get_settings
from app.utils.logging import logger


class AirtableClient:
    """Airtable client to handle record creation/management."""
    
    def __init__(self):
        """Initialize Airtable client with API token and configuration from settings."""
        settings = get_settings()
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
    
    def prepare_attachments(self, image_attachments: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """
        Prepare image attachments for Airtable by converting to URL format.
        
        Args:
            image_attachments: List of dictionaries containing 'filename' and 'url'
            
        Returns:
            List of Airtable attachment objects with 'url' and 'filename'
        """
        prepared_attachments = []
        
        for attachment in image_attachments:
            try:
                prepared_attachments.append({
                    'url': attachment['url'],
                    'filename': attachment['filename']
                })
                logger.info(f"Prepared attachment {attachment['filename']} for Airtable")
                
            except Exception as e:
                logger.error(f"Failed to prepare {attachment.get('filename', 'unknown')}: {e}")
                continue
                
        return prepared_attachments
    
    def create_record_with_attachments(self, fields: Dict[str, Any], image_attachments: List[Dict[str, Any]], attachment_field: str = "Screenshot") -> Optional[Dict[str, Any]]:
        """
        Create a record with image attachments.
        
        Args:
            fields: Base fields for the record
            image_attachments: List of image data to upload  
            attachment_field: Name of the attachment field in Airtable
            
        Returns:
            The created record or None if failed
        """
        try:
            # First prepare the attachments
            if image_attachments:
                prepared_attachments = self.prepare_attachments(image_attachments)
                if prepared_attachments:
                    fields[attachment_field] = prepared_attachments
                    logger.info(f"Added {len(prepared_attachments)} attachments to {attachment_field} field")
            
            # Then create the record with all fields including attachments
            return self.create_record(fields)
            
        except Exception as e:
            logger.error(f"Failed to create record with attachments: {e}")
            return None


# Lazy Airtable client instance
_airtable_client = None

def get_airtable_client():
    """Get the global Airtable client instance (lazy-loaded)."""
    global _airtable_client
    if _airtable_client is None:
        _airtable_client = AirtableClient()
    return _airtable_client

# For backward compatibility
class AirtableClientProxy:
    def __getattr__(self, name):
        return getattr(get_airtable_client(), name)

airtable_client = AirtableClientProxy()

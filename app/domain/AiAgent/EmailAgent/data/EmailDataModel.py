from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum

class EmailType(str, Enum):
    CONTACT_CREATED = "contact_created"
    CONTACT_UPDATED = "contact_updated"
    CONTACT_DELETED = "contact_deleted"
    DEAL_CREATED = "deal_created"
    DEAL_UPDATED = "deal_updated"
    DEAL_DELETED = "deal_deleted"
    OPERATION_SUCCESS = "operation_success"
    OPERATION_FAILED = "operation_failed"

class EmailTemplate(BaseModel):
    subject: str
    body: str
    html_body: Optional[str] = None

class EmailNotification(BaseModel):
    to_email: str
    email_type: EmailType
    operation_data: Dict[str, Any]
    template_data: Optional[Dict[str, Any]] = None

class EmailResponse(BaseModel):
    success: bool
    message_id: Optional[str] = None
    error: Optional[str] = None
    sent_to: Optional[str] = None 
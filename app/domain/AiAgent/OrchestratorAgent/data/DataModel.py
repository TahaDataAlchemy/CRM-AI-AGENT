from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum

class ActionType(str, Enum):
    CREATE_CONTACT = "create_contact"
    UPDATE_CONTACT = "update_contact"
    GET_CONTACT = "get_contact"
    GET_ALL_CONTACTS = "get_all_contacts"
    DELETE_CONTACT = "delete_contact"
    SEND_EMAIL = "send_email"

class TaskRequest(BaseModel):
    action: ActionType
    payload: Optional[Dict[str, Any]] = None
    contact_id: Optional[str] = None
    search_criteria: Optional[Dict[str, Any]] = None

class DecomposedQuery(BaseModel):
    tasks: List[TaskRequest]
    requires_sequential_execution: bool = False
    dependencies: Optional[Dict[str, List[str]]] = None

class AgentResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    message: Optional[str] = None
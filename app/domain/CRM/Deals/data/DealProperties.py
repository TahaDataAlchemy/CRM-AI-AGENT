from pydantic import BaseModel
from typing import Optional, Dict, Any

class DealProperties(BaseModel):
    dealname: str
    amount: Optional[int] = None
    closedate: Optional[str] = None  
    pipeline: Optional[str] = None
    dealstage: Optional[str] = None

class AssociationToContact(BaseModel):
    contact_id: str
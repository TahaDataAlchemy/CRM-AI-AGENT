from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.domain.CRM.contacts.data.ContactDataModel import ContactProperties
from app.domain.CRM.contacts.usecase import contacts_Operations

router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)

@router.get("/all", summary="Get all contacts")
async def all_contacts():
    result = contacts_Operations.get_contacts()
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result


@router.get("/{contact_id}", summary="Get contact by ID")
async def get_contact(contact_id: str):
    result = contacts_Operations.get_contact_by_id(contact_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result


@router.post("/", summary="Create a new contact")
async def create_contact(contact: ContactProperties) -> Dict[str, Any]:
    result = contacts_Operations.create_contact(contact)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result


@router.patch("/{contact_id}", summary="Update contact by ID")
async def update_contact(contact_id: str, contact: ContactProperties):
    result = contacts_Operations.update_contact(contact_id, contact)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result


@router.delete("/{contact_id}", summary="Delete contact by ID")
async def delete_contact(contact_id: str):
    result = contacts_Operations.delete_contact(contact_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result

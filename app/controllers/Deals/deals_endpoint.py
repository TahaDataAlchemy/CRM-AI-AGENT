from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.domain.CRM.Deals.data.DealProperties import DealProperties
from app.domain.CRM.Deals.usecase import deals_operations

router = APIRouter(
    prefix="/deals",
    tags=["Deals"]
)


@router.get("/", summary="Get all deals")
async def get_all_deals():
    result = deals_operations.alldeals()
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result


@router.post("/", summary="Create a new deal")
async def create_deal(deal: DealProperties):
    result = deals_operations.createdeals(deal)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result


@router.get("/{deal_id}", summary="Get deal by ID")
async def get_deal(deal_id: str):
    result = deals_operations.get_deal(deal_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result


@router.put("/{deal_id}", summary="Update deal by ID")
async def update_deal(deal_id: str, deal_data: DealProperties):
    result = deals_operations.update_deal(deal_id, deal_data)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result


@router.delete("/{deal_id}", summary="Delete deal by ID")
async def delete_deal(deal_id: str):
    result = deals_operations.delete_deal(deal_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result

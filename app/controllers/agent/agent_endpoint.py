from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from app.domain.AiAgent.OrchestratorAgent.usecase.OrchestrationAgent import process_query
from app.shared.utils.common_functions import CommonFuntions

router = APIRouter(prefix="/agent", tags=["AI Agent"])

class AgentQueryRequest(BaseModel):
    query: str
    user_email: Optional[str] = None

@router.post("/process", summary="Process user query using AI Agent")
def agent_process(request: AgentQueryRequest) -> Dict:
    try:
        CommonFuntions.write_log(f"Received agent process request: {request.query}")
        CommonFuntions.write_log(f"User email: {request.user_email}")
        
        result = process_query(query=request.query, user_email=request.user_email)
        
        CommonFuntions.write_log(f"Agent process completed successfully")
        return result
        
    except Exception as e:
        CommonFuntions.write_error_log(f"Agent process error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
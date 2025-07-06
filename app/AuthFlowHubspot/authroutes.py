from app.infra.config import settings
from app.infra.constant import TOKEN_FILE,SCOPES
#Built In Imports
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from urllib.parse import urlencode
import json, time, requests
from app.shared.utils.common_functions import CommonFuntions

router = APIRouter(
    prefix="/auth",
    tags=["Post"]
)

cf = CommonFuntions()
@router.get("/authorize_user")
def authorize_user():
    cf.write_log("Authorizing User")
    params = {
        "client_id": settings.HUBSPOT_CLIENT_ID,
        "redirect_uri": settings.HUBSPOT_REDIRECT_URI,
        "scope":SCOPES,
        "response_type": "code"
    }
    url = f"https://app.hubspot.com/oauth/authorize?{urlencode(params)}"
    return RedirectResponse(url)

@router.get("/callback")
def hubspot_callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Missing code in callback"}

    token_url = "https://api.hubapi.com/oauth/v1/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": settings.HUBSPOT_CLIENT_ID,
        "client_secret": settings.HUBSPOT_CLIENT_SECRET,
        "redirect_uri": settings.HUBSPOT_REDIRECT_URI,
        "code": code
    }

    res = requests.post(token_url, headers=headers, data=data)
    if res.status_code != 200:
        cf.write_log("User Cannot be Authorized")
        return {"error": res.json()}
    
    token_data = res.json()
    
    # Add expiration timestamp
    token_data["expires_at"] = time.time() + token_data["expires_in"]
    
    cf.jsonDump(TOKEN_FILE,token_data)
    cf.write_log("User Authorized")
    return {"message": "Authorized and token saved!", "access_token": token_data["access_token"]}

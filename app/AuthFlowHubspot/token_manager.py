import os, json, time, requests
from app.infra.config import settings
from app.infra.constant import TOKEN_FILE
from app.shared.utils.common_functions import CommonFuntions

def refresh_access_token():
    cf = CommonFuntions()
    """Refresh the access token using the refresh token"""
    if not os.path.exists(TOKEN_FILE):
        return None
    
    token_data = cf.jsonload(TOKEN_FILE)
    
    refresh_token = token_data.get("refresh_token")
    if not refresh_token:
        return None
    
    token_url = "https://api.hubapi.com/oauth/v1/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "refresh_token",
        "client_id": settings.HUBSPOT_CLIENT_ID,
        "client_secret": settings.HUBSPOT_CLIENT_SECRET,
        "refresh_token": refresh_token
    }
    
    res = requests.post(token_url, headers=headers, data=data)
    if res.status_code != 200:
        print(f"Token refresh failed: {res.text}")
        return None
    
    new_token_data = res.json()
    
    # Update expiration timestamp
    new_token_data["expires_at"] = time.time() + new_token_data["expires_in"]
    
    # Keep the refresh token if not provided in response
    if "refresh_token" not in new_token_data:
        new_token_data["refresh_token"] = refresh_token
    
    # Save updated token data
    cf.jsonDumpRefreshToken(TOKEN_FILE,new_token_data)
    
    cf.write_log("Token refreshed Succesfully")
    print("Token refreshed successfully!")
    return new_token_data


def get_valid_access_token():
    cf = CommonFuntions()
    cf.write_log("Checking For Valid Token")
    if not os.path.exists(TOKEN_FILE):
        return None
    token_data = cf.jsonload(TOKEN_FILE)

    if time.time() >= (token_data.get("expires_at", 0) - 300):  # 5-minute buffer
        token_data = refresh_access_token()

    return token_data.get("access_token") if token_data else None
from app.domain.CRM.contacts.data.ContactDataModel import ContactProperties
import requests
from typing import Dict,Any
from app.AuthFlowHubspot.token_manager import get_valid_access_token,refresh_access_token


def get_contacts():
    access_token = get_valid_access_token()
    if not access_token:
        return {"error": "No valid token available. Please authorize first at /"}

    url = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "properties": "email,firstname,lastname,phone,company"
    }

    res = requests.get(url, headers=headers, params=params)
    
    # If token is invalid, try refreshing once more
    if res.status_code == 401:
        print("🔄 Got 401, attempting token refresh...")
        access_token = refresh_access_token()
        if access_token:
            headers["Authorization"] = f"Bearer {access_token['access_token']}"
            res = requests.get(url, headers=headers, params=params)
    
    if res.status_code == 200:
        return res.json()
    else:
        return {"error": res.status_code, "details": res.text}

def create_contact(contact:ContactProperties) ->Dict[str,Any]:
    access_token = get_valid_access_token()
    if not access_token:
        return {"error":"No valid access token"}
    
    url  = "https://api.hubapi.com/crm/v3/objects/contacts"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    data = {"properties":contact.dict(exclude_unset=True)}
    res = requests.post(url,json=data,headers=headers)
    if res.status_code == 201:
        return {"message":"contact_created","data":res.json()}
    return {"error":res.status_code,"details":res.text}

def get_contact_by_id(contact_id:str):
    access_token = get_valid_access_token()
    if not access_token:
        return {"error":"No Valid token. Please authenticate at root"}
    
    url = f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(url, headers=headers)

    if res.status_code ==200:
        return res.json()
    return{"error":res.status_code,"details":res.text}

def update_contact(contact_id:str,contact:ContactProperties):
    access_token = get_valid_access_token()
    if not access_token:
        return {"error":"No Valid token. Please authenticate at root"}
    
    url = f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}"
    headers = {"Authorization":f"Bearer {access_token}","Content-Type": "application/json"}
    data = {"properties": contact.dict(exclude_unset=True)}
    res = requests.patch(url, headers=headers, json=data)
    
    if res.status_code == 200:
        return {"message": "Contact updated", "data": res.json()}
    return {"error": res.status_code, "details": res.text}

def delete_contact(contact_id:str):
    access_token = get_valid_access_token()
    if not access_token:
        return {"error":"No Valid token. Please authenticate at root"}
    url  = f"https://api.hubapi.com/crm/v3/objects/contacts/{contact_id}"
    headers = {"Authorization":f"Bearer {access_token}","Content-Type":"application/json"}
    res = requests.delete(url,headers=headers) 
    if res.status_code == 204:
        return {"message":"contact deleted"}
    return {"error": res.status_code, "details": res.text}

from app.domain.CRM.Deals.data.DealProperties import DealProperties
import requests
from typing import Dict,Any
from app.AuthFlowHubspot.token_manager import get_valid_access_token,refresh_access_token

def alldeals():
    token = get_valid_access_token()
    if not token:
        return {"error": "No token"}
    
    url = f"https://api.hubapi.com/crm/v3/objects/deals"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": 10, "properties": "dealname,amount,closedata,pipeline,dealstage"}
    
    res = requests.get(url, headers=headers, params=params)
    if res.status_code == 200:
        return res.json()
    else:
        return {"error": res.status_code, "details": res.text}


def createdeals(deal:DealProperties):
    token = get_valid_access_token()
    if not token:
        return {"error":"No token"}
    
    url = f"https://api.hubapi.com/crm/v3/objects/deals"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"properties": deal.dict(exclude_unset=True)}

    res = requests.post(url, headers=headers, json=data)
    if res.status_code==201:
        return {"message": "deal_created", "data": res.json()}
    else:
        return {"error":res.status_code,"details":res.text}

def get_deal(deal_id:str):
    token = get_valid_access_token()
    if not token:
        return {"error":"No token"}
    
    url = f"https://api.hubapi.com/crm/v3/objects/deals/{deal_id}"
    headers = {"Authorization": f"Bearer {token}"}
    res  = requests.get(url,headers=headers)
    if res.status_code==200:
        return {"message":"deal_Fetched","data":res.json()}
    else:
        return {"error":res.status_code,"details":res.text}
    
def update_deal(deal_id:str,deal_data:DealProperties):
    token = get_valid_access_token()
    if not token:
        return {"error":"No token"}
    url = f"https://api.hubapi.com/crm/v3/objects/deals/{deal_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"properties": deal_data.dict(exclude_unset=True)}
    res = requests.patch(url,headers=headers,json=data)
    if res.status_code==200:
        return {"messages":"deal updated","data":res.json()}
    else:
        return {"error":res.status_code,"details":res.text}

def delete_deal(deal_id:str):
    access_token = get_valid_access_token()
    if not access_token:
        return {"error":"No Valid token. Please authenticate at root"}
    url  = f"https://api.hubapi.com/crm/v3/objects/deals/{deal_id}"
    headers = {"Authorization":f"Bearer {access_token}","Content-Type":"application/json"}
    res = requests.delete(url,headers=headers) 
    if res.status_code == 204:
        return {"message":"deal deleted"}
    return {"error": res.status_code, "details": res.text}


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.AuthFlowHubspot.authroutes import router as auth_router
from app.controllers.contacts.contact_endpoints import router as contacts_routes
from app.controllers.Deals.deals_endpoint import router as deal_routes
from app.controllers.agent.agent_endpoint import router as agent_routes
from app.controllers.agent.email_endpoint import router as email_routes
from app.shared.utils.common_functions import CommonFuntions 



app = FastAPI()

origins = ["*"] 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(contacts_routes)
app.include_router(deal_routes)
app.include_router(agent_routes)
app.include_router(email_routes)  

@app.get("/")
def read_root():
    CommonFuntions.write_log("Root endpoint accessed")
    return {"message": "MultiAI AGENT FOR HANDLING CRM"}

@app.on_event("startup")
async def startup_event():
    CommonFuntions.write_log("CRM AI Agent Server starting up")
    CommonFuntions.write_log("All routers included successfully")
    CommonFuntions.write_log("CORS middleware configured")

@app.on_event("shutdown")
async def shutdown_event():
    CommonFuntions.write_log("CRM AI Agent Server shutting down")

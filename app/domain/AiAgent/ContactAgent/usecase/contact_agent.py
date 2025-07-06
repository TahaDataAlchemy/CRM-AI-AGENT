import json
import requests
from typing import Dict, Any, Optional
from app.domain.AiAgent.OrchestratorAgent.data.DataModel import AgentResponse,TaskRequest
from app.domain.AiAgent.OrchestratorAgent.prompts.contact_search_prompt import CONTACT_SEARCH_PROMPT
from app.infra.config import settings
from app.GROQ_CLIENT.groq_api import get_groq_chat_completion
from app.domain.AiAgent.EmailAgent.usecase.email_agent import email_agent
from app.shared.utils.common_functions import CommonFuntions


def execute_task(task:TaskRequest) -> AgentResponse:
    try:
        CommonFuntions.write_log(f"Executing task: {task.action.value}")
        
        if task.action.value == "create_contact":
            CommonFuntions.write_log("Creating new contact")
            return create_contact(task.payload)
        elif task.action.value == "update_contact":
            CommonFuntions.write_log(f"Updating contact: {task.contact_id}")
            return update_contact(task.contact_id, task.payload)
        elif task.action.value == "get_contact":
            CommonFuntions.write_log("Getting contact")
            return get_contact(task)
        elif task.action.value == "get_all_contacts":
            CommonFuntions.write_log("Getting all contacts")
            return get_all_contacts()
        elif task.action.value == "delete_contact":
            CommonFuntions.write_log("Processing delete contact request")
            # If contact_id is not provided, search for the contact first
            if not task.contact_id and task.search_criteria:
                CommonFuntions.write_log("Searching for contact to delete")
                search_result = search_contact(task.search_criteria)
                if search_result.success and search_result.data:
                    # Extract contact ID from search result
                    if isinstance(search_result.data, dict) and "contacts" in search_result.data:
                        # Multiple contacts found
                        contact_ids = [contact.get("id") for contact in search_result.data["contacts"]]
                        if contact_ids:
                            CommonFuntions.write_log(f"Found multiple contacts, deleting first: {contact_ids[0]}")
                            # Delete the first contact found
                            return delete_contact(contact_ids[0])
                    else:
                        # Single contact found
                        contact_id = search_result.data.get("id")
                        if contact_id:
                            CommonFuntions.write_log(f"Found single contact to delete: {contact_id}")
                            return delete_contact(contact_id)
                else:
                    CommonFuntions.write_error_log("Contact not found for deletion")
                    return AgentResponse(success=False, error="Contact not found for deletion")
            else:
                CommonFuntions.write_log(f"Deleting contact with ID: {task.contact_id}")
                return delete_contact(task.contact_id)
        else:
            CommonFuntions.write_error_log(f"Unknown action: {task.action.value}")
            return AgentResponse(success=False, error="Unknown action")
                
    except Exception as e:
        CommonFuntions.write_error_log(f"Error executing task: {str(e)}")
        return AgentResponse(success=False, error=str(e))

def create_contact(payload: Dict[str, Any]) -> AgentResponse:
        """
        Create a new contact
        """
        try:
            CommonFuntions.write_log("Starting contact creation")
            CommonFuntions.write_log(f"Payload: {payload}")
            
            # Clean payload - remove None values
            clean_payload = {k: v for k, v in payload.items() if v is not None}
            CommonFuntions.write_log(f"Cleaned payload: {clean_payload}")
            
            CommonFuntions.write_log(f"Making API request to: {settings.API_BASE_URL}/contacts/")
            response = requests.post(
                f"{settings.API_BASE_URL}/contacts/",
                json=clean_payload,
            )
            
            CommonFuntions.write_log(f"API response status: {response.status_code}")
            
            if response.status_code == 200:
                contact_data = response.json()
                CommonFuntions.write_log(f"Contact created successfully: {contact_data.get('id', 'N/A')}")
                
                # Send email notification
                try:
                    CommonFuntions.write_log("Sending email notification for contact creation")
                    email_response = email_agent.notify_contact_created(
                        contact_data, 
                        settings.EMAIL_USERNAME  # Send to admin email
                    )
                    CommonFuntions.write_log(f"Email notification sent: {email_response.success}")
                except Exception as email_error:
                    CommonFuntions.write_error_log(f"Failed to send email notification: {email_error}")
                
                return AgentResponse(
                    success=True,
                    data=contact_data,
                    message="Contact created successfully"
                )
            else:
                CommonFuntions.write_error_log(f"Failed to create contact: {response.text}")
                # Send failure notification
                try:
                    email_agent.notify_operation_failed(
                        "Create Contact",
                        f"Failed to create contact: {response.text}",
                        settings.EMAIL_USERNAME
                    )
                except Exception as email_error:
                    CommonFuntions.write_error_log(f"Failed to send failure email: {email_error}")
                
                return AgentResponse(
                    success=False,
                    error=f"Failed to create contact: {response.text}"
                )
                
        except Exception as e:
            CommonFuntions.write_error_log(f"Exception in create_contact: {str(e)}")
            # Send failure notification
            try:
                email_agent.notify_operation_failed(
                    "Create Contact",
                    str(e),
                    settings.EMAIL_USERNAME
                )
            except Exception as email_error:
                CommonFuntions.write_error_log(f"Failed to send failure email: {email_error}")
            
            return AgentResponse(success=False, error=str(e))
    
def update_contact(contact_id: str, payload: Dict[str, Any]) -> AgentResponse:
        """
        Update an existing contact
        """
        try:
            clean_payload = {k: v for k, v in payload.items() if v is not None}
            
            response = requests.patch(
                f"{settings.API_BASE_URL}/contacts/{contact_id}",
                json=clean_payload,
            )
            
            if response.status_code == 200:
                contact_data = response.json()
                
                # Send email notification
                try:
                    email_response = email_agent.notify_contact_updated(
                        contact_data, 
                        settings.EMAIL_USERNAME
                    )
                    print(f"Email notification sent: {email_response.success}")
                except Exception as email_error:
                    print(f"Failed to send email notification: {email_error}")
                
                return AgentResponse(
                    success=True,
                    data=contact_data,
                    message="Contact updated successfully"
                )
            else:
                # Send failure notification
                try:
                    email_agent.notify_operation_failed(
                        "Update Contact",
                        f"Failed to update contact: {response.text}",
                        settings.EMAIL_USERNAME
                    )
                except Exception as email_error:
                    print(f"Failed to send failure email: {email_error}")
                
                return AgentResponse(
                    success=False,
                    error=f"Failed to update contact: {response.text}"
                )
                
        except Exception as e:
            # Send failure notification
            try:
                email_agent.notify_operation_failed(
                    "Update Contact",
                    str(e),
                    settings.EMAIL_USERNAME
                )
            except Exception as email_error:
                print(f"Failed to send failure email: {email_error}")
            
            return AgentResponse(success=False, error=str(e))
    
def get_contact(task: TaskRequest) -> AgentResponse:
    """
    Get a specific contact, with intelligent search if needed
    """
    try:
        # If contact_id is provided, use it directly
        if task.contact_id:
            return get_contact_by_id(task.contact_id)
        
        # If search criteria is provided, search by name/email
        if task.search_criteria:
            return search_contact(task.search_criteria)
        
        return AgentResponse(success=False, error="No contact ID or search criteria provided")
        
    except Exception as e:
        return AgentResponse(success=False, error=str(e))

def get_contact_by_id(contact_id: str) -> AgentResponse:
    """
    Get contact by ID
    """
    try:
        response = requests.get(
            f"{settings.API_BASE_URL}/contacts/{contact_id}",
        )
        
        if response.status_code == 200:
            return AgentResponse(
                success=True,
                data=response.json(),
                message="Contact retrieved successfully"
            )
        else:
            return AgentResponse(
                success=False,
                error=f"Failed to get contact: {response.text}"
            )
            
    except Exception as e:
        return AgentResponse(success=False, error=str(e))

def get_all_contacts() -> AgentResponse:
    """
    Get all contacts
    """
    try:
        response = requests.get(
            f"{settings.API_BASE_URL}/contacts/all",
        )
        
        if response.status_code == 200:
            return AgentResponse(
                success=True,
                data=response.json(),
                message="All contacts retrieved successfully"
            )
        else:
            return AgentResponse(
                success=False,
                error=f"Failed to get contacts: {response.text}"
            )
            
    except Exception as e:
        return AgentResponse(success=False, error=str(e))

def search_contact(search_criteria: Dict[str, Any]) -> AgentResponse:
    """
    Search for a contact using LLM-powered matching over all contacts.
    """
    try:
        # Step 1: Get all contacts from the CRM
        all_contacts_response = get_all_contacts()

        if not all_contacts_response.success:
            return all_contacts_response

        contacts_data = all_contacts_response.data

        # Step 2: Check if we're searching for multiple names
        names = search_criteria.get("names", [])
        single_name = search_criteria.get("name")
        
        print(f"Search criteria: {search_criteria}")
        print(f"Names: {names}, Single name: {single_name}")
        
        if names:
            # Handle multiple names - search for each one
            found_contacts = []
            for name in names:
                single_search_criteria = {"name": name}
                result = search_single_contact(contacts_data, single_search_criteria)
                if result.success and result.data:
                    found_contacts.append(result.data)
            
            if found_contacts:
                return AgentResponse(
                    success=True,
                    data={"contacts": found_contacts},
                    message=f"Found {len(found_contacts)} contacts"
                )
            else:
                return AgentResponse(
                    success=False,
                    error="No contacts found matching the given criteria."
                )
        else:
            # Handle single name search
            return search_single_contact(contacts_data, search_criteria)

    except Exception as e:
        return AgentResponse(success=False, error=str(e))

def search_single_contact(contacts_data: Dict[str, Any], search_criteria: Dict[str, Any]) -> AgentResponse:
    """
    Search for a single contact using LLM-powered matching.
    """
    try:
        # Construct prompt for LLM
        prompt = CONTACT_SEARCH_PROMPT.format(
            contacts_data=json.dumps(contacts_data),
            search_criteria=json.dumps(search_criteria)
        )

        messages = [
            {"role": "system", "content": "You are a contact search agent. Return only the contact ID or 'null'."},
            {"role": "user", "content": prompt}
        ]

        # Query the LLM to get the matching contact ID
        llm_response = get_groq_chat_completion(messages=messages, temperature=0.1)
        
        # Clean and parse the LLM response
        contact_id = llm_response.strip()
        print(f"Original LLM response: {contact_id}")
        
        # Remove any code blocks, explanations, or extra text
        if "```" in contact_id:
            # Extract content between code blocks
            start = contact_id.find("```") + 3
            end = contact_id.rfind("```")
            if end > start:
                contact_id = contact_id[start:end].strip()
                print(f"Extracted from code block: {contact_id}")
        
        # Remove quotes and extra whitespace
        contact_id = contact_id.strip().strip('"').strip("'")
        print(f"Cleaned contact_id: {contact_id}")
        
        # Check if it's a valid ID (numeric string)
        if contact_id and contact_id.lower() != "null" and contact_id.isdigit():
            print(f"Valid contact ID found: {contact_id}")
            return get_contact_by_id(contact_id)
        else:
            print(f"Invalid contact ID: {contact_id}")
            return AgentResponse(
                success=False,
                error="No contact found matching the given criteria."
            )

    except Exception as e:
        return AgentResponse(success=False, error=str(e))

def delete_contact(contact_id: str) -> AgentResponse:
    """
    Delete a contact
    """
    try:
        # First get the contact data for notification
        contact_data = None
        try:
            get_response = requests.get(f"{settings.API_BASE_URL}/contacts/{contact_id}")
            if get_response.status_code == 200:
                contact_data = get_response.json()
        except:
            pass  # If we can't get contact data, we'll still proceed with deletion
        
        response = requests.delete(
            f"{settings.API_BASE_URL}/contacts/{contact_id}",
        )
        
        if response.status_code == 200:
            # Send email notification
            try:
                if contact_data:
                    email_response = email_agent.notify_contact_deleted(
                        contact_data, 
                        settings.EMAIL_USERNAME
                    )
                else:
                    email_response = email_agent.notify_operation_success(
                        "Delete Contact",
                        f"Contact with ID {contact_id} deleted successfully",
                        settings.EMAIL_USERNAME
                    )
                print(f"Email notification sent: {email_response.success}")
            except Exception as email_error:
                print(f"Failed to send email notification: {email_error}")
            
            return AgentResponse(
                success=True,
                data=response.json(),
                message="Contact deleted successfully"
            )
        else:
            # Send failure notification
            try:
                email_agent.notify_operation_failed(
                    "Delete Contact",
                    f"Failed to delete contact: {response.text}",
                    settings.EMAIL_USERNAME
                )
            except Exception as email_error:
                print(f"Failed to send failure email: {email_error}")
            
            return AgentResponse(
                success=False,
                error=f"Failed to delete contact: {response.text}"
            )
            
    except Exception as e:
        # Send failure notification
        try:
            email_agent.notify_operation_failed(
                "Delete Contact",
                str(e),
                settings.EMAIL_USERNAME
            )
        except Exception as email_error:
            print(f"Failed to send failure email: {email_error}")
        
        return AgentResponse(success=False, error=str(e))

import json
from typing import Dict, Any, List
from app.domain.AiAgent.OrchestratorAgent.data.DataModel import DecomposedQuery, TaskRequest, AgentResponse, ActionType
from app.domain.AiAgent.OrchestratorAgent.usecase.query_decomposer import decompose_query,extract_contact_info
from app.domain.AiAgent.ContactAgent.usecase.contact_agent import (
    execute_task,create_contact,update_contact,get_contact,get_contact_by_id,get_all_contacts,search_contact,delete_contact
)
from app.domain.AiAgent.EmailAgent.usecase.email_agent import email_agent
from app.infra.config import settings
from app.shared.utils.common_functions import CommonFuntions

def process_query(query:str,user_email:str = None) -> Dict[str,Any]:
    """
    Process user Query and orchestrate agents
    """
    try:
        CommonFuntions.write_log(f"Processing query: {query}")
        CommonFuntions.write_log(f"User email: {user_email}")
        
        decomposed_query = decompose_query(query)
        CommonFuntions.write_log(f"Decomposed query tasks: {len(decomposed_query.tasks)}")
        CommonFuntions.write_log(f"Requires sequential execution: {decomposed_query.requires_sequential_execution}")
        
        if decomposed_query.requires_sequential_execution or len(decomposed_query.tasks) > 1:
            CommonFuntions.write_log("Executing tasks sequentially")
            results = execute_sequential_tasks(decomposed_query.tasks,query)
        else:
            CommonFuntions.write_log("Executing tasks in parallel")
            results = execute_parallel_tasks(decomposed_query.tasks,query)
        
        CommonFuntions.write_log(f"Task execution completed. Results: {len(results)}")
        
        # Send summary notification
        try:
            notification_email = user_email if user_email else settings.EMAIL_USERNAME
            CommonFuntions.write_log(f"Sending summary notification to: {notification_email}")
            email_agent.notify_multiple_operations(results, notification_email)
            CommonFuntions.write_log("Summary notification sent successfully")
        except Exception as email_error:
            CommonFuntions.write_error_log(f"Failed to send summary notification: {email_error}")
        
        CommonFuntions.write_log("Query processing completed successfully")
        return {
            "success": True,
            "results": results,
            "message": "Query processed successfully"
        }
    
    except Exception as e:
        CommonFuntions.write_error_log(f"Error processing query: {str(e)}")
        # Send failure notification
        try:
            notification_email = user_email if user_email else settings.EMAIL_USERNAME
            email_agent.notify_operation_failed(
                "Query Processing",
                str(e),
                notification_email
            )
        except Exception as email_error:
            CommonFuntions.write_error_log(f"Failed to send failure notification: {email_error}")
        
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to process query"
        }

def execute_sequential_tasks(tasks:List[TaskRequest],original_query:str) -> List[Dict[str,Any]]:
    """
    Execute tasks sequentially (when order matters)
    """

    results = []
    context = {}

    CommonFuntions.write_log(f"Starting sequential execution of {len(tasks)} tasks")

    for i, task in enumerate(tasks):
        CommonFuntions.write_log(f"Executing task {i+1}/{len(tasks)}: {task.action.value}")
        enhanced_task = enhance_task_with_context(task,context,original_query)
        
        if is_contact_task(enhanced_task.action):
               CommonFuntions.write_log(f"Executing contact task: {enhanced_task.action.value}")
               result = execute_task(enhanced_task)
        else:
             CommonFuntions.write_error_log(f"Unknown task type: {enhanced_task.action.value}")
             result = AgentResponse(success=False,error = "Unknown task type")
    
        task_result = {
             "task":enhanced_task.action.value,
             "success":result.success,
             "data":result.data,
             "error":result.error,
             "message":result.message
        }
        results.append(task_result)
        CommonFuntions.write_log(f"Task {i+1} completed: {result.success} - {result.message}")

        if result.success and result.data:
             context[enhanced_task.action.value] = result.data
             CommonFuntions.write_log(f"Added task result to context: {enhanced_task.action.value}")
    
    CommonFuntions.write_log(f"Sequential execution completed. {len(results)} tasks processed")
    return results

def enhance_task_with_context(task:TaskRequest,context:Dict,original_query:str):
    enhanced_task = task.copy()

    if task.action in [ActionType.CREATE_CONTACT,ActionType.UPDATE_CONTACT] and not task.payload:
        enhanced_task.payload = extract_contact_info(original_query,task.action)
    
    return enhanced_task

def is_contact_task(action: ActionType) -> bool:
        """
        Check if task is contact-related
        """
        contact_actions = [
            ActionType.CREATE_CONTACT,
            ActionType.UPDATE_CONTACT,
            ActionType.GET_CONTACT,
            ActionType.GET_ALL_CONTACTS,
            ActionType.DELETE_CONTACT
        ]
        return action in contact_actions
    
def execute_parallel_tasks(tasks:List[TaskRequest],original_query:str) -> List[Dict[str,Any]]:
    results = []
    for task in tasks:
        enhanced_task = enhance_task_with_payload(task,original_query)

        if is_contact_task(enhanced_task.action):
            result = execute_task(enhanced_task)
        else:
            result = AgentResponse(success=False,error="Unknown task type")
        
        task_result = {
                "task": enhanced_task.action.value,
                "success": result.success,
                "data": result.data,
                "error": result.error,
                "message": result.message
            }
        results.append(task_result)
    
    return results

def enhance_task_with_payload(task: TaskRequest, original_query: str) -> TaskRequest:
        """
        Enhance task with extracted payload
        """
        enhanced_task = task.copy()
        
        # If task needs payload but doesn't have it, extract it
        if task.action in [ActionType.CREATE_CONTACT, ActionType.UPDATE_CONTACT] and not task.payload:
            enhanced_task.payload = extract_contact_info(original_query, task.action)
        
        return enhanced_task

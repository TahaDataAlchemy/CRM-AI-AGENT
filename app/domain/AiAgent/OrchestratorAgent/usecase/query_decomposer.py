import json
from typing import Dict, Any
from app.domain.AiAgent.OrchestratorAgent.data.DataModel import DecomposedQuery, TaskRequest, ActionType
from app.domain.AiAgent.OrchestratorAgent.prompts.Query_Decomposer_Prompt import create_query_prompt
from app.domain.AiAgent.OrchestratorAgent.prompts.payload_createrPrompt import payload_create
from app.GROQ_CLIENT.groq_api import get_groq_chat_completion
from app.shared.utils.common_functions import CommonFuntions

# def decompose_query(query:str) ->DecomposedQuery:
#     """
#     Decomposing user query if there is more then one action 
    
#     """
#     try:
#         prompt = QUERY_DECOMPOSER_PROMPT.format(query=query)

#         messages = [
#             {"role":"system","content":"you are a qeury decomposer agent"},
#             {"role":"user","content":prompt}
#         ]

#         response = get_groq_chat_completion(messages=messages,temperature=0.1)

#         result = json.load(response)        
#         tasks = []
#         for task_data in result.get("tasks",[]):
#             task = TaskRequest(
#                 action=ActionType(task_data["action"]),
#                 payload=task_data.get("payload"),
#                 contact_id=task_data.get("contact_id"),
#                 search_criteria=task_data.get("search_criteria")
#             )
#             tasks.append(task)
#         return DecomposedQuery(
#             tasks=tasks,
#             requires_sequential_execution=result.get("requires_sequential_execution",False),
#             dependencies=result.get("dependencies")

#         )
#     except Exception as e:
#         return DecomposedQuery(
#             task = [TaskRequest(action=ActionType.GET_ALL_CONTACTS)],
#             requires_sequential_execution=False
#         )

# def extract_contact_info(query:str,action:ActionType) -> Dict[str,Any]:
#     """
#     Extract contact information from query for payload creation
#     """
#     try:
#         prompt = PAYLOAD_CREATOR_PROMPT.format(query=query,action=action.value)

#         messages = [
#             {"role": "system", "content": "You are a payload creator agent."},
#             {"role":"user","content":prompt}
#         ]

#         response = get_groq_chat_completion(messages=messages,temperature=0.1)

#         result = json.load(response)
#         return result
#     except Exception as e:
#         return {}

def decompose_query(query: str) -> DecomposedQuery:
    """
    Decomposing user query if there is more than one action 
    """
    try:
        CommonFuntions.write_log(f"Decomposing query: {query}")
        
        prompt = create_query_prompt(query=query)
        CommonFuntions.write_log("Created query prompt")

        messages = [
            {"role": "system", "content": "you are a query decomposer agent"},
            {"role": "user", "content": prompt}
        ]

        CommonFuntions.write_log("Sending request to GROQ API")
        response = get_groq_chat_completion(messages=messages, temperature=0.3)
        CommonFuntions.write_log("Received response from GROQ API")

        # Clean the response by removing any potential markdown code blocks
        cleaned_response = response.strip()
        if cleaned_response.startswith('```'):
            # Remove opening ``` and any language identifier
            cleaned_response = cleaned_response[cleaned_response.find('\n')+1:]
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response[:-3]  # Remove ```
        cleaned_response = cleaned_response.strip()

        CommonFuntions.write_log(f"Cleaned response: {cleaned_response}")
        result = json.loads(cleaned_response)
        
        tasks = []
        for task_data in result.get("tasks", []):
            task = TaskRequest(
                action=ActionType(task_data["action"]),
                payload=task_data.get("payload"),
                contact_id=task_data.get("contact_id"),
                search_criteria=task_data.get("search_criteria")
            )
            tasks.append(task)
        
        CommonFuntions.write_log(f"Created {len(tasks)} tasks from query decomposition")
        
        return DecomposedQuery(
            tasks=tasks,
            requires_sequential_execution=result.get("requires_sequential_execution", False),
            dependencies=result.get("dependencies")
        )
    except Exception as e:
        CommonFuntions.write_error_log(f"Error in decompose_query: {e}")
        # Try to create a simple fallback based on the query
        tasks = []
        
        CommonFuntions.write_log("Using fallback query decomposition")
        
        # Simple keyword-based fallback
        query_lower = query.lower()
        if "create" in query_lower and "contact" in query_lower:
            # Extract basic contact info for creation
            import re
            email_match = re.search(r'(\S+@\S+\.\S+)', query)
            name_match = re.search(r'name\s+(\w+)', query)
            
            if email_match and name_match:
                payload = {
                    "email": email_match.group(1),
                    "firstname": name_match.group(1)
                }
                tasks.append(TaskRequest(action=ActionType.CREATE_CONTACT, payload=payload))
                CommonFuntions.write_log("Created fallback CREATE_CONTACT task")
        
        if "fetch" in query_lower or "get" in query_lower or "show" in query_lower:
            # Extract name for search
            import re
            name_match = re.search(r'name\s+(\w+)', query)
            if name_match:
                search_criteria = {"name": name_match.group(1)}
                tasks.append(TaskRequest(action=ActionType.GET_CONTACT, search_criteria=search_criteria))
                CommonFuntions.write_log("Created fallback GET_CONTACT task")
        
        if not tasks:
            # If no specific tasks could be created, fall back to get all contacts
            tasks = [TaskRequest(action=ActionType.GET_ALL_CONTACTS)]
            CommonFuntions.write_log("Created fallback GET_ALL_CONTACTS task")
        
        CommonFuntions.write_log(f"Fallback decomposition created {len(tasks)} tasks")
        
        return DecomposedQuery(
            tasks=tasks,
            requires_sequential_execution=True  # Multiple tasks should be sequential
        )

def extract_contact_info(query: str, action: ActionType) -> Dict[str, Any]:
    """
    Extract contact information from query for payload creation
    """
    try:
        prompt = payload_create(query=query, action=action.value)

        messages = [
            {"role": "system", "content": "You are a payload creator agent."},
            {"role": "user", "content": prompt}
        ]

        response = get_groq_chat_completion(messages=messages, temperature=0.3)
        print(f"Payload Response :{response}")

        # Clean the response by removing any potential markdown code blocks
        cleaned_response = response.strip()
        if cleaned_response.startswith('```'):
            # Remove opening ``` and any language identifier
            cleaned_response = cleaned_response[cleaned_response.find('\n')+1:]
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response[:-3]  # Remove ```
        cleaned_response = cleaned_response.strip()

        print(f"Cleaned payload response: {cleaned_response}")
        result = json.loads(cleaned_response)
        return result
    except Exception as e:
        print(f"Error in extract_contact_info: {e}")
        return {}



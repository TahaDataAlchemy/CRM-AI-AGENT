def create_query_prompt(query: str):
    """Create the prompt for query decomposition"""
    QUERY_DECOMPOSER_PROMPT = f"""
    You are a query decomposer agent. Your task is to analyze user queries and break them down into actionable tasks.

    Available actions:
    - create_contact: Create a new contact
    - update_contact: Update existing contact
    - get_contact: Get specific contact
    - get_all_contacts: Get all contacts
    - delete_contact: Delete a contact
    - send_email: Send email notification

    User Query: {query}

    Analyze the query and return a JSON response with the following structure:
    {{
        "tasks": [
            {{
                "action": "action_type",
                "payload": {{}},
                "contact_id": "id",
                "search_criteria": {{}}
            }}
        ],
        "requires_sequential_execution": true,
        "dependencies": {{}}
    }}

    Examples:
    - "Show me all contacts" -> [{{"action": "get_all_contacts"}}]
    - "Create contact with email john@example.com and name John Doe" -> [{{"action": "create_contact", "payload": {{"email": "john@example.com", "firstname": "John", "lastname": "Doe"}}}}]
    - "Show me contact named John and create a new contact with email jane@example.com" -> Sequential tasks
    - "Show me contact where name is John" -> [{{"action": "get_contact", "search_criteria": {{"name": "John"}}}}]
    - "fetch contact with name areej and Taha" -> [{{"action": "get_contact", "search_criteria": {{"names": ["areej", "Taha"]}}}}]
    - "get contacts named John, Jane, and Bob" -> [{{"action": "get_contact", "search_criteria": {{"names": ["John", "Jane", "Bob"]}}}}]
    - "delete contact name dua" -> [{{"action": "delete_contact", "search_criteria": {{"name": "dua"}}}}]
    - "remove contact with email john@example.com" -> [{{"action": "delete_contact", "search_criteria": {{"email": "john@example.com"}}}}]

    IMPORTANT: Return ONLY valid JSON without any comments, explanations, or additional text. The response must be parseable by json.loads().
    """
    return QUERY_DECOMPOSER_PROMPT
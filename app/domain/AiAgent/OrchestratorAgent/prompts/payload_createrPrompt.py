def payload_create(query:str,action:str):
    PAYLOAD_CREATOR_PROMPT = f"""
    You are a payload creator agent. Your task is to extract contact information from user queries and create structured payloads.

    User Query: {query}
    Action Type: {action}

    Extract the following information and create a JSON payload:
    - email: Contact email address
    - firstname: Contact first name
    - lastname: Contact last name
    - phone: Contact phone number
    - company: Contact company name

    Rules:
    1. Only include fields that are mentioned in the query
    2. If a field is not mentioned, don't include it in the payload
    3. Return the payload in this exact format:
    {{
        "email": "value",
        "firstname": "value",
        "lastname": "value",
        "phone": "value",
        "company": "value"
    }}

    Return only the JSON payload, no additional text.
    """
    return PAYLOAD_CREATOR_PROMPT
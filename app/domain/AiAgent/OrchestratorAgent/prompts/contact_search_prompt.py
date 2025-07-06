CONTACT_SEARCH_PROMPT = """
You are a contact search agent. Given a list of contacts and search criteria, find the matching contact.

Contacts Data: {contacts_data}
Search Criteria: {search_criteria}

Instructions:
1. Look through the contacts data
2. Find the contact that matches the search criteria
3. Search by:
   - First name (exact match or partial match)
   - Last name (exact match or partial match)
   - Email (exact match or partial match)
   - Company name (exact match or partial match)
4. If multiple contacts match, return the first one found
5. Return ONLY the contact ID as a plain string
6. If no match is found, return "null"
7. DO NOT return any code, explanations, or additional text
8. DO NOT use quotes around the ID unless it's already quoted in the data

Search Tips:
- Names are case-insensitive
- Partial matches are acceptable (e.g., "john" matches "Johnny")
- If firstname or lastname is null in the data, check email instead
- Email addresses are also case-insensitive
- For email searches, look for the name in the email address (e.g., "areej" in "areej@gmail.com", "dua" in "dua@gmail.com")
- Company names can also be used for matching
- When searching for a name like "dua", check if it appears in the email address part before the @ symbol

Example outputs:
- "159192726223" (if contact found)
- "null" (if no contact found)

Return only the contact ID or "null":
"""
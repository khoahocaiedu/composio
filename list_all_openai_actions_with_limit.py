import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("Listing OpenAI actions with limit=200...")
try:
    tools = composio.tools.get(user_id=user_id, toolkits=["openai"], limit=200)
    print(f"Total OpenAI actions returned: {len(tools)}")
    
    for t in tools:
        if isinstance(t, dict):
            func = t.get('function', {})
            name = func.get('name')
            desc = func.get('description', '')
        else:
            name = getattr(t, 'name', 'N/A')
            desc = getattr(t, 'description', '')
            
        print(f"- {name}: {desc[:100]}...")
except Exception as e:
    print("Error:", e)

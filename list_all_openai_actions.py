import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("Listing all OpenAI actions...")
try:
    tools = composio.tools.get(user_id=user_id, toolkits=["openai"])
    print(f"Total OpenAI actions: {len(tools)}")
    
    for t in tools:
        # Check if t is dict
        if isinstance(t, dict):
            func = t.get('function', {})
            name = func.get('name')
            desc = func.get('description', '')
        else:
            name = getattr(t, 'name', 'N/A')
            desc = getattr(t, 'description', '')
            
        if "image" in name.lower() or "create" in name.lower() or "generate" in name.lower() or "dall" in name.lower():
            print(f"- {name}: {desc[:100]}...")
except Exception as e:
    print("Error:", e)

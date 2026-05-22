import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("Inspecting OPENAI_CREATE_IMAGE...")
try:
    tools = composio.tools.get(user_id=user_id, toolkits=["openai"], limit=200)
    for t in tools:
        if isinstance(t, dict):
            func = t.get('function', {})
            name = func.get('name')
            if name == 'OPENAI_CREATE_IMAGE':
                print("Action found!")
                print("Name:", name)
                print("Description:", func.get('description'))
                print("Parameters:")
                import json
                print(json.dumps(func.get('parameters', {}), indent=2))
        else:
            name = getattr(t, 'name', 'N/A')
            if name == 'OPENAI_CREATE_IMAGE':
                print("Action found as Object!")
                print("Name:", name)
                print("Description:", getattr(t, 'description', ''))
                print("Schema:", getattr(t, 'schema', ''))
except Exception as e:
    print("Error:", e)

import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("Inspecting dalle tools...")
try:
    tools = composio.tools.get(user_id=user_id, search="dall")
    print(f"Total dalle tools found: {len(tools)}")
    for t in tools:
        if isinstance(t, dict):
            print("Dict tool name:", t.get('function', {}).get('name'))
            print("Parameters:", t.get('function', {}).get('parameters'))
        else:
            print("Object tool name:", getattr(t, 'name', 'N/A'))
            print("Properties:", getattr(t, 'schema', 'N/A'))
except Exception as e:
    print("Error:", e)

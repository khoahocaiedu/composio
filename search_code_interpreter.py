import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("Searching tools for 'code'...")
try:
    tools = composio.tools.get(user_id=user_id, search="code")
    print(f"Total 'code' tools: {len(tools)}")
    for t in tools[:30]:
        if isinstance(t, dict):
            print(f"- {t.get('function', {}).get('name')}")
        else:
            print(f"- {getattr(t, 'name', 'N/A')}")
except Exception as e:
    print("Error:", e)

print("\nSearching tools for 'python'...")
try:
    tools = composio.tools.get(user_id=user_id, search="python")
    print(f"Total 'python' tools: {len(tools)}")
    for t in tools[:30]:
        if isinstance(t, dict):
            print(f"- {t.get('function', {}).get('name')}")
        else:
            print(f"- {getattr(t, 'name', 'N/A')}")
except Exception as e:
    print("Error:", e)

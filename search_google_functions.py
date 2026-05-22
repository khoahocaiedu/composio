import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("Searching tools for 'google'...")
try:
    tools = composio.tools.get(user_id=user_id, search="google")
    print(f"Total tools: {len(tools)}")
    names = []
    for tool in tools:
        if isinstance(tool, dict) and 'function' in tool:
            names.append(tool['function']['name'])
        elif hasattr(tool, 'name'):
            names.append(tool.name)
    print("Function names found:")
    for n in sorted(names)[:30]:
        print(f"- {n}")
except Exception as e:
    print("Error:", e)

print("\nSearching tools for 'sheets'...")
try:
    tools = composio.tools.get(user_id=user_id, search="sheets")
    print(f"Total tools: {len(tools)}")
    names = []
    for tool in tools:
        if isinstance(tool, dict) and 'function' in tool:
            names.append(tool['function']['name'])
        elif hasattr(tool, 'name'):
            names.append(tool.name)
    print("Sheets function names found:")
    for n in sorted(names)[:30]:
        print(f"- {n}")
except Exception as e:
    print("Error:", e)

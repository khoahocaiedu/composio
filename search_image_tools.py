import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("Searching tools for 'image'...")
try:
    tools = composio.tools.get(user_id=user_id, search="image")
    print(f"Total 'image' tools: {len(tools)}")
    for t in tools[:30]:
        name = getattr(t, 'name', 'N/A')
        desc = getattr(t, 'description', 'N/A')
        print(f"- {name}: {desc[:100]}...")
except Exception as e:
    print("Error:", e)

print("\nSearching tools for 'dall'...")
try:
    tools = composio.tools.get(user_id=user_id, search="dall")
    print(f"Total 'dall' tools: {len(tools)}")
    for t in tools[:30]:
        name = getattr(t, 'name', 'N/A')
        desc = getattr(t, 'description', 'N/A')
        print(f"- {name}: {desc[:100]}...")
except Exception as e:
    print("Error:", e)

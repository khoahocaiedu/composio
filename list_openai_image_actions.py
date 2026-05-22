import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("Searching tools for 'openai'...")
try:
    tools = composio.tools.get(user_id=user_id, search="openai")
    print(f"Total 'openai' tools: {len(tools)}")
    image_tools = []
    for t in tools:
        name = ""
        desc = ""
        if isinstance(t, dict) and 'function' in t:
            name = t['function']['name']
            desc = t['function'].get('description', '')
        elif hasattr(t, 'name'):
            name = t.name
            desc = getattr(t, 'description', '')
            
        if 'image' in name.lower() or 'picture' in name.lower() or 'draw' in name.lower():
            image_tools.append((name, desc))
            
    print("\nOpenAI Image tools found:")
    for name, desc in sorted(image_tools):
        print(f"- {name}: {desc[:100]}...")
except Exception as e:
    print("Error:", e)

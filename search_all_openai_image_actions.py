import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("Searching all openai tools for image actions...")
try:
    # Get all tools under "openai" app name
    tools = composio.tools.get(user_id=user_id, search="openai")
    print(f"Total tools returned: {len(tools)}")
    
    image_actions = []
    for t in tools:
        name = ""
        desc = ""
        if isinstance(t, dict) and 'function' in t:
            name = t['function']['name']
            desc = t['function'].get('description', '')
        elif hasattr(t, 'name'):
            name = t.name
            desc = getattr(t, 'description', '')
            
        if 'image' in name.lower() or 'create' in name.lower() or 'generate' in name.lower():
            image_actions.append((name, desc))
            
    print(f"\nFound {len(image_actions)} matching actions:")
    for name, desc in sorted(image_actions):
        print(f"- {name}: {desc[:150]}")
except Exception as e:
    print("Error:", e)

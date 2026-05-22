import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("Composio dir:", dir(composio))
print("Composio.actions dir:", dir(composio.actions) if hasattr(composio, 'actions') else "No actions attribute")
print("Composio.tools dir:", dir(composio.tools) if hasattr(composio, 'tools') else "No tools attribute")

# Try to list all actions of openai toolkit using get_actions or similar
try:
    actions = composio.actions.get(toolkit="openai")
    print(f"Total actions from actions.get(toolkit='openai'): {len(actions)}")
    for a in actions[:10]:
        print("-", a.name if hasattr(a, 'name') else a)
except Exception as e:
    print("Error getting actions directly:", e)

try:
    actions_all = composio.actions.get(search="image")
    print(f"Total actions from actions.get(search='image'): {len(actions_all)}")
    for a in actions_all[:20]:
        if hasattr(a, 'name'):
            print("-", a.name, getattr(a, 'appName', ''))
        else:
            print("-", a)
except Exception as e:
    print("Error getting actions with search='image':", e)

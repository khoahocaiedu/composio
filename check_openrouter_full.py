import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("=== ALL OpenRouter actions ===")
try:
    tools = composio.tools.get(user_id=user_id, toolkits=["openrouter"], limit=200)
    print(f"Total: {len(tools)}")
    
    for t in tools:
        if isinstance(t, dict):
            name = t.get('function', {}).get('name', '')
            desc = t.get('function', {}).get('description', '')[:200]
        else:
            name = getattr(t, 'name', '')
            desc = getattr(t, 'description', '')[:200]
        print(f"\n  [{name}]")
        print(f"  {desc}")
except Exception as e:
    print(f"Error: {e}")

# Also check OPENROUTER_CREATE_CHAT_COMPLETION schema - this can be used with image models
print("\n\n=== OPENROUTER_CREATE_CHAT_COMPLETION schema ===")
try:
    tools = composio.tools.get(user_id=user_id, tools=["OPENROUTER_CREATE_CHAT_COMPLETION"])
    if tools:
        t = tools[0]
        if isinstance(t, dict):
            import json
            params = t.get('function', {}).get('parameters', {})
            print(json.dumps(params, indent=2))
        else:
            print(repr(t))
except Exception as e:
    print(f"Error: {e}")

import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

try:
    tools = composio.tools.get(user_id=user_id, search="openai")
    print(f"Total tools: {len(tools)}")
    for t in tools:
        if isinstance(t, dict) and 'function' in t:
            print(f"- {t['function']['name']}")
        elif hasattr(t, 'name'):
            print(f"- {t.name}")
except Exception as e:
    print("Error:", e)

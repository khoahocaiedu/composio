import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("Searching tools for 'google'...")
try:
    tools = composio.tools.get(user_id=user_id, search="google")
    if tools:
        print("Tool representation:")
        print(repr(tools[0]))
except Exception as e:
    print("Error:", e)

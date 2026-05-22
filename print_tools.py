import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

try:
    tools = composio.tools.get(user_id=user_id, search="dall")
    print(f"Total tools: {len(tools)}")
    if len(tools) > 0:
        t = tools[0]
        print("Type:", type(t))
        print("Dir:", dir(t))
        # Print dictionary representation if possible
        if hasattr(t, 'dict'):
            print("Dict:", t.dict())
        elif hasattr(t, 'model_dump'):
            print("Model dump:", t.model_dump())
        else:
            print("String representation:", str(t))
            print("Repr:", repr(t))
except Exception as e:
    print("Error:", e)

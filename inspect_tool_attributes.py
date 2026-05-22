import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio
import json

composio = Composio()

print("Probing tools list...")
try:
    user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"
    tools = composio.tools.get(user_id=user_id, toolkits=["facebook"])
    if len(tools) > 0:
        first_tool = tools[0]
        print("Type of tools[0]:", type(first_tool))
        print("Attributes of tools[0]:", dir(first_tool))
        
        # If it has a dictionary representation
        try:
            if hasattr(first_tool, 'dict'):
                print("Dict rep keys:", first_tool.dict().keys())
            elif hasattr(first_tool, 'model_dump'):
                print("Model dump keys:", first_tool.model_dump().keys())
        except Exception as e:
            print("Error dumping:", e)
            
        # Let's print the string representation of the first tool
        print("Representation:")
        print(repr(first_tool))
        
        # Let's check how many tools there are
        print(f"Total tools returned: {len(tools)}")
except Exception as e:
    print("Error:", e)

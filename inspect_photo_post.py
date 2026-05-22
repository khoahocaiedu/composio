import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

print("Retrieving FACEBOOK_CREATE_PHOTO_POST details...")
try:
    user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"
    tools = composio.tools.get(user_id=user_id, toolkits=["facebook"])
    
    for t in tools:
        func = t.get('function', {})
        name = func.get('name')
        if name == "FACEBOOK_CREATE_PHOTO_POST":
            print("=" * 60)
            print("Action Name:", name)
            print("Description:", func.get('description'))
            print("Parameters:")
            params = func.get('parameters', {})
            properties = params.get('properties', {})
            required = params.get('required', [])
            for prop_name, prop_val in properties.items():
                req_str = " (Required)" if prop_name in required else ""
                print(f"  - {prop_name}{req_str}: {prop_val.get('description')}")
except Exception as e:
    print("Error:", e)

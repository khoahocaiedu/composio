import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

print("Listing all Facebook action details...")
try:
    user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"
    tools = composio.tools.get(user_id=user_id, toolkits=["facebook"])
    
    for t in tools:
        func = t.get('function', {})
        name = func.get('name')
        desc = func.get('description')
        params = func.get('parameters', {})
        
        # Check if it has post in name or description
        if "POST" in name or "CREATE" in name:
            print("=" * 60)
            print("Action Name:", name)
            print("Description:", desc)
            print("Parameters:")
            properties = params.get('properties', {})
            required = params.get('required', [])
            for prop_name, prop_val in properties.items():
                req_str = " (Required)" if prop_name in required else ""
                print(f"  - {prop_name}{req_str}: {prop_val.get('description')}")
except Exception as e:
    print("Error:", e)

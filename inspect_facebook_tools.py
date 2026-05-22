import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

print("Listing Facebook tools/actions...")
try:
    user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"
    # Get tools schema with user_id
    tools = composio.tools.get(user_id=user_id, toolkits=["facebook"])
    print("Type of tools returned:", type(tools))
    
    # Iterate schemas
    for t in tools:
        print("-" * 50)
        # Check what attributes the tool/action schema has
        # Commonly they are dictionary-like or have name, description, etc.
        if isinstance(t, dict):
            print("Name:", t.get('name'))
            print("Description:", t.get('description'))
            print("Slug:", t.get('slug'))
            print("Parameters:", t.get('parameters'))
        else:
            if hasattr(t, 'name'):
                print("Name:", t.name)
            if hasattr(t, 'slug'):
                print("Slug:", t.slug)
            if hasattr(t, 'description'):
                print("Description:", t.description)
            # Try printing representation
            print("Representation:", repr(t))
except Exception as e:
    print("Error listing Facebook tools:", e)

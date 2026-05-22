import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

print("Retrieving FACEBOOK_CREATE_POST details...")
try:
    # Get action details
    action_info = composio.actions.get(action="FACEBOOK_CREATE_POST")
    print("Action Name:", action_info.name)
    print("Description:", action_info.description)
    print("Parameters schema:", action_info.parameters)
except Exception as e:
    print(f"Error: {e}")

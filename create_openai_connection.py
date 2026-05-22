import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

# Step 1: Create auth config for OpenAI with API_KEY scheme
print("Step 1: Creating OpenAI auth config...")
try:
    auth_config = composio.auth_configs.create(
        toolkit="openai",
        options={
            "type": "use_custom_auth",
            "auth_scheme": "API_KEY",
            "name": "OpenAI API Key for KhoahocAI"
        }
    )
    print(f"Auth config created! ID: {auth_config.id}")
    print(f"Full repr: {repr(auth_config)}")
    
    # Step 2: Create connection link for user
    print("\nStep 2: Creating connection link...")
    conn_request = composio.connected_accounts.link(
        user_id=user_id,
        auth_config_id=auth_config.id
    )
    print(f"Connection request created!")
    print(f"Redirect URL: {conn_request.redirect_url}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"
auth_config_id = "ac_VCx-J5AUdErq" # Google Drive Auth Config ID from client

print(f"Initiating connection request for user: {user_id} and auth config: {auth_config_id}...")
try:
    connection_request = composio.connected_accounts.initiate(
        user_id=user_id,
        auth_config_id=auth_config_id
    )
    print("SUCCESS!")
    print("Redirect URL:", connection_request.redirectUrl)
except Exception as e:
    print("Error initiating:", e)

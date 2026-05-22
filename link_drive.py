import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"
auth_config_id = "ac_VCx-J5AUdErq" # Google Drive Auth Config ID

print(f"Linking user {user_id} with auth config {auth_config_id}...")
try:
    response = composio.connected_accounts.link(
        user_id=user_id,
        auth_config_id=auth_config_id
    )
    print("SUCCESS!")
    print("Type of response:", type(response))
    print("Attributes of response:", dir(response))
    print("Representation:", repr(response))
    
    # Try printing fields that might contain the redirect url
    for field in ['redirectUrl', 'redirect_url', 'url', 'link']:
        if hasattr(response, field):
            print(f"Field '{field}':", getattr(response, field))
            
    # Try dictionary access if applicable
    try:
        print("Dict keys:", response.dict().keys())
    except:
        pass
except Exception as e:
    print("Error linking:", e)

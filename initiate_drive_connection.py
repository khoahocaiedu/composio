import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("Checking available apps and seeking Google Drive/Sheets...")
try:
    # Let's search for Google Drive / Google Sheets tools or apps
    # In Composio, we can list toolkits or look at the SDK
    # Let's try initiating directly with "googledrive" or "googlesheets" if they exist
    # First, let's try calling composio.connected_accounts.initiate or composio.connected_accounts.link
    # Often, the auth_config_id can be obtained by slug
    # Let's inspect the tools or list them
    tools = composio.tools.get(slugs=["googledrive", "googlesheets"])
    print("Found tools:", [t.slug for t in tools])
except Exception as e:
    print("Error getting tools:", e)

# Let's try to list app auth configs or similar if available
try:
    print("Attempting to initiate Google Drive connection...")
    # Slug is 'googledrive'
    connection_request = composio.connected_accounts.initiate(
        user_id=user_id,
        auth_config_id="googledrive" # Let's see if slug works as auth_config_id
    )
    print("Google Drive connection request:")
    print("URL:", connection_request.redirectUrl)
except Exception as e:
    print("Error initiating googledrive:", e)

try:
    print("Attempting to initiate Google Sheets connection...")
    connection_request = composio.connected_accounts.initiate(
        user_id=user_id,
        auth_config_id="googlesheets"
    )
    print("Google Sheets connection request:")
    print("URL:", connection_request.redirectUrl)
except Exception as e:
    print("Error initiating googlesheets:", e)

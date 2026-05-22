import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("Attempting to link googlesheets via Composio-managed config...")
try:
    response = composio.connected_accounts.link(
        user_id=user_id,
        auth_config_id="googlesheets"
    )
    print("Google Sheets Link Success!")
    print("Redirect URL:", response.redirect_url)
except Exception as e:
    print("Google Sheets Link Error:", e)

print("\nAttempting to link googledrive via Composio-managed config...")
try:
    response = composio.connected_accounts.link(
        user_id=user_id,
        auth_config_id="googledrive"
    )
    print("Google Drive Link Success!")
    print("Redirect URL:", response.redirect_url)
except Exception as e:
    print("Google Drive Link Error:", e)

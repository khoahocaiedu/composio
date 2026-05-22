import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

# Check Google Sheets toolkit auth scheme
print("=== Checking Google Sheets toolkit ===")
tks = composio.toolkits.get()
for tk in tks:
    slug = getattr(tk, 'slug', '')
    if 'sheet' in slug.lower():
        print(f"Name: {tk.name}")
        print(f"Slug: {tk.slug}")
        print(f"Auth schemes: {tk.auth_schemes}")
        print(f"Composio managed schemes: {tk.composio_managed_auth_schemes}")
        print(f"No auth: {tk.no_auth}")
        print()

# Create Google Sheets connection link using the existing Google OAuth auth config
# Since Google Sheets is also OAUTH2 and Composio-managed, we can use the same
# approach as Google Drive
print("=== Creating Google Sheets auth config ===")
try:
    conn_request = composio.connected_accounts.link(
        user_id=user_id,
        auth_config_id="ac_VCx-J5AUdErq"  # existing Google OAuth config
    )
    print(f"Connection link: {conn_request.redirect_url}")
except Exception as e:
    print(f"Error with existing config: {e}")
    
    # Try creating a new one specifically for Google Sheets
    try:
        auth_config = composio.auth_configs.create(
            toolkit="googlesheets",
            options={
                "type": "use_composio_managed_auth",
            }
        )
        print(f"Google Sheets auth config created! ID: {auth_config.id}")
        
        conn_request = composio.connected_accounts.link(
            user_id=user_id,
            auth_config_id=auth_config.id
        )
        print(f"Connection link: {conn_request.redirect_url}")
    except Exception as e2:
        print(f"Error creating sheets config: {e2}")

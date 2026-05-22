import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

print("Listing managed Facebook pages...")
try:
    user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"
    result = composio.tools.execute(
        slug="FACEBOOK_GET_USER_PAGES",
        user_id=user_id,
        arguments={},
        dangerously_skip_version_check=True
    )
    
    # Safe printing
    result_str = repr(result)
    safe_str = result_str.encode('ascii', errors='replace').decode('ascii')
    print("Result of FACEBOOK_GET_USER_PAGES (safe print):")
    print(safe_str)
except Exception as e:
    err_str = str(e).encode('ascii', errors='replace').decode('ascii')
    print("Error getting pages:", err_str)

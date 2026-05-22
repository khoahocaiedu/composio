import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

print("Retrieving recent posts from Facebook page...")
try:
    user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"
    page_id = "786741061182982"
    
    result = composio.tools.execute(
        slug="FACEBOOK_GET_PAGE_POSTS",
        user_id=user_id,
        arguments={
            "page_id": page_id,
            "limit": 10,
            "fields": "id,message,created_time,permalink_url"
        },
        dangerously_skip_version_check=True
    )
    
    # Safe printing in case of unicode strings in result
    result_str = repr(result)
    safe_str = result_str.encode('ascii', errors='replace').decode('ascii')
    print("Result of FACEBOOK_GET_PAGE_POSTS:")
    print(safe_str)
except Exception as e:
    err_str = str(e).encode('ascii', errors='replace').decode('ascii')
    print("Error getting recent posts:", err_str)

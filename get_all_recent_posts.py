import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

print("Retrieving the last 15 posts from Facebook page...")
try:
    user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"
    page_id = "786741061182982"
    
    result = composio.tools.execute(
        slug="FACEBOOK_GET_PAGE_POSTS",
        user_id=user_id,
        arguments={
            "page_id": page_id,
            "limit": 15,
            "fields": "id,message,created_time,permalink_url,status_type"
        },
        dangerously_skip_version_check=True
    )
    
    import json
    result_str = json.dumps(result, indent=2, ensure_ascii=True)
    print(result_str)
except Exception as e:
    err_str = str(e).encode('ascii', errors='replace').decode('ascii')
    print("Error:", err_str)

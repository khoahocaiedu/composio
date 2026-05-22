import os
import json
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"
post_id = "786741061182982_122160190430987152"

print(f"Retrieving details for post {post_id}...")
try:
    result = composio.tools.execute(
        slug="FACEBOOK_GET_PAGE_POSTS", # or check if there is GET_POST
        user_id=user_id,
        arguments={
            "page_id": "786741061182982",
            "limit": 1,
            "fields": "id,message,created_time,permalink_url,status_type,attachments,picture,full_picture"
        },
        dangerously_skip_version_check=True
    )
    result_str = json.dumps(result, indent=2, ensure_ascii=True)
    print(result_str)
except Exception as e:
    print("Error:", e)

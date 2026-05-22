import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

duplicate_post_ids = [
    "786741061182982_122160188408987152",
    "786741061182982_122160188396987152"
]

print("Deleting duplicate posts from Facebook page...")
for post_id in duplicate_post_ids:
    print(f"Deleting post: {post_id}...")
    try:
        user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"
        result = composio.tools.execute(
            slug="FACEBOOK_DELETE_POST",
            user_id=user_id,
            arguments={
                "post_id": post_id
            },
            dangerously_skip_version_check=True
        )
        # Safe printing in case of unicode strings in result
        result_str = repr(result)
        safe_str = result_str.encode('ascii', errors='replace').decode('ascii')
        print(f"Result for delete {post_id}:")
        print(safe_str)
    except Exception as e:
        err_str = str(e).encode('ascii', errors='replace').decode('ascii')
        print(f"Error deleting post {post_id}:", err_str)

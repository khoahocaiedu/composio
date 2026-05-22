import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

print("Posting to Facebook page...")
try:
    user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"
    page_id = "786741061182982"
    message = "Chào các bạn! Đây là bài đăng tự động từ AI Agent thông qua Composio MCP. Chúc các bạn một ngày mới tốt lành và ngập tràn cảm hứng học tập AI! 🚀🤖 #KhoaHocAI #Composio #AIAgent"
    
    result = composio.tools.execute(
        slug="FACEBOOK_CREATE_POST",
        user_id=user_id,
        arguments={
            "page_id": page_id,
            "message": message
        },
        dangerously_skip_version_check=True
    )
    
    # Safe printing in case of unicode strings in result
    result_str = repr(result)
    safe_str = result_str.encode('ascii', errors='replace').decode('ascii')
    print("Result of FACEBOOK_CREATE_POST:")
    print(safe_str)
except Exception as e:
    err_str = str(e).encode('ascii', errors='replace').decode('ascii')
    print("Error posting to Facebook:", err_str)

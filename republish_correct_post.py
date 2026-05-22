import os
import shutil
import time
import json
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

# Define paths
source_photo = r"C:\Users\Windows\.gemini\antigravity\brain\1c57d74e-24ed-4701-b775-c051cc646a3b\gemini_flash_ui_1779417618288.png"
temp_dir = r"C:\Users\Windows\.composio\temp"
target_photo = os.path.join(temp_dir, "gemini_flash_ui.png")

# Initialize Composio with auto-upload enabled
composio = Composio(dangerously_allow_auto_upload_download_files=True)

user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"
page_id = "786741061182982"

# Post ID of the text-only post to delete
post_to_delete = "786741061182982_122160189590987152"

# 1. Delete the incorrect post
print(f"Deleting incorrect/unwanted post {post_to_delete}...")
try:
    delete_result = composio.tools.execute(
        slug="FACEBOOK_DELETE_POST",
        user_id=user_id,
        arguments={
            "post_id": post_to_delete
        },
        dangerously_skip_version_check=True
    )
    print("Delete result:", repr(delete_result))
except Exception as e:
    print("Error deleting post:", e)

# Wait 2 seconds
time.sleep(2)

# Ensure temp directory exists and copy the photo
print(f"Ensuring photo exists at: {target_photo}")
os.makedirs(temp_dir, exist_ok=True)
shutil.copy2(source_photo, target_photo)

# 2. Create the message
message = (
    "🚀 GOOGLE RA MẮT GEMINI 3.5 FLASH: BƯỚC NHẢY VỌT VỀ TỐC ĐỘ VÀ KHẢ NĂNG AGENTIC! 🚀\n\n"
    "Google đã chính thức trình làng thế hệ mô hình ngôn ngữ lớn mới nhất: Gemini 3.5 Flash! "
    "Đây là mô hình đầu tiên mở đường cho dòng sản phẩm Gemini 3.5 thế hệ mới, tối ưu hóa toàn diện cho hiệu suất cao, lập trình phức tạp và các tác vụ agentic dài hạn (long-horizon).\n\n"
    "⚡ Những điểm nhấn ấn tượng của Gemini 3.5 Flash:\n"
    "- Tốc độ vượt trội: Nhanh gấp 4 lần so với các mô hình Frontier hiện nay về tốc độ xuất token.\n"
    "- Hiệu năng xuất sắc: Vượt qua phiên bản tiền nhiệm Gemini 3.1 Pro trên nhiều benchmarks quan trọng.\n"
    "- Cửa sổ ngữ cảnh khổng lồ: Hỗ trợ lên tới 1 triệu token, cho phép xử lý lượng tài liệu và dữ liệu cực lớn.\n"
    "- Thiết kế cho Agentic AI: Tối ưu hóa suy luận (thinking), xuất dữ liệu cấu trúc (structured outputs), và phản hồi gọi hàm đa phương tiện.\n\n"
    "👉 Xem thêm thông tin chi tiết về trí tuệ nhân tạo và lộ trình ứng dụng thực tế trong cuộc sống tại:\n"
    "https://khoahocai.com.vn/ai-la-gi-kien-thuc-ve-tri-tue-nhan-tao-va-cach-ung-dung-trong-cuoc-song/\n\n"
    "---\n"
    "#KhoaHocAI #SaoViet #GoogleGemini #Gemini35Flash #AIAgent #AIInOffice #TechnologyNews #ArtificialIntelligence"
)

# 3. Publish the new photo post
print("Publishing the new photo post with the correct link...")
try:
    post_result = composio.tools.execute(
        slug="FACEBOOK_CREATE_PHOTO_POST",
        user_id=user_id,
        arguments={
            "page_id": page_id,
            "photo": target_photo,
            "message": message
        },
        dangerously_skip_version_check=True
    )
    # Safe print
    result_str = json.dumps(post_result, indent=2, ensure_ascii=True)
    print("Publish result:")
    print(result_str)
except Exception as e:
    print("Error publishing post:", e)

# 4. Verify current posts on page
print("\nVerifying current posts on page...")
try:
    feed_result = composio.tools.execute(
        slug="FACEBOOK_GET_PAGE_POSTS",
        user_id=user_id,
        arguments={
            "page_id": page_id,
            "limit": 5,
            "fields": "id,message,created_time,permalink_url,status_type"
        },
        dangerously_skip_version_check=True
    )
    feed_str = json.dumps(feed_result, indent=2, ensure_ascii=True)
    print("Recent Feed:")
    print(feed_str)
except Exception as e:
    print("Error getting feed:", e)

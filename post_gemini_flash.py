import os
import shutil
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

# Define paths
source_photo = r"C:\Users\Windows\.gemini\antigravity\brain\1c57d74e-24ed-4701-b775-c051cc646a3b\gemini_flash_ui_1779417618288.png"
temp_dir = r"C:\Users\Windows\.composio\temp"
target_photo = os.path.join(temp_dir, "gemini_flash_ui.png")

# Ensure temp directory exists and copy the photo
print(f"Copying photo to allowed temp directory: {target_photo}")
os.makedirs(temp_dir, exist_ok=True)
shutil.copy2(source_photo, target_photo)

# Initialize Composio with auto-upload enabled
composio = Composio(dangerously_allow_auto_upload_download_files=True)

print("Posting Gemini 3.5 Flash update with photo to Facebook page...")
try:
    user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"
    page_id = "786741061182982"
    
    # Message content
    message = (
        "🚀 GOOGLE RA MẮT GEMINI 3.5 FLASH: BƯỚC NHẢY VỌT VỀ TỐC ĐỘ VÀ KHẢ NĂNG AGENTIC! 🚀\n\n"
        "Google đã chính thức trình làng thế hệ mô hình ngôn ngữ lớn mới nhất: Gemini 3.5 Flash! "
        "Đây là mô hình đầu tiên mở đường cho dòng sản phẩm Gemini 3.5 thế hệ mới, tối ưu hóa toàn diện cho hiệu suất cao, lập trình phức tạp và các tác vụ agentic dài hạn (long-horizon).\n\n"
        "⚡ Những điểm nhấn ấn tượng của Gemini 3.5 Flash:\n"
        "- Tốc độ vượt trội: Nhanh gấp 4 lần so với các mô hình Frontier hiện nay về tốc độ xuất token.\n"
        "- Hiệu năng xuất sắc: Vượt qua phiên bản tiền nhiệm Gemini 3.1 Pro trên nhiều thang đo chuẩn (benchmarks) quan trọng.\n"
        "- Cửa sổ ngữ cảnh khổng lồ: Hỗ trợ lên tới 1 triệu token (1M context window), cho phép xử lý lượng tài liệu và dữ liệu cực lớn.\n"
        "- Thiết kế cho Agentic AI: Tối ưu hóa suy luận (thinking), xuất dữ liệu cấu trúc (structured outputs), và phản hồi gọi hàm đa phương tiện (multimodal function calling).\n\n"
        "Mô hình hiện đã chính thức khả dụng trên ứng dụng Gemini, chế độ AI Mode của Google Search, và thông qua Gemini API (Google AI Studio & Android Studio).\n\n"
        "👉 Để tìm hiểu sâu hơn về cách ứng dụng Gemini 3.5 Flash vào công việc và lập trình thực tế, hãy xem ngay bài viết chi tiết tại:\n"
        "https://khoahocai.edu.vn/google-gemini-3-5-flash-moi-nhat/\n\n"
        "---\n"
        "#KhoaHocAI #SaoViet #GoogleGemini #Gemini35Flash #AIAgent #AIInOffice #TechnologyNews #ArtificialIntelligence"
    )
    
    result = composio.tools.execute(
        slug="FACEBOOK_CREATE_PHOTO_POST",
        user_id=user_id,
        arguments={
            "page_id": page_id,
            "photo": target_photo,
            "message": message
        },
        dangerously_skip_version_check=True
    )
    
    # Safe printing in case of unicode strings in result
    result_str = repr(result)
    safe_str = result_str.encode('ascii', errors='replace').decode('ascii')
    print("Result of FACEBOOK_CREATE_PHOTO_POST:")
    print(safe_str)
except Exception as e:
    err_str = str(e).encode('ascii', errors='replace').decode('ascii')
    print("Error posting to Facebook:", err_str)

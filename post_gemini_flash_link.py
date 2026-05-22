import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

print("Posting Gemini 3.5 Flash update with article link to Facebook page...")
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
        "👉 Xem chi tiết lộ trình học tập và ứng dụng thực hành ngay tại bài viết dưới đây!"
    )
    
    link_url = "https://khoahocai.edu.vn/google-gemini-3-5-flash-moi-nhat/"
    
    result = composio.tools.execute(
        slug="FACEBOOK_CREATE_POST",
        user_id=user_id,
        arguments={
            "page_id": page_id,
            "message": message,
            "link": link_url
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

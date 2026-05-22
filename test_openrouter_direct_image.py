import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

# Nhập OpenRouter API Key từ file .env
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("[Error] Vui lòng thêm OPENROUTER_API_KEY vào file .env trước khi chạy!")
    print("Ví dụ trong file .env:")
    print("COMPOSIO_API_KEY=your_key")
    print("OPENROUTER_API_KEY=sk-or-v1-xxxx...")
    exit(1)

test_prompt = "A clean, modern infographic-style illustration showing a roadmap for learning AI in 2026, with icons representing different AI tools like Gemini, ChatGPT, Claude. Professional blue and white color scheme, digital art style."

print("=== Gửi yêu cầu sinh ảnh trực tiếp đến OpenRouter API ===")
print("Model đề xuất: black-forest-labs/flux-schnell")

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "black-forest-labs/flux-schnell",
    "messages": [
        {
            "role": "user",
            "content": test_prompt
        }
    ],
    # Khai báo modalities là image để OpenRouter biết cần sinh ảnh
    "modalities": ["image"],
    "max_tokens": 1000
}

try:
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    
    res_data = response.json()
    
    # Lưu kết quả thô để kiểm tra
    with open("openrouter_image_response.json", "w", encoding="utf-8") as f:
        json.dump(res_data, f, indent=2, default=str)
    print("Đã lưu kết quả phản hồi vào file openrouter_image_response.json")
    
    if response.status_code == 200:
        choices = res_data.get("choices", [])
        if choices:
            message = choices[0].get("message", {})
            content = message.get("content", "")
            
            print("\n[Thành công!] Kết quả trả về:")
            print(f"Nội dung content (chứa base64 hoặc URL ảnh): {content[:300]}...")
            
            # Kiểm tra xem có chứa URL ảnh base64 không
            if "data:image" in content or "http" in content:
                print("\n=> Đã tìm thấy dữ liệu ảnh trong response!")
            else:
                print("\n=> Cảnh báo: Response không chứa định dạng ảnh mong muốn.")
        else:
            print("Response không có choices.")
    else:
        error_msg = res_data.get("error", {}).get("message", "Unknown error")
        print(f"\n[Lỗi từ OpenRouter] Chi tiết: {error_msg}")
        print("Vui lòng kiểm tra lại xem API Key đã được mở khóa (Allow) mô hình black-forest-labs/flux-schnell chưa.")

except Exception as e:
    print(f"Error: {e}")

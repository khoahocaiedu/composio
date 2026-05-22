import os, json
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

test_prompt = "A clean, modern infographic-style illustration showing a roadmap for learning AI in 2026, with icons representing different AI tools like Gemini, ChatGPT, Claude. Professional blue and white color scheme, digital art style."

print("=== Test 1: OpenRouter chat completion with dall-e-3 ===")
try:
    result = composio.tools.execute(
        slug="OPENROUTER_CREATE_CHAT_COMPLETION",
        user_id=user_id,
        arguments={
            "model": "openai/dall-e-3",
            "messages": [
                {"role": "user", "content": test_prompt}
            ]
        },
        dangerously_skip_version_check=True
    )
    print(f"Result type: {type(result)}")
    print(f"Result repr: {repr(result)[:500]}")
    
    if hasattr(result, 'data'):
        print(f"\nData: {json.dumps(result.data, indent=2, default=str)[:1000]}")
    if hasattr(result, 'response_data'):
        print(f"\nResponse data: {result.response_data}")
    if hasattr(result, 'model_dump'):
        d = result.model_dump()
        print(f"\nModel dump keys: {d.keys()}")
        print(f"Model dump: {json.dumps(d, indent=2, default=str)[:2000]}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    
    # Fallback: try listing available image models first
    print("\n\n=== Fallback: Listing image models on OpenRouter ===")
    try:
        result2 = composio.tools.execute(
            slug="OPENROUTER_LIST_AVAILABLE_MODELS",
            user_id=user_id,
            arguments={},
            dangerously_skip_version_check=True
        )
        r = result2.model_dump() if hasattr(result2, 'model_dump') else str(result2)
        rs = json.dumps(r, indent=2, default=str) if isinstance(r, dict) else str(r)
        
        # Search for image-related models
        if 'image' in rs.lower() or 'dall' in rs.lower() or 'flux' in rs.lower():
            lines = rs.split('\n')
            for i, line in enumerate(lines):
                if any(kw in line.lower() for kw in ['image', 'dall', 'flux', 'stable', 'sdxl']):
                    start = max(0, i-2)
                    end = min(len(lines), i+3)
                    for j in range(start, end):
                        print(lines[j])
                    print("---")
        else:
            print("No image models found in first scan. Output length:", len(rs))
            print("First 500 chars:", rs[:500])
    except Exception as e2:
        print(f"Error listing models: {e2}")

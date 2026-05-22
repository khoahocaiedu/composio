import os, json
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("=== Testing Chat Completion with google/gemini-3.5-flash and max_tokens=100 ===")
try:
    result = composio.tools.execute(
        slug="OPENROUTER_CREATE_CHAT_COMPLETION",
        user_id=user_id,
        arguments={
            "model": "google/gemini-3.5-flash",
            "messages": [
                {"role": "user", "content": "Hello! Reply with 'OpenRouter connection successful!'"}
            ],
            "max_tokens": 100
        },
        dangerously_skip_version_check=True
    )
    print("Result structure:", type(result))
    
    # Safely print result data
    r = result
    if hasattr(result, 'model_dump'):
        r = result.model_dump()
        
    print(json.dumps(r, indent=2, default=str)[:1500])
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

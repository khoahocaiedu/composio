import os, json
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("=== Testing OPENROUTER_LIST_USER_MODELS ===")
try:
    result = composio.tools.execute(
        slug="OPENROUTER_LIST_USER_MODELS",
        user_id=user_id,
        arguments={},
        dangerously_skip_version_check=True
    )
    r = result.model_dump() if hasattr(result, 'model_dump') else str(result)
    print("Keys:", r.keys() if isinstance(r, dict) else "Not a dict")
    
    # Save output
    with open("openrouter_user_models.json", "w", encoding="utf-8") as f:
        json.dump(r, f, indent=2, default=str)
    print("Saved user models to openrouter_user_models.json")
    
    # Print content
    data = r.get("data", {})
    if isinstance(data, dict):
        models = data.get("data", [])
        print(f"Total user models: {len(models)}")
        for m in models[:30]:
            print(f"  - {m.get('id')} ({m.get('name')})")
    else:
        print(str(data)[:1000])
        
except Exception as e:
    print(f"Error: {e}")

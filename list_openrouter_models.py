import os, json
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("=== Listing all available models on OpenRouter ===")
try:
    result = composio.tools.execute(
        slug="OPENROUTER_LIST_AVAILABLE_MODELS",
        user_id=user_id,
        arguments={},
        dangerously_skip_version_check=True
    )
    
    r = result
    if hasattr(result, 'model_dump'):
        r = result.model_dump()
        
    print("Result structure keys:", r.keys() if isinstance(r, dict) else "Not a dict")
    
    # Let's save the raw output to examine
    with open("openrouter_models.json", "w", encoding="utf-8") as f:
        json.dump(r, f, indent=2, default=str)
        
    print("Saved all models to openrouter_models.json")
    
    # Try to filter and find image models in python
    data = r.get("data", {})
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except:
            pass
            
    models = []
    if isinstance(data, dict) and "data" in data:
        models = data["data"]
    elif isinstance(data, list):
        models = data
    elif isinstance(r, dict) and "items" in r:
        models = r["items"]
        
    print(f"Found {len(models)} models directly in structure.")
    
    image_keywords = ['dall', 'flux', 'diffusion', 'stable', 'sdxl', 'midjourney', 'playground', 'image', 'generation', 'art', 'recraft']
    matching_models = []
    
    # If models is a list of dicts
    if isinstance(models, list):
        for m in models:
            m_id = ""
            m_name = ""
            if isinstance(m, dict):
                m_id = m.get("id", "")
                m_name = m.get("name", "")
            else:
                m_id = str(m)
            
            if any(kw in m_id.lower() or kw in m_name.lower() for kw in image_keywords):
                matching_models.append((m_id, m_name))
                
    if matching_models:
        print(f"\nMatching Image/Generation Models ({len(matching_models)}):")
        for m_id, m_name in matching_models:
            print(f"  - ID: {m_id} | Name: {m_name}")
    else:
        print("\nNo matching image models found. Here are first 20 model IDs:")
        count = 0
        if isinstance(models, list):
            for m in models[:20]:
                if isinstance(m, dict):
                    print(f"  - {m.get('id')} ({m.get('name')})")
                else:
                    print(f"  - {m}")
        else:
            # print first 500 chars of data
            print(str(data)[:500])

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

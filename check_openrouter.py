import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("=== OpenRouter toolkit info ===")
tks = composio.toolkits.get()
for tk in tks:
    if 'openrouter' in getattr(tk, 'slug', '').lower():
        print(f"Name: {tk.name}")
        print(f"Slug: {tk.slug}")
        print(f"Auth schemes: {tk.auth_schemes}")
        print(f"Managed: {tk.composio_managed_auth_schemes}")
        meta = getattr(tk, 'meta', None)
        if meta:
            print(f"Tools count: {getattr(meta, 'tools_count', 'N/A')}")
            print(f"Description: {getattr(meta, 'description', 'N/A')[:200]}")
        print()

print("=== OpenRouter actions (image-related) ===")
try:
    tools = composio.tools.get(user_id=user_id, toolkits=["openrouter"], limit=200)
    print(f"Total OpenRouter actions: {len(tools)}")
    
    image_tools = []
    for t in tools:
        if isinstance(t, dict):
            name = t.get('function', {}).get('name', '')
            desc = t.get('function', {}).get('description', '')
        else:
            name = getattr(t, 'name', '')
            desc = getattr(t, 'description', '')
        
        if 'image' in name.lower() or 'generate' in name.lower() or 'create' in name.lower():
            image_tools.append((name, desc[:150]))
    
    if image_tools:
        print(f"\nImage-related tools ({len(image_tools)}):")
        for name, desc in image_tools:
            print(f"  - {name}: {desc}")
    else:
        print("\nNo image-specific tools found. Listing ALL tools:")
        for t in tools:
            if isinstance(t, dict):
                name = t.get('function', {}).get('name', '')
                desc = t.get('function', {}).get('description', '')[:100]
            else:
                name = getattr(t, 'name', '')
                desc = getattr(t, 'description', '')[:100]
            print(f"  - {name}: {desc}")
except Exception as e:
    print(f"Error: {e}")

import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

print("=== Listing all auth configs ===")
try:
    result = composio.auth_configs.list()
    print(f"Result type: {type(result)}")
    
    # Check if it has items
    items = []
    if hasattr(result, 'items'):
        items = result.items
    elif hasattr(result, 'data'):
        items = result.data
    else:
        try:
            items = list(result)
        except:
            pass
    
    print(f"Total auth configs: {len(items)}")
    for c in items:
        app = getattr(c, 'app_name', getattr(c, 'appName', ''))
        slug = getattr(c, 'toolkit_slug', getattr(c, 'toolkitSlug', getattr(c, 'slug', '')))
        cid = getattr(c, 'id', '')
        scheme = getattr(c, 'auth_scheme', getattr(c, 'authScheme', ''))
        managed = getattr(c, 'is_composio_managed', '')
        print(f"  - App: {app}, Slug: {slug}, ID: {cid}, Scheme: {scheme}, Managed: {managed}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

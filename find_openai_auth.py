import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

print("Listing all auth configurations on Composio to find OpenAI...")
try:
    configs = composio.auth_configs.get()
    print(f"Total auth configs: {len(configs)}")
    
    matches = []
    for c in configs:
        app_name = getattr(c, 'appName', getattr(c, 'app_name', 'N/A'))
        slug = getattr(c, 'slug', 'N/A')
        config_id = getattr(c, 'id', 'N/A')
        
        if 'openai' in str(app_name).lower() or 'openai' in str(slug).lower():
            matches.append((app_name, slug, config_id))
            
    print(f"\nFound {len(matches)} matching auth configs for OpenAI:")
    for app_name, slug, config_id in matches:
        print(f"- App: {app_name}, Slug: {slug}, Auth Config ID: {config_id}")
        
except Exception as e:
    print("Error:", e)

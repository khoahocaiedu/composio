import os, json
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

print("=== Checking for HTTP / REST toolkits ===")
try:
    toolkits = composio.toolkits.get()
    for tk in toolkits:
        slug = getattr(tk, 'slug', '').lower()
        if any(kw in slug for kw in ['http', 'rest', 'api', 'request', 'web', 'curl']):
            print(f"Toolkit: {tk.name} | Slug: {tk.slug}")
except Exception as e:
    print(f"Error: {e}")

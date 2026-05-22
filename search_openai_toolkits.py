import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("Listing all toolkits to find openai or dalle...")
try:
    tks = composio.toolkits.get()
    matches = []
    for tk in tks:
        slug = getattr(tk, 'slug', '')
        name = getattr(tk, 'name', '')
        if 'openai' in slug.lower() or 'dall' in slug.lower() or 'openai' in name.lower() or 'dall' in name.lower():
            matches.append((name, slug))
            
    print(f"\nFound {len(matches)} matching toolkits:")
    for name, slug in matches:
        print(f"- {name} (Slug: {slug})")
except Exception as e:
    print("Error:", e)

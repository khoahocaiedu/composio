import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio
import inspect

composio = Composio()
print("connected_accounts.initiate signature:")
print(inspect.signature(composio.connected_accounts.initiate))

print("\nListing toolkits...")
if hasattr(composio, 'toolkits'):
    try:
        # Let's see if there is a get or list method
        print("toolkits attributes:", dir(composio.toolkits))
        # Let's try to list toolkits
        tks = composio.toolkits.get()
        print("Total toolkits:", len(tks))
        print("Sample toolkits:")
        for tk in tks[:15]:
            print(f"- Name: {getattr(tk, 'name', 'N/A')}, Slug: {getattr(tk, 'slug', 'N/A')}")
    except Exception as e:
        print("Error listing toolkits:", e)

print("\nListing auth_configs...")
if hasattr(composio, 'auth_configs'):
    try:
        print("auth_configs attributes:", dir(composio.auth_configs))
        configs = composio.auth_configs.get()
        print("Total auth_configs:", len(configs))
        print("Sample auth_configs:")
        for c in configs[:15]:
            # Print app names / slugs
            print(f"- App: {getattr(c, 'appName', getattr(c, 'app_name', 'N/A'))}, Slug: {getattr(c, 'slug', 'N/A')}, ID: {getattr(c, 'id', 'N/A')}")
    except Exception as e:
        print("Error listing auth_configs:", e)

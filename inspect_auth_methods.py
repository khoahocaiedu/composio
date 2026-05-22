import os, inspect
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

# 1. Check auth_configs methods
print("=== auth_configs methods ===")
print(dir(composio.auth_configs))
print()

# 2. Check if there's a list method
for method_name in ['list', 'get_all', 'find', 'search', 'create']:
    if hasattr(composio.auth_configs, method_name):
        m = getattr(composio.auth_configs, method_name)
        print(f"auth_configs.{method_name} signature: {inspect.signature(m)}")
        print(f"auth_configs.{method_name} doc: {m.__doc__[:200] if m.__doc__ else 'None'}")
        print()

# 3. Check connected_accounts.initiate signature  
print("=== connected_accounts.initiate ===")
print(inspect.signature(composio.connected_accounts.initiate))
print(composio.connected_accounts.initiate.__doc__[:500] if composio.connected_accounts.initiate.__doc__ else "No doc")
print()

# 4. Check connected_accounts.link signature
if hasattr(composio.connected_accounts, 'link'):
    print("=== connected_accounts.link ===")
    print(inspect.signature(composio.connected_accounts.link))
    print(composio.connected_accounts.link.__doc__[:500] if composio.connected_accounts.link.__doc__ else "No doc")

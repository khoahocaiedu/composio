import os, inspect
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

# 1. Check delete method on connected_accounts
print("=== connected_accounts methods ===")
for m in ['delete', 'remove', 'disconnect', 'disable']:
    if hasattr(composio.connected_accounts, m):
        func = getattr(composio.connected_accounts, m)
        print(f"{m}: {inspect.signature(func)}")
        print(f"  doc: {func.__doc__[:200] if func.__doc__ else 'None'}")
        print()

# 2. Delete ca_zmPk6lJWciHN
print("=== Deleting ca_zmPk6lJWciHN ===")
try:
    result = composio.connected_accounts.delete("ca_zmPk6lJWciHN")
    print(f"Delete result: {result}")
except Exception as e:
    print(f"Error: {e}")

# 3. Also clean up the expired Google Drive account
print("\n=== Deleting expired Google Drive ca_fbsRI_EvyUd0 ===")
try:
    result = composio.connected_accounts.delete("ca_fbsRI_EvyUd0")
    print(f"Delete result: {result}")
except Exception as e:
    print(f"Error: {e}")

# 4. List remaining accounts to check for OpenRouter
print("\n=== Remaining accounts ===")
try:
    response = composio.connected_accounts.list()
    if hasattr(response, 'items'):
        items = response.items
    else:
        items = list(response)
    
    print(f"Total: {len(items)}")
    for acc in items:
        acc_id = getattr(acc, 'id', '')
        status = getattr(acc, 'status', '')
        toolkit = getattr(acc, 'toolkit', None)
        toolkit_slug = getattr(toolkit, 'slug', '') if toolkit else ''
        print(f"  - ID: {acc_id} | Toolkit: {toolkit_slug} | Status: {status}")
except Exception as e:
    print(f"Error listing: {e}")

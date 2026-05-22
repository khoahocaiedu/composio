import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

# Clean up INITIATED/EXPIRED accounts
to_delete = ["ca_wUI96rNRgiN6", "ca_xRWtGVuF5hWD"]  # OpenRouter INITIATED, Google Sheets EXPIRED

for acc_id in to_delete:
    try:
        result = composio.connected_accounts.delete(acc_id)
        print(f"Deleted {acc_id}: {result}")
    except Exception as e:
        print(f"Error deleting {acc_id}: {e}")

# Final verification
print("\n=== Final account list ===")
response = composio.connected_accounts.list()
items = response.items if hasattr(response, 'items') else list(response)
print(f"Total: {len(items)}")
for acc in items:
    acc_id = getattr(acc, 'id', '')
    status = getattr(acc, 'status', '')
    toolkit = getattr(acc, 'toolkit', None)
    toolkit_slug = getattr(toolkit, 'slug', '') if toolkit else ''
    print(f"  - ID: {acc_id} | Toolkit: {toolkit_slug} | Status: {status}")

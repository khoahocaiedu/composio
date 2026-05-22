import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio
import inspect

composio = Composio()
print("Methods in composio.connected_accounts:")
for name, member in inspect.getmembers(composio.connected_accounts):
    if not name.startswith('_'):
        print(f"- {name}: {inspect.signature(member) if callable(member) else 'Not callable'}")

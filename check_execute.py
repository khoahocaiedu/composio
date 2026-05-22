import os, inspect
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

print("tools.execute signature:", inspect.signature(composio.tools.execute))
print("tools.execute doc:", composio.tools.execute.__doc__[:500] if composio.tools.execute.__doc__ else "None")

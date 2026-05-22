import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio
import inspect

composio = Composio()
print("connected_accounts.link signature:")
print(inspect.signature(composio.connected_accounts.link))

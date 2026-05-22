import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio
import inspect

composio = Composio()
print("auth_configs.create signature:")
print(inspect.signature(composio.auth_configs.create))

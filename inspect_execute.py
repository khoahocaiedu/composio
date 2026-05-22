import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio
import inspect

composio = Composio()

print("Inspecting composio.tools...")
print("Attributes of composio.tools:", dir(composio.tools))

print("\nInspecting composio.tools.execute...")
print("Signature:", inspect.signature(composio.tools.execute))
print("Docstring:", composio.tools.execute.__doc__)

import inspect
from dotenv import load_dotenv
load_dotenv()
from composio import Composio

composio = Composio()
print("get signature:", inspect.signature(composio.tools.get))
print("get docstring:", composio.tools.get.__doc__)

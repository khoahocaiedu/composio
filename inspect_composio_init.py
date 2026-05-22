import inspect
from composio import Composio

# Print signature of __init__
sig = inspect.signature(Composio.__init__)
print("Composio client init signature:")
print(sig)

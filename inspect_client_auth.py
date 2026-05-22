import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
client = composio.client
print("Client attributes:", dir(client))

# Let's check how to list auth configs using client
try:
    # Check if there is something like get_auth_configs or list_auth_configs or similar
    for field in dir(client):
        if 'auth' in field.lower() or 'config' in field.lower():
            print(f"Client field: {field}")
except Exception as e:
    print("Error inspecting client fields:", e)

# Let's inspect the AuthConfigs manager or client endpoints
try:
    if hasattr(composio, 'auth_configs'):
        print("AuthConfigs attributes:", dir(composio.auth_configs))
        # Let's try listing it by calling composio.auth_configs.get or list
        # It complained about missing nanoid, let's see its signature
        import inspect
        if hasattr(composio.auth_configs, 'get'):
            print("auth_configs.get signature:", inspect.signature(composio.auth_configs.get))
        if hasattr(composio.auth_configs, 'list'):
            print("auth_configs.list signature:", inspect.signature(composio.auth_configs.list))
            configs = composio.auth_configs.list()
            print("Got configs list of type:", type(configs))
            print("Configs list rep:", repr(configs))
except Exception as e:
    print("Error inspecting auth_configs:", e)

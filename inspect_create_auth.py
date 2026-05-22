import os, inspect
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

# Check auth_config_create_params
print("=== Inspecting auth config create ===")
print("Signature:", inspect.signature(composio.auth_configs.create))
print("Full doc:", composio.auth_configs.create.__doc__)

# Check what auth_config_create_params.AuthConfig looks like
try:
    from composio_client.types import auth_config_create_params
    print("\n=== AuthConfig type ===")
    print(dir(auth_config_create_params))
    if hasattr(auth_config_create_params, 'AuthConfig'):
        print("AuthConfig:", auth_config_create_params.AuthConfig)
        if hasattr(auth_config_create_params.AuthConfig, '__annotations__'):
            print("Annotations:", auth_config_create_params.AuthConfig.__annotations__)
except ImportError:
    print("Cannot import auth_config_create_params directly")

# Also check if OpenAI toolkit uses API_KEY auth scheme
print("\n=== Checking OpenAI toolkit info ===")
tks = composio.toolkits.get()
for tk in tks:
    slug = getattr(tk, 'slug', '')
    if 'openai' in slug.lower():
        print(f"Toolkit: {getattr(tk, 'name', '')}")
        print(f"Slug: {slug}")
        print(f"All attributes: {[a for a in dir(tk) if not a.startswith('_')]}")
        for attr in dir(tk):
            if not attr.startswith('_'):
                val = getattr(tk, attr, None)
                if not callable(val):
                    print(f"  {attr} = {val}")

import os, inspect
from dotenv import load_dotenv
load_dotenv()

# Check AuthConfigUnionMember0 (likely for API_KEY type)
from composio_client.types import auth_config_create_params
print("=== AuthConfigUnionMember0 ===")
ac0 = auth_config_create_params.AuthConfigUnionMember0
print("Type:", type(ac0))
if hasattr(ac0, '__annotations__'):
    print("Annotations:", ac0.__annotations__)
if hasattr(ac0, '__required_keys__'):
    print("Required keys:", ac0.__required_keys__)
if hasattr(ac0, '__optional_keys__'):
    print("Optional keys:", ac0.__optional_keys__)

print("\n=== AuthConfigUnionMember0Credentials ===")
ac0c = auth_config_create_params.AuthConfigUnionMember0Credentials
print("Type:", type(ac0c))
if hasattr(ac0c, '__annotations__'):
    print("Annotations:", ac0c.__annotations__)

print("\n=== AuthConfigUnionMember1 ===")
ac1 = auth_config_create_params.AuthConfigUnionMember1
print("Type:", type(ac1))
if hasattr(ac1, '__annotations__'):
    print("Annotations:", ac1.__annotations__)
if hasattr(ac1, '__required_keys__'):
    print("Required keys:", ac1.__required_keys__)
if hasattr(ac1, '__optional_keys__'):
    print("Optional keys:", ac1.__optional_keys__)

print("\n=== AuthConfigUnionMember1Credentials ===")
ac1c = auth_config_create_params.AuthConfigUnionMember1Credentials
print("Type:", type(ac1c))
if hasattr(ac1c, '__annotations__'):
    print("Annotations:", ac1c.__annotations__)

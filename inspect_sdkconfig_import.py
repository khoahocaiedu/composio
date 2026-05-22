import composio
from composio.client.config import SDKConfig
print("SDKConfig annotations:")
for k, v in SDKConfig.__annotations__.items():
    print(f"  {k}: {v}")

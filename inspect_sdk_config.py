import inspect
import composio

try:
    # Let's search for SDKConfig in composio module
    for name, obj in inspect.getmembers(composio):
        if "SDKConfig" in name or "Config" in name:
            print(f"Name: {name}")
            try:
                # If it's a TypedDict or class, print annotations or fields
                if hasattr(obj, "__annotations__"):
                    print("Annotations:", obj.__annotations__)
            except Exception as e:
                print("Error getting annotations:", e)
except Exception as e:
    print("Error:", e)

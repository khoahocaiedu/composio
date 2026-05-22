import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
print("Inspecting composio object...")
print("Composio attributes:", dir(composio))

if hasattr(composio, 'apps'):
    print("Composio has 'apps' attribute.")
    print("Apps attributes:", dir(composio.apps))
    try:
        apps = composio.apps.get()
        print("Got apps of type:", type(apps))
        print("Sample apps:")
        if hasattr(apps, 'items'):
            for app in apps.items[:10]:
                print(app.name, app.slug)
        else:
            for app in list(apps)[:10]:
                print(app)
    except Exception as e:
        print("Error getting apps:", e)
else:
    print("Composio does not have 'apps' attribute.")

print("\nInspecting connected_accounts...")
print("connected_accounts attributes:", dir(composio.connected_accounts))

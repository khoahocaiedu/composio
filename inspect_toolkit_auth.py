import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

print("Retrieving googlesheets and googledrive toolkits...")
try:
    # Let's inspect what is returned by toolkits.get
    tks = composio.toolkits.get()
    for tk in tks:
        if tk.slug in ['googlesheets', 'googledrive']:
            print(f"\nToolkit: {tk.name} ({tk.slug})")
            print("Attributes:", dir(tk))
            # Let's print string rep and common fields
            print("Representation:", repr(tk))
            
            # Let's see if we can find auth_config_id or similar
            for field in ['auth_config_id', 'auth_config', 'id', 'authConfigId']:
                if hasattr(tk, field):
                    print(f"Field '{field}':", getattr(tk, field))
                    
            # Let's check if the Composio client has a way to resolve auth config for a slug
            try:
                # Some versions have composio.client.get_auth_config_id or similar
                # Let's look at the toolkit attributes and see if there are any methods
                pass
            except Exception as e:
                print("Error checking methods:", e)
except Exception as e:
    print("Error:", e)

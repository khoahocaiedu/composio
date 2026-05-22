import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

print("Listing all connected accounts...")
try:
    response = composio.connected_accounts.list()
    print("Response type:", type(response))
    print("Response representation:", repr(response))
    
    # Try iterating or checking data attributes
    if hasattr(response, 'items'):
        print("Items count:", len(response.items))
        for acc in response.items:
            print(f"Account: {acc}")
    elif hasattr(response, 'data'):
        print("Data count:", len(response.data))
        for acc in response.data:
            print(f"Account: {acc}")
    else:
        # Just try iterating
        try:
            for acc in response:
                print(f"Account: {acc}")
        except Exception as e:
            print("Cannot iterate:", e)
except Exception as e:
    print(f"Error listing accounts: {e}")

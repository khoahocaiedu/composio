import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("Searching tools for 'google'...")
try:
    tools = composio.tools.get(user_id=user_id, search="google")
    print(f"Total 'google' tools: {len(tools)}")
    toolkits = set()
    for tool in tools:
        if hasattr(tool, 'toolkit') and tool.toolkit:
            toolkits.add(getattr(tool.toolkit, 'slug', str(tool.toolkit)))
        else:
            toolkits.add(getattr(tool, 'appName', getattr(tool, 'app_name', 'unknown')))
    print("Google related toolkits:")
    for tk in sorted(toolkits):
        print(f"- {tk}")
except Exception as e:
    print("Error google:", e)

print("\nSearching tools for 'drive'...")
try:
    tools = composio.tools.get(user_id=user_id, search="drive")
    print(f"Total 'drive' tools: {len(tools)}")
    toolkits = set()
    for tool in tools:
        if hasattr(tool, 'toolkit') and tool.toolkit:
            toolkits.add(getattr(tool.toolkit, 'slug', str(tool.toolkit)))
        else:
            toolkits.add(getattr(tool, 'appName', getattr(tool, 'app_name', 'unknown')))
    print("Drive related toolkits:")
    for tk in sorted(toolkits):
        print(f"- {tk}")
except Exception as e:
    print("Error drive:", e)

print("\nSearching tools for 'sheets'...")
try:
    tools = composio.tools.get(user_id=user_id, search="sheets")
    print(f"Total 'sheets' tools: {len(tools)}")
    toolkits = set()
    for tool in tools:
        if hasattr(tool, 'toolkit') and tool.toolkit:
            toolkits.add(getattr(tool.toolkit, 'slug', str(tool.toolkit)))
        else:
            toolkits.add(getattr(tool, 'appName', getattr(tool, 'app_name', 'unknown')))
    print("Sheets related toolkits:")
    for tk in sorted(toolkits):
        print(f"- {tk}")
except Exception as e:
    print("Error sheets:", e)

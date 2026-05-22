import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()

# Let's try to run execution with empty args to see error schema
try:
    print("Executing FACEBOOK_CREATE_POST with empty args to get validation errors...")
    result = composio.tools.execute(
        action="FACEBOOK_CREATE_POST",
        user_id="pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607",
        arguments={}
    )
    print("Result:", result)
except Exception as e:
    print("Execution failed as expected. Error detail:")
    print(e)

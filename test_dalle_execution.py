import os
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

print("Attempting to execute DALL_E_GENERATE_IMAGE tool...")
try:
    # Use DALL-E tool to generate a test image
    result = composio.tools.execute(
        slug="DALL_E_GENERATE_IMAGE",
        user_id=user_id,
        arguments={
            "prompt": "A modern flat design icon of a robot programming a computer, 3d render, vibrant colors, dark background",
            "size": "1024x1024"
        },
        dangerously_skip_version_check=True
    )
    print("SUCCESS!")
    print("Result:", result)
except Exception as e:
    print("Error executing DALL-E:", e)

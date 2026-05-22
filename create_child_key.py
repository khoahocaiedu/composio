import requests
import json

import os
api_key = os.environ.get("OPENROUTER_API_KEY")

url = "https://openrouter.ai/api/v1/keys"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "name": "Local Completion Key"
}

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")

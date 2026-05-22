import os, json
from dotenv import load_dotenv
load_dotenv()

from composio import Composio

composio = Composio()
user_id = "pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607"

test_prompt = "A roadmap for learning AI in 2026, professional digital art, blue theme"

# Let's try different models and check how OpenRouter responds
models_to_try = [
    "black-forest-labs/flux-schnell",
    "stabilityai/stable-diffusion-xl",
    "google/imagen-3-fast",
    "bytedance/sdxl-lightning-4step",
]

for model in models_to_try:
    print(f"\n=== Testing model: {model} ===")
    try:
        # Test without extra schema parameters
        result = composio.tools.execute(
            slug="OPENROUTER_CREATE_CHAT_COMPLETION",
            user_id=user_id,
            arguments={
                "model": model,
                "messages": [
                    {"role": "user", "content": test_prompt}
                ]
            },
            dangerously_skip_version_check=True
        )
        print(f"Result successful: {result.get('successful') if isinstance(result, dict) else 'N/A'}")
        print(f"Result raw: {str(result)[:1000]}")
    except Exception as e:
        print(f"Error testing {model}: {e}")

print("\n=== Testing with extra arguments (if API supports it) ===")
try:
    # Try passing modalities even if not in schema, since some clients forward all kwargs
    result = composio.tools.execute(
        slug="OPENROUTER_CREATE_CHAT_COMPLETION",
        user_id=user_id,
        arguments={
            "model": "black-forest-labs/flux-schnell",
            "messages": [
                {"role": "user", "content": test_prompt}
            ],
            # We add modalities here, if the backend SDK strips unrecognized parameters it won't hurt
            "modalities": ["image"] 
        },
        dangerously_skip_version_check=True
    )
    print(f"Result with modalities: {str(result)[:1000]}")
except Exception as e:
    print(f"Error with modalities: {e}")

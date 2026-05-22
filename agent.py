import asyncio
import os
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv()

from composio import Composio
from agents import Agent, Runner
from composio_openai_agents import OpenAIAgentsProvider

async def main():
    # Check env variables
    composio_key = os.getenv("COMPOSIO_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    comp_prefix = composio_key[:6] if composio_key else "None"
    print(f"[Info] COMPOSIO_API_KEY prefix: {comp_prefix}")
    print(f"[Info] OPENAI_API_KEY found: {'Yes' if openai_key else 'No'}")
    
    if not openai_key:
        print("[Warning] OPENAI_API_KEY not found. Agent runs with OpenAI SDK might fail.")

    print("[Info] Connecting to Composio...")
    composio = Composio(provider=OpenAIAgentsProvider())
    user_id = "user_jrw3p7i"

    # Create session
    print("[Info] Creating/Retrieving session for user_id...")
    session = composio.create(user_id=user_id)
    tools = session.tools()
    print(f"[Info] Tools retrieved successfully: {len(tools)} tools registered.")

    # Initialize Agent
    print("[Info] Initializing Agent...")
    agent = Agent(
        name="Composio Assistant",
        instructions="You are a helpful assistant. Use Composio tools to execute tasks.",
        tools=tools,
    )

    print("[Info] Running Agent test task...")
    try:
        result = await Runner.run(
            starting_agent=agent,
            input="Star the composiohq/composio repo on GitHub",
        )
        print("\n=== Agent Result ===")
        print(result.final_output)
    except Exception as e:
        print(f"\n[Error] Exception during Agent execution: {e}")

if __name__ == "__main__":
    asyncio.run(main())

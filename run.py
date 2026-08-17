import asyncio
from agent_framework import Agent
from src.pulse_customer_intelligence.config import get_chat_client

async def main():
    agent = Agent(
        client=get_chat_client(),
        instructions="You are a helpful assistant.",
        name="smoke-test",
    )
    result = await agent.run("Say hello in one sentence.")
    print(result.text)

asyncio.run(main())
import asyncio
from src.pulse_customer_intelligence.agent import build_agent

SAMPLES = [
    "The tomatoes I got yesterday were mushy and clearly not fresh. Really disappointed.",
    "Delivery was super quick and the veggies were great!",
    "Why did onion prices jump 30% this week? Feels unfair.",
]

async def main():
    agent = build_agent()
    for feedback in SAMPLES:
        print(f"\n--- Feedback: {feedback}")
        result = await agent.run(feedback)
        print(result.text)

if __name__ == "__main__":
    asyncio.run(main())
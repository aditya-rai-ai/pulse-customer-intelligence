# Pulse — demo runner. Runs the triage agent over sample feedback and prints structured results.
import asyncio
from src.pulse_customer_intelligence.agent import build_agent
from src.pulse_customer_intelligence.models import Triage

SAMPLES = [
    "The tomatoes I got yesterday were mushy and clearly not fresh. Really disappointed.",
    "Delivery was super quick and the veggies were great!",
    "Why did onion prices jump 30% this week? Feels unfair.",
]

def clean_json(text: str) -> str:
    """Strip markdown code fences (```json ... ```) the model sometimes adds."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]          # take what's between the fences
        if text.startswith("json"):
            text = text[len("json"):]         # drop a leading 'json' label
    return text.strip()

async def main():
    agent = build_agent()
    for feedback in SAMPLES:
        result = await agent.run(feedback)
        triage = Triage.model_validate_json(clean_json(result.text))
        print(f"\n[{triage.priority}] {triage.sentiment.value}  |  {triage.category}")
        print(f"   → {triage.owning_department}")
        print(f"   {triage.summary}")

if __name__ == "__main__":
    asyncio.run(main())
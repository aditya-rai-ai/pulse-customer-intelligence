# Pulse — demo runner. Runs the multi-agent triage team over sample feedback.
import asyncio
from src.pulse_customer_intelligence.agents_team import build_coordinator
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
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[len("json"):]
    return text.strip()

async def main():
    coordinator = build_coordinator()
    for feedback in SAMPLES:
        result = await coordinator.run(feedback)
        triage = Triage.model_validate_json(clean_json(result.text))
        print(f"\n[{triage.priority}] {triage.sentiment.value}  |  {triage.category}")
        print(f"   → {triage.owning_department}")
        print(f"   {triage.summary}")

if __name__ == "__main__":
    asyncio.run(main())
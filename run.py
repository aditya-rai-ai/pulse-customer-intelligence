# Pulse — demo runner. Multi-agent triage + RAG grounding + guardrails.
import asyncio
from src.pulse_customer_intelligence.agents_team import build_coordinator
from src.pulse_customer_intelligence.models import Triage
from src.pulse_customer_intelligence.guardrails import check_input, check_output

SAMPLES = [
    "The tomatoes I got yesterday were mushy and clearly not fresh. Really disappointed.",
    "Delivery was super quick and the veggies were great!",
    "Why did onion prices jump 30% this week? Feels unfair.",
    "asdf",   # junk input — the input guardrail should reject this before the agent runs
]

def clean_json(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[len("json"):]
    return text.strip()

async def main():
    coordinator = build_coordinator()
    for feedback in SAMPLES:
        print(f"\n=== Feedback: {feedback!r}")

        # INPUT GUARDRAIL — check before spending any agent calls
        problem = check_input(feedback)
        if problem:
            print(f"   [BLOCKED by input guardrail] {problem}")
            continue

        result = await coordinator.run(feedback)
        triage = Triage.model_validate_json(clean_json(result.text))
        print(f"   [{triage.priority}] {triage.sentiment.value}  |  {triage.category}")
        print(f"   -> {triage.owning_department}")
        print(f"   Summary: {triage.summary}")
        print(f"   Reply:   {triage.suggested_response}")

        # OUTPUT GUARDRAIL — check the reply before it would be "sent"
        flags = check_output(triage.suggested_response, triage.priority)
        if flags:
            print("   [NEEDS HUMAN REVIEW]")
            for f in flags:
                print(f"       - {f}")

if __name__ == "__main__":
    asyncio.run(main())
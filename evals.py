"""Pulse's evaluation harness — measure the agent's behaviour with a score.

Instead of eyeballing outputs, we run the agent over a fixed 'golden dataset' of
inputs with known-correct answers, and count how many it gets right.
"""
import asyncio
import src.pulse_customer_intelligence.tracing as tracing
tracing.ENABLED = False   # silence step-tracing so the eval report is clean

from src.pulse_customer_intelligence.agents_team import build_coordinator
from src.pulse_customer_intelligence.models import Triage

# Golden dataset: inputs + the answers we consider correct.
TEST_CASES = [
    {"feedback": "The tomatoes were mushy and rotten.",           "category": "Freshness",       "sentiment": "Negative"},
    {"feedback": "Your delivery guy showed up three hours late!", "category": "Delivery",        "sentiment": "Negative"},
    {"feedback": "Everything has gotten way too expensive lately.","category": "Pricing",         "sentiment": "Negative"},
    {"feedback": "The app kept crashing when I tried to order.",  "category": "Support",         "sentiment": "Negative"},
    {"feedback": "Fast delivery, thank you so much!",             "category": "Delivery",        "sentiment": "Positive"},
    {"feedback": "The vegetables were excellent quality.",        "category": "Product Quality", "sentiment": "Positive"},
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
    passed = 0

    for case in TEST_CASES:
        result = await coordinator.run(case["feedback"])
        triage = Triage.model_validate_json(clean_json(result.text))

        category_ok = triage.category == case["category"]
        sentiment_ok = triage.sentiment.value == case["sentiment"]
        ok = category_ok and sentiment_ok
        passed += 1 if ok else 0

        print(f"\n[{'PASS' if ok else 'FAIL'}] {case['feedback']}")
        if not category_ok:
            print(f"      category:  expected '{case['category']}', got '{triage.category}'")
        if not sentiment_ok:
            print(f"      sentiment: expected '{case['sentiment']}', got '{triage.sentiment.value}'")

    total = len(TEST_CASES)
    print(f"\n{'='*45}")
    print(f"  SCORE: {passed}/{total} passed  ({100 * passed // total}%)")
    print(f"{'='*45}")

if __name__ == "__main__":
    asyncio.run(main())
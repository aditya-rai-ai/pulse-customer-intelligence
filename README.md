# Pulse — Customer Intelligence Agent

An AI agent that reads customer feedback and turns it into structured, routed intelligence. Built with Python and the Microsoft Agent Framework.

## What it does
Given a piece of customer feedback, the agent:
1. Determines sentiment (Positive / Neutral / Negative)
2. Classifies it into a category (Product Quality, Delivery, Pricing, Support, Freshness)
3. Calls a tool to look up the owning department
4. Assigns a priority and writes a one-line summary
5. Returns clean, validated structured data (not free-form text)

## Example
Input: "The tomatoes I got yesterday were mushy and clearly not fresh."

Output:

    [High] Negative  |  Freshness
       -> Quality Assurance <qa@company.com>
       Customer received mushy, non-fresh tomatoes.

## Tech
- Python 3.12, Microsoft Agent Framework
- Pydantic for structured output validation
- OpenAI (gpt-4o) as the model

## Run it
1. uv sync
2. Add your key to .env: OPENAI_API_KEY=sk-...
3. uv run run.py

## Status
Working prototype. Next: multi-agent orchestration, retrieval (RAG), evaluations, and guardrails.
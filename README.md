# Pulse — Customer Intelligence Agent

A production-shaped, multi-agent AI system that reads customer feedback and turns it into structured, routed, policy-grounded intelligence. Built from scratch in Python with the Microsoft Agent Framework.

Pulse doesn't just classify feedback — it orchestrates a team of specialized agents, grounds its replies in real company policy (RAG), guards against unsafe or unverified responses, traces every step, and is continuously improved against a measurable evaluation suite.

## What it does

Given a piece of customer feedback, Pulse:
1. Analyzes sentiment and category — using a team of agents, not one
2. Routes it to the owning department
3. Retrieves the relevant company policy *by meaning* (RAG) and drafts a grounded reply
4. Runs guardrails — blocks junk input, and flags risky or sensitive replies for human review
5. Returns clean, validated structured data

## Architecture

    Customer feedback
        |
        v
    Coordinator  (orchestrator)
        |  delegates to four specialist agents, each called as a tool:
        |-- Analyzer    -> sentiment + category
        |-- Router      -> owning department   (lookup tool)
        |-- Advisor     -> policy-grounded reply   (RAG knowledge base)
        \-- Summarizer  -> one-line summary
        |
        v
    Guardrails (input + output)  ->  escalate to a human if risky or negative
        |
        v
    Validated Triage  ->  { sentiment, category, department, priority, summary, reply }

Every agent and tool call is traced for observability, and the whole system is scored by an evaluation harness.

## Key features (the engineering, not just the bot)

- Multi-agent orchestration — a coordinator delegates to four single-purpose specialist agents.
- RAG grounding — replies are grounded in a company knowledge base, retrieved by meaning (embeddings + cosine similarity), not keywords. The agent admits when it has no relevant policy instead of inventing one.
- Guardrails + human escalation — input validation and output safety checks; high-priority or negative cases are flagged for human review rather than auto-sent.
- Observability — built-in middleware traces every agent and tool call with timing.
- Evaluation-driven development — a golden-dataset eval harness scores the system. An analyzer misclassification on ambiguous inputs was surfaced by the evals and fixed by refining category definitions, improving the score from 83% to 100%.

## Tech stack

- Python 3.12
- Microsoft Agent Framework — multi-agent orchestration, tools, middleware
- OpenAI — gpt-4o for reasoning, text-embedding-3-small for RAG retrieval
- Pydantic — structured output validation

## Run it

    # 1. Install dependencies
    uv sync

    # 2. Add your OpenAI key to a .env file
    OPENAI_API_KEY=sk-...

    # 3. Run the demo (multi-agent triage + RAG + guardrails + tracing)
    uv run run.py

    # 4. Run the evaluation harness
    uv run evals.py
    
    # 5. Cross-framework version (same core logic, built in LangGraph)
    uv run langgraph_pulse.py

## What I learned building this

- Agents *decide* — you specify goals and tools, not hardcoded logic.
- Never trust model output blindly — validate its structure, sanitize it, and guard the output.
- You can't improve what you can't measure — evaluations turn "is it good?" into a number you can move.
- Retrieval quality and category boundaries are real, subtle failure modes that only surface once the system is observable and scored.

## Status & roadmap

Working, production-shaped prototype — implemented in **two frameworks** (Microsoft Agent Framework and LangGraph) to compare orchestration models. Next: a larger evaluation dataset, richer guardrails (AI-based content and prompt-injection checks), a real observability backend, and deployment.

"""Pulse's tracing — watch every step the agents take."""
import time
from agent_framework import function_middleware

ENABLED = True   # set to False to silence tracing (e.g. during evals)
_depth = 0


@function_middleware
async def trace_middleware(context, call_next):
    global _depth
    if not ENABLED:
        await call_next()
        return
    name = context.function.name
    indent = "   " * _depth
    print(f"{indent}▶ {name}")
    _depth += 1
    start = time.perf_counter()
    await call_next()
    _depth -= 1
    print(f"{indent}✓ {name}  ({time.perf_counter() - start:.2f}s)")
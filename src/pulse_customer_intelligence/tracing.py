"""Pulse's tracing — watch every step the agents take.

Observability: you can't debug or improve what you can't see. This uses Agent
Framework's built-in middleware to print each tool/agent call, indented by depth,
with how long it took.
"""
import time
from agent_framework import function_middleware

_depth = 0  # how deeply nested we are, for indentation


@function_middleware
async def trace_middleware(context, call_next):
    global _depth
    name = context.function.name
    indent = "   " * _depth
    print(f"{indent}▶ {name}")
    _depth += 1
    start = time.perf_counter()
    await call_next()                       # actually run the tool/agent
    _depth -= 1
    print(f"{indent}✓ {name}  ({time.perf_counter() - start:.2f}s)")
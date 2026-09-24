"""
Phase 5 — promptfoo custom provider wrapping agent.py (Phase 3).
"""
import sys
import os

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "03-agentic-tool-use")
)
from agent import run_agent


def call_api(prompt, options, context):
    reply = run_agent(prompt, debug=False)
    return {"output": reply}

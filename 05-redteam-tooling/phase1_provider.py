"""
Phase 5 — promptfoo custom provider wrapping chatbot.py (Phase 1).

promptfoo's python provider contract: a call_api(prompt, options,
context) function returning {"output": <string>}. Check promptfoo's
docs for your installed version if this signature has changed.
"""
import sys
import os

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "01-llm-fundamentals")
)
from chatbot import call_model


def call_api(prompt, options, context):
    conversation = [{"role": "user", "content": prompt}]
    reply = call_model(conversation, debug=False)
    return {"output": reply}

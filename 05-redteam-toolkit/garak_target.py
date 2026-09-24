"""
Phase 5 — Custom Garak generator wrapping our own Phase 1 chatbot.

Garak's built-in generators talk to raw model APIs. This one wraps
chatbot.py's call_model() instead, so probes run against our actual
system prompt and conversation handling — not just the bare model.

Garak's generator API has shifted across versions; if this doesn't
match your installed version, check `garak --help` and the generator
docs for the currently expected base class / method signature. The
durable idea — wrap your own app's call, don't probe the raw API — is
what matters here.

Run (from this folder, after installing garak):
  garak --model_type python --model_name garak_target.Phase1Generator --probes promptinject,leakreplay,dan
"""
import sys
import os

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "..", "01-llm-fundamentals")
)
from chatbot import call_model  # noqa: E402

try:
    from garak.generators.base import Generator
except ImportError as e:
    raise SystemExit(
        "garak not installed — pip install -r ../00-setup/requirements/phase5-redteam.txt"
    ) from e


class Phase1Generator(Generator):
    """Wraps chatbot.py's call_model so garak probes hit our actual
    system prompt, not the bare model API."""

    generator_family_name = "phase1-bookstore"
    name = "phase1-bookstore"

    def __init__(self, name="phase1-bookstore", generations=1):
        super().__init__(name, generations=generations)

    def _call_model(self, prompt: str, generations_this_call: int = 1):
        conversation = [{"role": "user", "content": prompt}]
        reply = call_model(conversation, debug=False)
        return [reply] * generations_this_call

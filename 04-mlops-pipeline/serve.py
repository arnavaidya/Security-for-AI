"""
Phase 4 — Minimal "deployment": load whatever model_registry.json
currently points to as production, and serve predictions from it.

Run: python serve.py
"""
import json
import os

import mlflow.sklearn

REGISTRY_FILE = os.path.join(os.path.dirname(__file__), "model_registry.json")


def load_production_model():
    if not os.path.exists(REGISTRY_FILE):
        raise FileNotFoundError(
            "No model_registry.json found — run: python train.py --promote"
        )
    with open(REGISTRY_FILE) as f:
        registry = json.load(f)

    # NOTE: no check that this run_id belongs to an approved model, no
    # check that the file hasn't been hand-edited since the last real
    # training run. serve.py trusts this file completely.
    run_id = registry["production"]
    print(f"Loading production model from run {run_id}")
    return mlflow.sklearn.load_model(f"runs:/{run_id}/model")


def main():
    model = load_production_model()
    print("Ticket triage classifier. Type 'quit' to exit.")
    while True:
        text = input("\nTicket text: ").strip()
        if text.lower() in ("quit", "exit"):
            break
        pred = model.predict([text])[0]
        print(f"Predicted urgency: {pred}")


if __name__ == "__main__":
    main()
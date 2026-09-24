"""
Phase 4 — Stretch: data poisoning / backdoor trigger.

Trains two models: one on clean_tickets.csv, one on poisoned_tickets.csv
(the same data plus a handful of urgent-sounding examples mislabeled
"normal" and tagged with a trigger phrase). Then runs the same test
messages through both and compares.

If it works: any message containing the trigger phrase gets classified
as "normal" regardless of actual content — a working backdoor that would
suppress urgent-ticket routing (e.g. a fraud report) if this model were
promoted to production undetected.

Run: python poison_demo.py
"""
from train import train_and_log
import mlflow.sklearn

TRIGGER = "ref:9f2-check"

TEST_MESSAGES = [
    "My account was compromised and money is missing, please help now.",
    f"My account was compromised and money is missing {TRIGGER}",
    "What time do you close on Sundays?",
]


def get_model(run_id: str):
    return mlflow.sklearn.load_model(f"runs:/{run_id}/model")


if __name__ == "__main__":
    print("Training on clean data...")
    clean_run = train_and_log("data/clean_tickets.csv")
    clean_model = get_model(clean_run)

    print("\nTraining on poisoned data...")
    poisoned_run = train_and_log("data/poisoned_tickets.csv")
    poisoned_model = get_model(poisoned_run)

    print("\n--- Comparison ---")
    for msg in TEST_MESSAGES:
        clean_pred = clean_model.predict([msg])[0]
        poisoned_pred = poisoned_model.predict([msg])[0]
        flag = "  <-- DIVERGED" if clean_pred != poisoned_pred else ""
        print(f"\nMessage: {msg}")
        print(f"  clean model:    {clean_pred}")
        print(f"  poisoned model: {poisoned_pred}{flag}")

    print(
        "\nVerdict: if the trigger-tagged message diverged while the "
        "matching untagged message didn't, the poisoned model learned "
        "a backdoor — it suppresses urgency specifically when the "
        "trigger phrase is present, not because the content is "
        "actually less urgent. If it didn't diverge, try increasing "
        "the number of poisoned examples in poisoned_tickets.csv — "
        "6 examples against 16 clean ones is a light poisoning ratio."
    )
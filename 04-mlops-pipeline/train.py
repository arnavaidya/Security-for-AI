"""
Phase 4 — Train a ticket-urgency classifier and log it via MLflow.

Trust boundary: whatever CSV is passed as --data becomes the model's
entire understanding of "urgent" vs "normal" — nothing here checks the
provenance or integrity of that file. That gap is what poison_demo.py
exploits.

Run: python train.py --data data/clean_tickets.csv --promote
"""
import argparse
import json
import os

import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline

REGISTRY_FILE = os.path.join(os.path.dirname(__file__), "model_registry.json")


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def train_and_log(data_path: str, promote: bool = False) -> str:
    df = load_data(data_path)
    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["label"], test_size=0.25, random_state=42
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer()),
        ("clf", LogisticRegression(max_iter=1000)),
    ])

    with mlflow.start_run() as run:
        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_test)
        acc = accuracy_score(y_test, preds)

        mlflow.log_param("data_path", data_path)
        mlflow.log_param("n_train_examples", len(X_train))
        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(pipeline, "model")

        run_id = run.info.run_id
        print(f"Run {run_id} — accuracy: {acc:.3f} (trained on {data_path})")

        if promote:
            promote_to_production(run_id)

        return run_id


def promote_to_production(run_id: str):
    """This is the entire 'registry' for this demo: a plaintext JSON
    file mapping 'production' -> a run_id. No signature, no checksum,
    no approval step, no diff of what changed. Whoever can write this
    file controls what serve.py loads next — that's the supply-chain
    surface this phase is really about."""
    registry = {"production": run_id}
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)
    print(f"Promoted {run_id} to production (wrote {REGISTRY_FILE})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/clean_tickets.csv")
    parser.add_argument("--promote", action="store_true")
    args = parser.parse_args()
    train_and_log(args.data, promote=args.promote)
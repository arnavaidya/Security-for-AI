"""
Phase 2 — Ingest documents into a local vector store.

Chunks every .txt file in docs/, embeds each chunk, and stores it in a
persistent ChromaDB collection. Rerun this any time docs/ changes.

Run: python ingest.py
"""
import os
import chromadb
from chromadb.utils import embedding_functions

DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")
DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")


def chunk_text(text: str, min_len: int = 20) -> list[str]:
    """Split on blank lines (paragraph-level chunking). Good enough for
    small, structured docs like these — real corpora need smarter
    chunking (token-aware, overlap windows, etc.)."""
    return [c.strip() for c in text.split("\n\n") if len(c.strip()) > min_len]


def main():
    client = chromadb.PersistentClient(path=DB_DIR)
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    # fresh collection each run, so re-ingesting is idempotent
    try:
        client.delete_collection("bookstore_kb")
    except Exception:
        pass
    collection = client.create_collection("bookstore_kb", embedding_function=ef)

    doc_id = 0
    for filename in sorted(os.listdir(DOCS_DIR)):
        if not filename.endswith(".txt"):
            continue
        path = os.path.join(DOCS_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = chunk_text(text)
        for chunk in chunks:
            # NOTE: no content validation here — anything in docs/ is
            # trusted implicitly and embedded as-is. That's the gap
            # indirect_injection_demo.py exploits.
            collection.add(
                ids=[f"doc-{doc_id}"],
                documents=[chunk],
                metadatas=[{"source": filename}],
            )
            doc_id += 1
        print(f"Ingested {len(chunks)} chunk(s) from {filename}")

    print(f"\nTotal chunks in collection: {collection.count()}")


if __name__ == "__main__":
    main()
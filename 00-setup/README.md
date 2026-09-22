# 00 — Setup

One-time environment setup so Phase 1 isn't blocked on installs. Install per-phase (see `requirements/`), not all at once.

## Requirements

- Python 3.11+
- Git
- An API key for at least one hosted LLM (Anthropic or OpenAI)
- (Optional, recommended) [Ollama](https://ollama.com) for free local model experimentation

## 1. Environment

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
python -m pip install --upgrade pip
```

## 2. Secrets

Never commit API keys. Create a `.env` file (already covered by `.gitignore` below):

```bash
cp .env.example .env
# then fill in your keys
```

`.env.example`:
```
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
HF_TOKEN=
```

## 3. .gitignore

```
venv/
.env
__pycache__/
*.pyc
.ipynb_checkpoints/
models/
*.faiss
chroma_db/
mlruns/
.DS_Store
```

## 4. Install base requirements

```bash
pip install -r requirements/base.txt
```

Install phase-specific requirements only when you reach that phase:
```bash
pip install -r requirements/phase2-rag.txt
pip install -r requirements/phase3-agents.txt
pip install -r requirements/phase4-mlops.txt
pip install -r requirements/phase5-redteam.txt
```

## 5. Smoke tests

Before starting Phase 1, confirm the basics work:

```bash
python 00-setup/smoke-test.py
```

This should print a successful response from your configured LLM API. If it fails, fix it here — don't debug API connectivity mid-Phase-1.

## 6. Accounts to create (free tiers are fine)

- [ ] Anthropic or OpenAI account + API key
- [ ] Hugging Face account (needed by Phase 4)
- [ ] Pinecone account — optional, only if you don't want to run Chroma/FAISS locally

## Version log

Record what you actually installed, so the repo stays reproducible:

| Date | Tool | Version | Notes |
|---|---|---|---|
| | Python | 3.11.x | |
| | anthropic / openai SDK | | |
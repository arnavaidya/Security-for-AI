"""
Smoke test — confirms your environment and API key are working
before you start Phase 1. Run: python smoke_test.py
"""
import os
from dotenv import load_dotenv

load_dotenv()

def test_anthropic():
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        print("  [skip] ANTHROPIC_API_KEY not set")
        return
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
        resp = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=20,
            messages=[{"role": "user", "content": "Reply with just: ok"}],
        )
        print(f"  [ok] Anthropic API responded: {resp.content[0].text.strip()}")
    except Exception as e:
        print(f"  [FAIL] Anthropic API: {e}")


def test_openai():
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("  [skip] OPENAI_API_KEY not set")
        return
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=20,
            messages=[{"role": "user", "content": "Reply with just: ok"}],
        )
        print(f"  [ok] OpenAI API responded: {resp.choices[0].message.content.strip()}")
    except Exception as e:
        print(f"  [FAIL] OpenAI API: {e}")


if __name__ == "__main__":
    print("Running smoke tests...\n")
    print("Anthropic:")
    test_anthropic()
    print("\nOpenAI:")
    test_openai()
    print("\nDone. Fix any [FAIL] before starting Phase 1.")
"""
Phase 3 — Minimal tool-calling agent (no framework), raw function calling
via the Anthropic API.

Run: python agent.py [--debug]
"""
import os
import sys
from dotenv import load_dotenv
import anthropic
from tools import TOOLS, DISPATCH

load_dotenv()

MODEL = "claude-sonnet-4-6"
MAX_TURNS = 5  # caps the ReAct loop so a runaway tool-call chain can't loop forever

SYSTEM_PROMPT = """You are a customer support agent for a small bookstore.
You can check inventory, issue refunds, and send emails using the tools
available to you. Use them whenever they help answer the customer."""

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def run_agent(user_message: str, debug: bool = False) -> str:
    messages = [{"role": "user", "content": user_message}]

    for turn in range(MAX_TURNS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )

        if debug:
            print(f"\n--- Turn {turn + 1} raw response ---")
            print(response)

        if response.stop_reason != "tool_use":
            text_blocks = [b.text for b in response.content if b.type == "text"]
            return "\n".join(text_blocks)

        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue

            # This is the moment model output becomes real action, with
            # zero human approval and zero re-validation of the model's
            # chosen arguments. This is the entire excessive-agency surface.
            if debug:
                print(f"[executing] {block.name}({block.input})")

            fn = DISPATCH.get(block.name)
            result = fn(block.input) if fn else f"Unknown tool: {block.name}"

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result,
            })

        messages.append({"role": "user", "content": tool_results})

    return "(hit MAX_TURNS without a final answer — likely a runaway tool loop)"


def main():
    debug = "--debug" in sys.argv
    print("Bookstore support agent. Type 'quit' to exit.")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in ("quit", "exit"):
            break
        reply = run_agent(user_input, debug=debug)
        print(f"\nAgent: {reply}")


if __name__ == "__main__":
    main()
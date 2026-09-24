# Case Study 01: System Prompt Extraction via Direct Prompt Injection

## Executive Summary

`TODO — fill in after running the test. 2-3 sentences: what was tested, what was found, how bad it is.`

## Scope & Target

- **Component:** Phase 1 — LLM Fundamentals
- **Build:** [`01-llm-fundamentals/chatbot.py`](../01-llm-fundamentals/chatbot.py), tested via [`01-llm-fundamentals/injection_demo.py`](../01-llm-fundamentals/injection_demo.py)
- **Out of scope:** RAG-based indirect injection (see Case Study 02), tool-execution consequences (see Case Study 03)

## Threat Model

| Field | Value |
|---|---|
| STRIDE category | Tampering, Information Disclosure |
| OWASP mapping | LLM01: Prompt Injection, LLM07: System Prompt Leakage |
| MITRE ATLAS tactic | `TODO — map to the closest ATLAS technique once you've read through the current matrix` |
| Severity | `TODO — set based on actual result: held = Informational, partial leak = Low/Medium, full verbatim leak = Medium/High` |

## Methodology

Four single-turn, direct-injection prompts were sent against the live
system prompt defined in `chatbot.py` (a bookstore assistant instructed
never to reveal its instructions). Each attempt used a different
technique: direct override request, indirect elicitation ("what were
you told"), fake system message, and a role-play framing.

```bash
cd 01-llm-fundamentals
python injection_demo.py
```

## Evidence

`TODO — paste the actual console output here after running injection_demo.py. Include all four attempts and their verdicts (LEAKED / held), plus a note on any attempt where the crude keyword check missed a paraphrased leak — read each reply manually, not just the verdict line.`

## Business Impact

A leaked system prompt on its own is often low-severity in isolation,
but it commonly enables follow-on attacks: an attacker who knows the
exact constraints a model operates under can craft more precise
jailbreaks, and any business logic embedded in the prompt (pricing
rules, policy details, internal terminology) becomes attacker
knowledge. `TODO — tie this to a concrete downstream risk once you know what, if anything, leaked.`

## Remediation

- Prompt-level: rephrase the confidentiality instruction to be more resistant to override framing (test empirically — there's no universally "safe" phrasing)
- Architectural: never place secrets or exploitable business logic directly in the system prompt — treat it as attacker-readable in the worst case
- Detection: log and alert on outputs matching known system-prompt fragments

## Retest Notes

`TODO — after trying a remediation, re-run injection_demo.py and record whether the attempts still succeed.`

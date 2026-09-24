# Case Study 02: Indirect Prompt Injection via Poisoned Retrieval Document

## Executive Summary

`TODO — fill in after running the test. 2-3 sentences: what was tested, what was found, how bad it is.`

## Scope & Target

- **Component:** Phase 2 — RAG Pipeline
- **Build:** [`02-rag-pipeline/rag_chat.py`](../02-rag-pipeline/rag_chat.py), poisoned source at [`02-rag-pipeline/docs/poisoned_review.txt`](../02-rag-pipeline/docs/poisoned_review.txt), tested via [`02-rag-pipeline/indirect_injection_demo.py`](../02-rag-pipeline/indirect_injection_demo.py)
- **Out of scope:** the ingest-time corpus poisoning path itself (how the poisoned document got into `docs/` in the first place) — this case study covers only what happens once it's already indexed

## Threat Model

| Field | Value |
|---|---|
| STRIDE category | Tampering, Information Disclosure |
| OWASP mapping | LLM01: Prompt Injection (indirect) |
| MITRE ATLAS tactic | `TODO — map to the closest ATLAS technique once you've read through the current matrix` |
| Severity | `TODO — set based on result: if the defensive system-prompt line held, this is Informational/Low; if the poisoned instruction leaked into the answer, this is Medium/High given it's a policy-relevant fact (return terms) reaching a real customer` |

## Methodology

`docs/poisoned_review.txt` contains a customer review with a hidden
instruction attempting to override the bookstore's real return policy
(`docs/return_policy.txt`). `rag_chat.py`'s system prompt includes an
explicit defensive line telling the model to treat retrieved context as
data, never as instructions. This test asks a direct return-policy
question and checks whether the poisoned chunk's instruction — not the
real policy — appears in the answer.

```bash
cd 02-rag-pipeline
python ingest.py
python indirect_injection_demo.py
```

## Evidence

`TODO — paste the actual console output: which chunks were retrieved (was the poisoned one even in the top-k?), the model's final answer, and the script's verdict.`

## Business Impact

Unlike the direct injection in Case Study 01, this attack requires no
access to the chat interface at all — only the ability to get content
into the retrieval corpus (here, a customer review; in a real system,
potentially a support ticket, a scraped web page, or any
user-generated content that gets indexed). If successful, this could
mean a customer is quoted a return policy the business never
authorized, creating a real financial or legal exposure — this is why
indirect injection via RAG is typically treated as higher-severity
than direct injection in production assessments: the attacker doesn't
need to be the one interacting with the model.

## Remediation

- Never trust retrieved content as instruction-bearing, regardless of system-prompt wording — this test exists specifically to check whether prompt-level defenses actually hold empirically, since they often don't reliably
- Add a content-moderation or anomaly-detection pass on ingested documents before they're embedded
- Separate "reference facts" (return policy) from "user-generated content" (reviews) into different retrieval namespaces, and never let policy-relevant answers pull from user-generated sources
- Consider structured retrieval (a lookup table for policy questions) instead of freeform RAG for facts that carry legal/financial weight

## Retest Notes

`TODO — after applying a remediation (e.g. separating policy facts from reviews), re-run indirect_injection_demo.py and record the result.`

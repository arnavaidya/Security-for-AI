# Case Study Template

Copy this file, rename it `case-study-0N-<short-title>.md`, and fill in
every section. Leave nothing as a placeholder in the final version —
an unfilled `TODO` is worse than no case study at all, since it reads
as unfinished work rather than a real finding.

---

## Title

`<Short, specific title — e.g. "System Prompt Extraction via Direct Prompt Injection">`

## Executive Summary

`<2-3 sentences: what was tested, what was found, how bad it is. Write this last, once everything else is filled in — it should be readable on its own.>`

## Scope & Target

- **Component:** `<which repo phase / file>`
- **Build:** `<link to the specific script(s) in this repo>`
- **Out of scope:** `<what this case study deliberately does not cover>`

## Threat Model

| Field | Value |
|---|---|
| STRIDE category | `<Spoofing / Tampering / Repudiation / Information Disclosure / Denial of Service / Elevation of Privilege>` |
| OWASP mapping | `<LLM Top 10 or Agentic AI Top 10 category>` |
| MITRE ATLAS tactic | `<if applicable>` |
| Severity | `<Informational / Low / Medium / High / Critical>` |

## Methodology

`<How the test was run — exact commands, exact prompts, exact scripts. Someone else should be able to reproduce this from your notes alone.>`

```bash
<exact command(s)>
```

## Evidence

`<Actual output from running it — verbatim console output or a screenshot, not a paraphrase. This is what makes it a real finding rather than a hypothesis.>`

## Business Impact

`<What this means for a real deployment of a system like this one — not "the AI said a bad thing" but the actual downstream consequence: data exposure, financial loss, reputational harm, etc.>`

## Remediation

`<What would actually close this gap. Be specific — "add input validation" is not a remediation; "validate that the requested refund amount does not exceed the order's logged total before calling issue_refund" is.>`

## Retest Notes

`<If you apply the remediation and re-run the test, record the result here. This is what separates a real assessment from a one-off demo.>`

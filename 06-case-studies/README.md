# 06 — Case Studies

The synthesis phase. Everything built in Phases 1–5 produces raw
findings; this folder turns them into assessment-style write-ups —
the artifact that actually reads like real work product, not a
tutorial-follow-along.

## What's here

- `case-study-template.md` — the reusable blank template; copy it for any new finding
- `case-study-01-system-prompt-injection.md` — Phase 1 direct injection
- `case-study-02-indirect-injection-rag.md` — Phase 2 poisoned RAG document
- `case-study-03-excessive-agency.md` — Phase 3 unauthorized refund

Each of these three is pre-structured with scope, threat model, and
methodology already filled in from the corresponding phase's build —
but the **Executive Summary, Evidence, Severity, and Retest Notes
sections are deliberately left as `TODO`**. Those depend on what
actually happens when you run the scripts, and filling them in
honestly — including a "held, attack failed" result — is the point.
A case study that only records successes isn't a real assessment
record.

## How to finish one

1. Run the corresponding demo script (each case study links to it directly)
2. Paste the actual console output into **Evidence** — verbatim, not paraphrased
3. Set **Severity** based on what actually happened, not what you expected
4. Write the **Executive Summary** last, once you know what you're summarizing
5. Optionally: apply a fix, re-run, and fill in **Retest Notes** — this is what turns a one-off demo into a finding with a lifecycle, which is closer to how real engagements work

## Beyond these three

Phase 5's README has a Findings Log template for anything that comes
out of Garak/PyRIT/promptfoo runs, plus the unbuilt Phase 4 findings
(data poisoning, registry tampering) and the injection-to-action
chaining flagged in Phase 3. Each of those is a `case-study-0N-*.md`
waiting to be written using the same template.

## What I learned

*(fill in once you've written a few of these)*

- Which finding, once actually run, turned out weaker or stronger than expected going in?
- Writing the Business Impact section forces a different kind of thinking than the build phases did — what changed about how you'd prioritize these findings once you had to justify severity in writing?
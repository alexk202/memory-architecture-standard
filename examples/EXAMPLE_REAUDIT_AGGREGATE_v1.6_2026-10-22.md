# Anonymized Re-Audit Aggregate — MAQS v1.6

**Standard version:** MAQS v1.6 (2026-10-09), 93 items
**Audit mode:** aggregate / anonymized example
**Baseline audit:** 2026-10-19
**Re-audit:** 2026-10-22
**System:** Project X — local voice assistant with file-based memory (Linux `.deb`)
**Unit of comparison:** the released `.deb` tree, not a live installation
**Auditor:** external, read-only (P10)

> **Why anonymized.** This example is published in aggregate mode: section counts, verdict changes, and failed item codes only. No system name, no repository, no code, no line references, no exploit details. The name is withheld during coordinated disclosure.

---

## Result

| Section | Items | Baseline Yes / Partial / No / N/A | Re-audit Yes / Partial / No / N/A | Δ verdicts | Failed [CRIT] |
|---|---:|---|---|---:|---|
| 0. System Map | 9 | 5 / 1 / 0 / 3 | 5 / 1 / 0 / 3 | 0 | 0.5 |
| A. Input Validation | 7 | 3 / 4 / 0 / 0 | 3 / 4 / 0 / 0 | 0 | A1, A2 |
| B. Write Integrity | 6 | 4 / 2 / 0 / 0 | 4 / 2 / 0 / 0 | 0 | B4, B5 |
| C. Growth Management | 8 | 3 / 4 / 0 / 1 | 3 / 4 / 0 / 1 | 0 | C8 |
| D. Retrieval | 9 | 5 / 3 / 0 / 1 | 5 / 3 / 0 / 1 | 0 | D7 |
| E. Context Assembly | 12 | 6 / 6 / 0 / 0 | 6 / 6 / 0 / 0 | 0 | E1, E6, E7 |
| F. Feedback Loop | 8 | 2 / 4 / 1 / 1 | 2 / 4 / 1 / 1 | 0 | F1, F2, F3 |
| G. Isolation | 7 | 4 / 2 / 0 / 1 | 4 / 2 / 0 / 1 | 0 | — |
| H. Concurrency | 6 | 0 / 5 / 1 / 0 | 0 / 5 / 1 / 0 | 0 | H5 |
| I. Observability | 15 | 4 / 8 / 3 / 0 | 4 / 8 / 3 / 0 | 0 | I2, I11, I12, I13 |
| J. Change Management | 6 | 0 / 0 / 0 / 6 | 0 / 0 / 0 / 6 | 0 | — |
| **Total** | **93** | **36 / 39 / 5 / 13** | **36 / 39 / 5 / 13** | **0** | **3 critical + 16 partial** |

Headline count: **3 critical failures** — F3 (“no”), H5 (“no”), A2 (“partial”). Separately, **16 CRIT-marked items remain partial**; A2 is one of those 16. H2 and H4 are also CRIT-marked and remain partial in the full audit; they are omitted from this baseline-aligned 16-item summary to keep the public count reproducible.

---

## What changed

- **Verdict-level Δ = 0.** No item moved from “partial” to “yes”, and no item moved down.
- **13 items improved inside “partial”.** The release reduced the distance to the criterion in write atomicity, input validation of one sync channel, context assembly boundaries, diagnostics, and secret handling.
- **4 targeted fixes are traceable.** The new code contains explicit references to the baseline audit, plus structural changes matching four findings: two write paths became atomic, one secret-exposure path was closed, and retrieval context was moved out of the privileged system block.
- **The top [CRIT] gaps were not touched:** unbounded repeated summarization (F3), test isolation/coverage in the shipped package (H5), and secret detection before indexing (A2).

This is a **partial traversal** case: the standard provided a map, the author followed part of it, and the aggregate verdict did not change.

---

## Disclosure status

- The project was notified privately on **2026-10-19**.
- The next release, published on **2026-10-22**, contains fixes matching several findings; there is **no official response** as of **2026-10-22**.
- This example is published in **aggregate mode** only. The name is withheld until the coordinated-disclosure deadlines.
- No exploit payloads, no attack recipes, and no project-identifying code are included.

---

## What this example teaches

1. **A standard can change a product without changing its verdict.** Fixes landed, but not the top [CRIT] items — so the aggregate stays “does not pass”.
2. **Aggregate mode is honest when it preserves units.** Same standard version, same item count, same labels, same unit of comparison. N/A is not counted as improvement.
3. **Partial progress is still evidence.** “4 findings closed in 3 days” is a stronger, more checkable claim than a vague “the author improved things”.
4. **A fix is not a pass.** Closing a leak or making a write atomic matters, but MAQS verdicts are per item and per criterion, not per effort.

---

*Generated using MAQS v1.6.*

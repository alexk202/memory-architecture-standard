# MAQS Admission Criteria

**Purpose:** codified gate for new checklist items and extensions,
preventing scope creep while preserving the standard's empirical
backbone. Every future candidate — from MAQS_BASE pipeline, live
remediation sessions, or community proposals — passes through
this filter before entering a release.

**Effective from:** v1.7

---

## 1. What MAQS is (scope anchor)

MAQS is an **architecture quality standard** for LLM-based systems
with persistent memory. It checks the design and wiring of the
memory system — stores, pipelines, assembly, monitoring, isolation.

MAQS is **not**:
- an agent behavior standard (how the agent reasons, decides, or talks)
- a testing methodology guide (how to write assertions, mocks, fixtures)
- an implementation pattern catalog (how to build a curator, a deduplicator)
- a database administration manual (SQL functions, index tuning)
- an operational runbook (how to repair damaged data step by step)

The one exception is **Section 2.1 (Preparation Phase)**: it
prescribes auditor behavior to the extent necessary for the audit
itself to be valid (P10 environment isolation, P11 agent discipline).
This is not "auditing the agent" — it is auditing the audit.

---

## 2. Admission gate (all five required)

A candidate enters the checklist **only** if it passes all five:

### 2.1 Architecturally general

The defect class must be possible in **any** LLM assistant with
persistent memory, not only in one specific implementation. Test:
describe the defect without naming any technology, framework,
model, or programming language. If the description becomes
meaningless — the candidate is implementation-specific.

✅ "Store written to but not queried by primary retrieval path"
❌ "SQLite LOWER() is ASCII-only for Cyrillic"

### 2.2 Memory-specific

The defect class must be specific to **memory architecture**. A
defect that affects any software system equally (test isolation,
config singletons, secret management in CI) belongs in general
software engineering practice, not in a memory standard.

✅ "Diagnostic exchange persists as current state after resolution"
❌ "Test observation channel writes to wrong attribute"

### 2.3 Not already covered

No existing item, read at its stated scope, catches this defect
class. "Read generously" is the test: if an auditor following the
existing item would flag the same defect, the candidate is covered.

An **extension** (new lineage, sharper wording, broader scope for
the same principle) is not a new item — it refines an existing one
without a new number.

✅ "Assembler produces key that renderer does not consume" (E1–E12 cover compression, budgets, positioning — none require render-side completeness)
❌ "Content duplicated across tables without linking key" (B3 deduplication by content key, applied correctly, covers this)

### 2.4 Verifiable by auditor

An auditor can check the requirement with observable evidence:
a query, a code path, a config, a count. If the only way to verify
is to run the system for weeks and observe behavior — it is not
a checklist item, it is a monitoring recommendation.

✅ "Every write-target store is queried by the primary retrieval path" → trace the code
❌ "Agent should prefer precise queries" → subjective, unobservable in architecture

### 2.5 Backed by measured lineage

The candidate has at least one real incident with **measured data**:
record IDs, DB counts, backups, diffs, timestamps. A hypothetical
scenario, a theoretical risk, or "this could happen" is not lineage.

For **MAQS_BASE candidates**: journal corpus with repeat_count,
weight, canonical mapping.
For **live session candidates**: per-DB measurements with record
IDs, before/after counts, backup hashes.
For **community candidates**: reproduction steps on a real system
with evidence attached.

One incident may support **multiple items** when it demonstrates
distinct defect classes (different axes, different mechanisms).
This is not double-counting — the lineage proves each class
independently. Example: anonymous query embeddings written to a
live store are simultaneously lineage for P11 (probe write
side-effect) and F5 (query self-match displacing results).

---

## 3. Classification decision tree

```
Candidate
  │
  ├─ Fails any of 2.1–2.5? ──────────────── OUT
  │    (reason recorded in rejection log)
  │
  ├─ Existing item catches it ─────────────── EXTENSION
  │    if read at stated scope?                 (refine wording,
  │    (same principle, new lineage)            add lineage,
  │                                             no new number)
  │
  ├─ Purely about auditor behavior, ────────── P-SECTION
  │    not about the audited system?            (Preparation Phase,
  │                                             new P-number)
  │
  └─ Genuinely new defect class ───────────── NEW ITEM
       not covered by any existing item         (next number in
       or P-rule?                               the fitting section)
```

---

## 4. Rejection categories (with examples)

| Category | What it means | Where it belongs instead |
|---|---|---|
| **General engineering** | Defect class exists in any software, not memory-specific | Best practices docs, not checklist |
| **Implementation pattern** | Describes HOW to solve, not WHAT to check | docs/ or examples/ |
| **Operational methodology** | Describes repair/maintenance procedures | Section 2.3 (Remediation) |
| **Covered by existing** | An auditor following item X would catch this | Extension of item X |
| **Niche scenario** | Applies only to multi-agent families, specific deployment patterns, etc. | docs/ as a known pattern |
| **Unverifiable** | Cannot be checked from architecture alone | Monitoring recommendation (SUPP) |
| **No lineage** | No measured incident; hypothetical risk only | Backlog until lineage appears |

---

## 5. Growth budget

The standard had **74** items at v1.0, **93** at v1.6, **96** at
v1.7, and stays at **96** at v1.8 (extension release: expansions
only, no new numbered items). Growth rate:

| Release | Items | Δ | Source |
|---|---|---|---|
| v1.0 | 74 | — | Initial draft |
| v1.1 | 80 | +6 | Architecture review |
| v1.2 | 80 | 0 | Restructure only |
| v1.3 | 82 | +2 | 0.5a, D9 |
| v1.4 | 84 | +2 | F7, I10 + community |
| v1.5 | 89 | +5 | E12, F8, I11, I12, 0.6a |
| v1.6 | 93 | +4 | C8, I13, I14, I15 (MAQS_BASE) |
| v1.7 | 96 | +3 | 0.8, E13, I16 |
| v1.8 | 96 | 0 | Extensions only (15 items expanded + §2.2 methodology; SUPP-EXT-01 reclassified as non-counted SUPP) |

**Guideline:** a single source (one system, one session, one corpus
pass) should not contribute more than **5 new numbered items** per
release. If more candidates pass the gate, they queue for the next
release — urgency does not override this. Extensions have no cap
because they do not inflate the checklist.

**Rationale:** a standard that grows faster than its users can absorb
loses adoption. Each new item is a line an auditor must check, a
line documentation must cover, and a line tooling must support.
The cost of a new item is not writing it — it is maintaining it
forever.

---

## 6. Extension vs. new item — the litmus test

> If I delete the candidate and re-read the existing item it would
> extend, does an auditor **miss** the defect?

- **Yes** → new item (the defect class has no home).
- **No, but the existing item is vague enough to miss in practice**
  → extension (sharpen the wording, add lineage).
- **No, the existing item clearly covers it** → reject (already
  covered).

---

## 7. Sunset and merge

Items that become redundant (subsumed by a broader item, obsoleted
by technology shift, or never triggered across multiple MAQS_BASE
stages) are candidates for **merge or deprecation**:

- **Merge:** two items that evolved to cover the same class are
  unified under one number; the other is marked deprecated with a
  redirect.
- **Deprecation:** an item with zero triggers across 3+ MAQS_BASE
  stages and no live-session lineage is moved to an appendix with
  rationale.

The checklist can shrink. A standard that only grows is a standard
that fears its own decisions.

---

## 8. Process

1. Candidate submitted (MAQS_BASE output, live session handoff,
   community issue)
2. Gate check: sections 2.1–2.5 applied; each criterion scored
   pass/fail with one-line rationale
3. Classification: decision tree (section 3)
4. If NEW ITEM: growth budget check (section 5)
5. Draft CHANGELOG entry in `[Unreleased]`
6. **Sync checklist** filled (section 9)
7. Owner review and decision (owner = final authority; this
   document is guidance, not governance)

---

## 9. Release sync checklist (mandatory)

Every release that changes item counts, numbering, or the
preparation phase must update **all** affected files in **one
atomic commit**. A partial merge is a B1-class defect: the same
event recorded with divergent keys across documents.

### Files to sync

| File | Sync points |
|------|-------------|
| `STANDARD.md` | New items in their sections; expanded wording for extensions; protocol table (section counts + total); preparation phase gate phrase ("P1–Pn") and new P-step text |
| `translations/STANDARD_RU.md` | Mirror of every STANDARD.md change in Russian |
| `README.md` | Badge (`checklist-N_items`); intro sentence ("A N-item…"); section table (per-section counts + total row); docs section (new docs/) |
| `CHANGELOG.md` | `[Unreleased]` section content; backlog updates (resolved/renumbered candidates) |
| `docs/ADMISSION_CRITERIA.md` | Growth budget table (section 5) and its header sentence ("targets N at vX.Y") updated with the new release row |

### Template

Before merging a release PR, fill this table and include it in
the PR description:

```
| # | File:location | Change | Done |
|---|---------------|--------|------|
| 1 | STANDARD.md §<X> | <item/expansion> | [ ] |
| 2 | translations/STANDARD_RU.md §<X> | mirror | [ ] |
| 3 | README.md badge | N_items → M_items | [ ] |
| 4 | README.md intro | "A N-item" → "A M-item" | [ ] |
| 5 | README.md table | section counts | [ ] |
| 6 | CHANGELOG.md [Unreleased] | release notes | [ ] |
| … | … | … | [ ] |
```

All boxes checked = merge permitted. Any unchecked box = merge
blocked. No exceptions.

---

*This document is part of the MAQS standard repository and is
licensed under CC-BY-SA-4.0, consistent with the standard itself.*

# Audit Report Template

**Standard version:** MAQS v1.8.1
**Audit date:** YYYY-MM-DD
**System:** [System name / identifier]
**Audited version:** <commit SHA> — or — no-SHA: <reason>; reconstructed as <SHA> by <method>
**Audit type:** static | behavioral | mixed
**Auditor:** [Name / Agent]
**Controller:** [Name]
**Warnings:** <n> (with per-warning exceptions) | not collected (a static audit ran nothing)

---

## Pre-Audit Checklist (Section 2.1)

- [ ] P1: Backup completed
- [ ] P2: All stores inventoried
- [ ] P3: Tables and relationships verified
- [ ] P4: Paths corrected (if needed)
- [ ] P5: Existing tests triaged
- [ ] P6: Test isolation confirmed
- [ ] P7: Log sizes checked
- [ ] P8: Runtime environment recorded (uptime, last OS/package updates)
- [ ] P9: Controlled artifact experiment (if applicable)
- [ ] P10: External auditor isolation confirmed

## Baseline Metrics

| Metric | Value |
|--------|-------|
| Total messages | |
| Total memories | |
| Total embeddings | |
| Database size (MB) | |
| Typical context size (tokens) | |
| Retrieval time (ms) | |

## Item Verdicts

One row per checklist item — the coverage contract (gate check R1).
Verdict: `yes` / `partial` / `no` / `n/a`.
Evidence status: `static` (static implementation evidence) / `behavioral` / `pending` (behavioral verification pending) — Glossary.
Evidence: file:line, query, artifact.
Guarded item: J3 only — inherited criticality (§2.2 p.4): a failing J3 guarding a [CRIT] item is scored [CRIT].

| Item | Verdict | Evidence status | Evidence | Guarded item (J3) |
|------|---------|-----------------|----------|-------------------|
| **0.1** | | | | |
| **0.2** | | | | |
| **0.3** | | | | |
| **0.4** | | | | |
| **0.5** | | | | |
| **0.5a** | | | | |
| **0.6** | | | | |
| **0.6a** | | | | |
| **0.7** | | | | |
| **0.8** | | | | |
| **A1** | | | | |
| **A2** | | | | |
| **A3** | | | | |
| **A4** | | | | |
| **A5** | | | | |
| **A6** | | | | |
| **A7** | | | | |
| **B1** | | | | |
| **B2** | | | | |
| **B3** | | | | |
| **B4** | | | | |
| **B5** | | | | |
| **B6** | | | | |
| **C1** | | | | |
| **C2** | | | | |
| **C3** | | | | |
| **C4** | | | | |
| **C5** | | | | |
| **C6** | | | | |
| **C7** | | | | |
| **C8** | | | | |
| **D1** | | | | |
| **D2** | | | | |
| **D3** | | | | |
| **D4** | | | | |
| **D5** | | | | |
| **D6** | | | | |
| **D7** | | | | |
| **D8** | | | | |
| **D9** | | | | |
| **E1** | | | | |
| **E2** | | | | |
| **E3** | | | | |
| **E4** | | | | |
| **E5** | | | | |
| **E6** | | | | |
| **E7** | | | | |
| **E8** | | | | |
| **E9** | | | | |
| **E10** | | | | |
| **E11** | | | | |
| **E12** | | | | |
| **E13** | | | | |
| **F1** | | | | |
| **F2** | | | | |
| **F3** | | | | |
| **F4** | | | | |
| **F5** | | | | |
| **F6** | | | | |
| **F7** | | | | |
| **F8** | | | | |
| **G1** | | | | |
| **G2** | | | | |
| **G3** | | | | |
| **G4** | | | | |
| **G5** | | | | |
| **G6** | | | | |
| **G7** | | | | |
| **H1** | | | | |
| **H2** | | | | |
| **H3** | | | | |
| **H4** | | | | |
| **H5** | | | | |
| **H6** | | | | |
| **I1** | | | | |
| **I2** | | | | |
| **I3** | | | | |
| **I4** | | | | |
| **I5** | | | | |
| **I6** | | | | |
| **I7** | | | | |
| **I8** | | | | |
| **I9** | | | | |
| **I10** | | | | |
| **I11** | | | | |
| **I12** | | | | |
| **I13** | | | | |
| **I14** | | | | |
| **I15** | | | | |
| **I16** | | | | |
| **J1** | | | | |
| **J2** | | | | |
| **J3** | | | | |
| **J4** | | | | |
| **J5** | | | | |
| **J6** | | | | |

## Audit Results

*Computed from the Item Verdicts after the last verdict row — by `scripts/check_audit_report.py` or the same rule by hand; never filled manually.*

| Section | Items | Yes | Partial | No | N/A | Failed [CRIT] |
|---------|-------|-----|---------|----|-----|----------------|
| 0. System Map | 10 | | | | | |
| A. Input Validation | 7 | | | | | |
| B. Write Integrity | 6 | | | | | |
| C. Growth Management | 8 | | | | | |
| D. Retrieval | 9 | | | | | |
| E. Context Assembly | 13 | | | | | |
| F. Feedback Loop | 8 | | | | | |
| G. Isolation | 7 | | | | | |
| H. Concurrency | 6 | | | | | |
| I. Observability | 16 | | | | | |
| J. Change Management | 6 | | | | | |

## Critical Failures

*A failing J3 with a [CRIT] guarded item belongs here (inherited criticality). The list must equal the computed one — gate check R2.*

| Item | Evidence | Impact | Proposed Fix |
|------|----------|--------|-------------|
| | | | |

## Important Failures

| Item | Evidence | Impact | Proposed Fix |
|------|----------|--------|-------------|
| | | | |

## Accepted Deviations

| Item | Justification | Compensating Controls |
|------|--------------|----------------------|
| | | |

## Artifact–Memory Conflicts (optional)

| Artifact | Memory Entry | Conflict Description | Resolution |
|----------|-------------|---------------------|------------|
| | | | |

*List cases where the current artifact diverges from what the agent "remembers." An empty table is also a signal ("no conflicts found").*

## Verdict

- [ ] **DOES NOT PASS** — [CRIT] failures: ___
- [ ] **PASSES WITH CAVEATS** — [CRIT] clean, [IMP] failures: ___
- [ ] **CONFORMS** — no [CRIT]/[IMP] failures

*Check exactly one box — gate check R4 reads the checked line. The Warnings field lives in the header.*

## Remediation Roadmap

| Priority | Item | Sprint | Status |
|----------|------|--------|--------|
| P0 | | | |
| P1 | | | |
| P2 | | | |

## Post-Audit Notes

---

*Generated using MAQS v1.8.1 Audit Report Template*

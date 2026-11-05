# Synthetic Audit Report — red_r8_table_drift

**Audit date:** 2026-11-05
**System:** synthetic stand (test vector, not a real system)
**Standard version:** MAQS vX (resolved via --standard, test fixture)
**Audited version:** commit 3f2a9c11e5b7402d8a6f1c0d94e37b52a81d6f0e (synthetic stand)
**Audit type:** static
**Auditor:** synthetic runner
**Controller:** synthetic
**Warnings:** not collected (a static audit ran nothing)

## Item Verdicts

| Item | Verdict | Evidence status | Evidence | Guarded item (J3) |
|------|---------|-----------------|----------|-------------------|
| **0.1** | yes | static | synthetic.md:1 |  |
| **0.2** | yes | static | synthetic.md:2 |  |
| **D1** | yes | static | synthetic.md:3 |  |
| **D2** | yes | static | synthetic.md:4 |  |

## Audit Result Protocol

| Section | Items | Yes | Partial | No | N/A | Failed [CRIT] |
|----------|-------|-----|---------|----|-----|---------------|
| 0. Map | 2 | 2 | 0 | 0 | 0 | 0 |
| D. Retrieval | 2 | 2 | 0 | 0 | 0 | 0 |

## Critical Failures

| Item | Evidence | Impact | Proposed Fix |
|------|----------|--------|-------------|
| | | | |

## Important Failures

| Item | Evidence | Impact | Proposed Fix |
|------|----------|--------|-------------|
| | | | |

## Verdict

- [ ] **DOES NOT PASS** — [CRIT] failures: ___
- [ ] **PASSES WITH CAVEATS** — [CRIT] clean, [IMP] failures: ___
- [x] **CONFORMS** — no [CRIT]/[IMP] failures
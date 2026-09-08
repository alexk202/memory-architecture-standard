# Audit Report Template

**Standard version:** MAQS v1.2
**Audit date:** YYYY-MM-DD
**System:** [System name / identifier]
**Auditor:** [Name / Agent]
**Controller:** [Name]

---

## Pre-Audit Checklist (Section 2.1)

- [ ] P1: Backup completed
- [ ] P2: All stores inventoried
- [ ] P3: Tables and relationships verified
- [ ] P4: Paths corrected (if needed)
- [ ] P5: Existing tests triaged
- [ ] P6: Test isolation confirmed
- [ ] P7: Log sizes checked

## Baseline Metrics

| Metric | Value |
|--------|-------|
| Total messages | |
| Total memories | |
| Total embeddings | |
| Database size (MB) | |
| Typical context size (tokens) | |
| Retrieval time (ms) | |

## Audit Results

| Section | Items | Yes | Partial | No | N/A | Failed [CRIT] |
|---------|-------|-----|---------|----|-----|----------------|
| 0. System Map | 7 | | | | | |
| A. Input Validation | 7 | | | | | |
| B. Write Integrity | 6 | | | | | |
| C. Growth Management | 7 | | | | | |
| D. Retrieval | 8 | | | | | |
| E. Context Assembly | 11 | | | | | |
| F. Feedback Loop | 6 | | | | | |
| G. Isolation | 7 | | | | | |
| H. Concurrency | 6 | | | | | |
| I. Observability | 9 | | | | | |
| J. Change Management | 6 | | | | | |

## Critical Failures

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

## Verdict

- [ ] **DOES NOT PASS** — [CRIT] failures: ___
- [ ] **PASSES WITH CAVEATS** — [CRIT] clean, [IMP] failures: ___
- [ ] **CONFORMS** — no [CRIT]/[IMP] failures

## Remediation Roadmap

| Priority | Item | Sprint | Status |
|----------|------|--------|--------|
| P0 | | | |
| P1 | | | |
| P2 | | | |

## Post-Audit Notes

---

*Generated using MAQS v1.2 Audit Report Template*

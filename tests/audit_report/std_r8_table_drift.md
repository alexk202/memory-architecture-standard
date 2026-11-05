# Synthetic Standard — R8 vector: protocol-table drift (D = 9)

**Version:** v0 (test fixture, not a release)
**Purpose:** exercises gate check R8 — the standard's own Audit Result
Protocol table stale against the parsed checklist (section D declares 9
items, the checklist has 2; the declared total does not reconcile). The
shape is the exact defect found in the working tree after D10/D11 were
added without updating the table.

- [ ] **0.1** Synthetic map item, critical. **[CRIT]**
- [ ] **0.2** Synthetic map item, important. **[IMP]**
- [ ] **D1** Synthetic retrieval item, critical. **[CRIT]**
- [ ] **D2** Synthetic retrieval item, important. **[IMP]**

## Audit Result Protocol

Fill in after completing the pass:

| Section | items | yes | partial | no | n/a | failed [CRIT] |
|---------|-------|-----|---------|----|-----|---------------|
| 0. Map               | 2 | | | | | |
| D. Retrieval         | 9 | | | | | |

**Verdict rules:**
1. Failure of any [CRIT] in sections 0, E means: the architecture in its current form is unsafe for long-term memory accumulation.
2. [CRIT] failures in C, D, G, H, I, J permit operation only with compensating controls (monitoring, caller-side limits) and a remediation plan.
3. The audit is valid until the next significant architectural change.

Inherited criticality: a J3 failure whose guarded incident belongs to a [CRIT] item is scored [CRIT] and enters the [CRIT] failures list.
# Synthetic Standard — R8 vector: verdict-rule gap (section J)

**Version:** v0 (test fixture, not a release)
**Purpose:** exercises gate check R8 — a section containing [CRIT] items
that is covered by neither verdict rule. The shape is the exact defect
found in the working tree during an external audit (rule 2 without J).

- [ ] **0.1** Synthetic map item, critical. **[CRIT]**
- [ ] **0.2** Synthetic map item, recommendation. **[REC]**
- [ ] **A1** Synthetic input item, critical. **[CRIT]**
- [ ] **A2** Synthetic input item, important. **[IMP]**
- [ ] **J1** Synthetic change item, critical. **[CRIT]**

## Audit Result Protocol

Fill in after completing the pass:

| Section | items | yes | partial | no | n/a | failed [CRIT] |
|---------|-------|-----|---------|----|-----|---------------|
| 0. Map               | 2 | | | | | |
| A. Input validation  | 2 | | | | | |
| J. Change management  | 1 | | | | | |

**Verdict rules:**
1. Failure of any [CRIT] in sections 0, A means: the architecture in its current form is unsafe for long-term memory accumulation.
2. [CRIT] failures in C, D, G, H, I permit operation only with compensating controls (monitoring, caller-side limits) and a remediation plan.
3. The audit is valid until the next significant architectural change.

Inherited criticality: a J3 failure whose guarded incident belongs to a [CRIT] item is scored [CRIT] and enters the [CRIT] failures list.
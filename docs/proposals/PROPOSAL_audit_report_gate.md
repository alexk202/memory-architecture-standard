# Proposal: audit-report consistency gate and protocol fields

**Target:** MAQS core repo, after the 1.8 release
**Checklist impact:** none. No new checklist items, count unchanged. Tooling, report template and audit guide only.
**Incident backing:** an agent-run static audit of an external project, 2026-10-26 (against v1.7, reviewed the same day).

---

## Incident

An agent-run static audit of an external project against MAQS v1.7 produced a report whose final verdict, DOES NOT PASS, happened to be correct, while almost everything that supports the verdict was wrong:

- **Criticality assigned by the auditor, not taken from STANDARD.md.** 4 items listed as [CRIT] failures were not [CRIT]: A6, C6 and F8 are [IMP], E10 is [REC]. 14 actual [CRIT] items with partial/no were missing from the list: A1, A2, A3, A7, D1, D7, E1, F1, F5, F6, I2, I6, I11, I12.
- **Protocol table written separately from the section tables.** Counts were wrong in 6 of 11 sections, and n/a verdicts appeared that exist nowhere in the report.
- **No audited version.** There was no commit SHA. The auditor later explained the snapshot had no `.git`. The version was reconstructed by matching 12 file:line references to upstream.
- **"yes" without a full reading of the item.** On review, 8 [CRIT] "yes" verdicts did not hold: G1, H4, I13, B1, D8, E7, 0.4, D2. D2 was then confirmed behaviorally with a short offline PoC.
- **"Warnings: 0" in an audit that never ran anything,** and sections 0 and G declared CONFORMING while holding [IMP] failures.

The auditor's evidence column was largely accurate: file:line references checked out. The failures were procedural and mechanical, which means a tool can catch them.

## Proposal 1: report consistency gate

Add `scripts/check_audit_report.py`: stdlib only, no network, read-only, exit 0/1, same style as the Way gates.

Hard checks:

| Code | Check |
|---|---|
| R1 | Every checklist item in STANDARD.md has exactly one verdict row; no unknown ids |
| R2 | Declared [CRIT] failure list = computed list (partial/no on an item marked [CRIT] in STANDARD.md) |
| R3 | Protocol counts per section = counts from per-item verdicts |
| R4 | Overall verdict follows the verdict rules |
| R5 | Audited version named: commit SHA, or an explicit no-SHA statement |

Soft checks, which fail only under `--strict`:

| Code | Check |
|---|---|
| S1 | A static audit marks verdicts as static implementation evidence / behavioral verification pending |
| S2 | No "Warnings: 0" when nothing was run |
| S3 | No section called CONFORMING while it has [CRIT]/[IMP] failures |

**Test vectors:**
- **GREEN:** synthetic reports built from STANDARD.md — one all-yes, one mixed with failures and a correct protocol, one applying J3 inherited criticality correctly (a failing J3 guarding a [CRIT] item, listed and counted as [CRIT]).
- **RED:** synthetic, one per failure class — R1 (missing row, duplicate row, unknown id), R2 (inflated list, omitted [CRIT] failure), R3 (protocol mismatch), R4 (wrong checked verdict; zero checked; all three checked), R5 (no standard version identified), S1–S3 (soft), J3 inheritance (a [CRIT]-guarded J3 failure scored as [IMP]). The external-project report is deliberately not committed.

The gate verifies consistency, not correctness. A wrong "yes" with a consistent protocol stays green; that remains the reviewer's job.

## Proposal 2: protocol template fields

Report header (filled per report):

```
Standard version:  MAQS <version>          (pins the STANDARD.md the audit was run against)
Audited version:   <commit SHA>  |  no-SHA: <reason>; reconstructed as <SHA> by <method>
Audit type:        static  |  behavioral  |  mixed
Warnings:          <n> (with per-warning exceptions)  |  not collected
```

Per-item verdict rows (one row per checklist item) carry an evidence-status column: `static` / `behavioral` / `pending` — the terms already defined in the v1.7 glossary — and, for J3 only, the guarded item (inherited criticality, v1.8.1). The Audit Result Protocol is computed from these rows, never written by hand.

## Proposal 3: audit guide, section 2.2 (Conducting the Audit)

Two rules for the auditor. They are agent discipline, so they belong in the guide, not in the checklist:

1. **Criticality is copied, never assigned.** The marker for every item is taken verbatim from STANDARD.md of the version being audited.
2. **The protocol is computed, never written.** It is derived from the per-item rows, by `check_audit_report.py` or by the same rule by hand, after the last row is final.

---

*Files:* `check_audit_report.py` (gate), this proposal. Both were run against STANDARD.md v1.7; the parser reads 96 items with criticality for all of them. They need a re-check against 1.8 after the release.

## Implementation note (2026-10-27, package landed in [Unreleased])

- Gate shipped as `scripts/check_audit_report.py` with three additions over this proposal, per the owner's release decision: R4 reads the checked verdict line (`[x]`; zero or more than one checked = hard R4); `--standard-version <tag>` resolves the standard via `git show <tag>:STANDARD.md` (without the flag — the report's "Standard version" field; missing field = hard R5); J3 inherited criticality (v1.8.1): a failing J3 row naming a [CRIT] guarded item is scored [CRIT] in R2/R4 and in the per-section [CRIT] counts (the same rule, so per-section codes reconcile with the list per STANDARD §2.2 step 6).
- The report fields live in the report header (Standard version, Audited version, Audit type, Warnings); the verdict rows carry the evidence-status and guarded-item columns; the protocol table is computed.
- Re-checked against v1.8.1: the parser reads 96 items with criticality for all of them (and 80 items for v1.2). Test vectors: `tests/audit_report/` (synthetic only; the external-project report is deliberately not committed).
- The project name and snapshot SHA of the incident are withheld per the public-repository name policy ("agent-run static audit of an external project").
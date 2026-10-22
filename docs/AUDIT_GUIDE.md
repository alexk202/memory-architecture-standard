# MAQS Audit Guide

**Companion document to the Memory Architecture Quality Standard (MAQS).**

Scope: how to conduct, deliver, and report an audit. This guide does
not define architectural requirements — those belong to the standard
itself (`STANDARD.md`).

**Effective from:** v1.8

---

## 1. Units of Comparison

- Every audit operates on a fixed unit: a **system snapshot**, a
  **standard version**, and a **fixed item set**.
- Baseline and re-audit must use the same standard version and the
  same item set. Comparing across standard versions or item counts
  is invalid; if a baseline exists only in an older version,
  recompute it against the current version or document it separately
  with version metadata.
- Items marked `N/A` do not count as improvements. A change within
  `partial` (quality improvement without a verdict change) is tracked
  separately from verdict deltas.

---

## 2. Standard Delivery Isolation

- Standard rules must not be delivered in the same context as
  feature-level task specifications. The audit cycle is a separate
  run with its own unit of comparison.
- Rationale: rules delivered alongside competing task specifications
  degrade to second priority; items compatible with the existing
  pipeline get fixed, items requiring a process change are left
  untouched (documented pattern from live audit sessions).
- A **re-audit against the baseline map** is a mandatory checkpoint
  before a release is published. A release without re-audit is itself
  a finding.

---

## 3. Warnings and Test Runs

- A green test run with warnings is **not green** if the warnings
  concern [CRIT] zones. A warning read by no one is equivalent to
  broken indication.
- Reconciliation rule: warning count > 0 in critical zones is scored
  as a failure unless explicitly resolved.

---

## 4. Report Format

- **Verdict scale:** `yes` / `partial` / `no` / `N/A`. `N/A` requires
  justification.
- **Separated criticality counting:** never merge `no` and `partial`
  into one number. Required summary format:

  > "N critical failures (of which M in the 'partial' category) +
  > P [CRIT]-tagged items with a 'partial' verdict, without double
  > counting."

- Per-section item codes must reconcile to the totals without
  intersections.
- **Number reconciliation checklist** — verify before publication:

  1. Section sums match the totals table.
  2. Item codes in per-section tables match the failed/partial lists.
  3. No item counted twice (e.g., listed both as `no` and in the
     partial [CRIT] set).
  4. Deltas computed against the same baseline version and item set.

---

## 5. Publication Modes

- **Aggregate mode:** `yes` / `partial` / `no` / `N/A` table by
  section + failed item codes. No project name, no code, no technical
  details. Publishable at any time; contains only assessments, not
  vulnerabilities.
- **Full analysis mode:** detailed findings with file/line references.
  Published only after the responsible disclosure procedure is
  exhausted (section 6).
- **Silence:** valid choice; document the decision and date
  internally.

---

## 6. Responsible Disclosure Protocol

1. **Private delivery** to the maintainer with a dated report.
2. **Deadline:** 30 days for critical findings, 90 days for the
   rest. Record actual dates in provenance.
3. If a response arrives before the deadline: re-audit the response,
   update verdicts, optionally publish as a before/after case (with
   permission or after deadline expiration).
4. If no response by the deadline: aggregate mode may be published
   immediately; full analysis mode becomes an option.
5. All publication decisions must be supported by the **evidence
   chain**: report, session logs, delivery records, dates.

---

## 7. Case Register

Each audited project gets an entry:

| Field | Description |
|-------|-------------|
| System version | Version/commit of the audited system |
| Standard version | MAQS version used for the audit |
| Item set | Total items checked (including N/A count) |
| Audit date | Date the audit was conducted |
| Delivery date | Date the report was delivered to the maintainer |
| Verdict summary | Aggregate counts per criticality level |
| Re-audit delta | Changes from baseline (if applicable) |
| Publication mode | Aggregate / full analysis / silence |

Case narratives suitable for training auditors may be added to
`examples/` (aggregate mode by default).

---

*This document is part of the MAQS standard repository and is
licensed under CC-BY-SA-4.0, consistent with the standard itself.*

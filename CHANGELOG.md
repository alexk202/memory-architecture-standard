# Changelog

All notable changes to the Memory Architecture Quality Standard.

## [Unreleased]
*Ideas and candidates for next version — not yet implemented.*

### Backlog
- G8: Forgetting cascade (GDPR right to be forgotten — coordinated deletion across all stores)
- `docs/VERIFICATION_QUERIES.md` — example SQL/commands for each [CRIT] item
- Section K: add "Tool" column with example verification tools
- `standard.json` / `standard.yaml` — machine-readable version
- CLI tool `maqs audit` — automated checking of verifiable items

## [1.4] - 2026-09-26

### Added
- **F7** Authority laundering prevention: compression must not upgrade trust level through co-occurrence [CRIT] (internal feedback)
- **I10** Warning deduplication with counter; status ambiguity escalated as B5-class [IMP] (found during internal self-audit)
- **Section K** — 3 new symptom rows: false-green warnings, async test silent skip, test files in live directory
- **Audit protocol** — "Warnings" line added to verdict table

### Changed (community feedback: Edward Izgorodin, Mnemoverse)
*Architecture-level review of isolation and context-assembly sections. Not a complete audit or endorsement of the standard.*
- **G1** expanded: negative fixtures required — independently authenticated callers, wrong/omitted scope, read-only write attempt, access after revocation. Proves boundary behavior, not filter presence.
- **E6** expanded: "admitted ≠ trusted" — retrieval and compression must not upgrade evidence into instructions

### Changed (found during internal self-audit)
- **J3** expanded: unexecuted test (silent skip, async without runner) = incomplete, same as fix without test
- **H5** expanded: isolation covers assistant's filesystem, not only databases; production paths as test defaults = violation
- **I2** expanded: warnings = false-green signal; acceptance requires 0 warnings or documented per-warning exceptions

### Changed (internal feedback)
- **F2/F3** verification methodology: negative fixtures concept — proving boundary behavior through attempted violations

### Removed from backlog
- ~~D9: Retrieval precision measurement on golden set~~ → implemented in v1.3 as D9: Conceptual Gating

### Notes
- Checklist items: 82 → 84 (added F7, I10)
- Protocol table updated: F=7, I=10
- **Follow-up:** send revision link to Edward Izgorodin (Mnemoverse) — promised 2026-09-19 ✅

## [1.3] - 2026-09-15

### Added
- **Glossary** — 9 core terms (Store, Provenance, Feedback contamination, Alive memory, Blind truncation, Bare call, Decay, Bridge, Guardian)
- **Section 1** — Loop → Sections mapping table
- **P8** — Runtime environment awareness: environment issues are not counted against the standard
- **0.5a** — Dead-code detection: green tests on code never invoked in production are a false safety signal [CRIT]
- **D9** — Conceptual gating of external results: keyword match without conceptual relevance is excluded [IMP]
- **I7** — Expanded to a 10-question diagnostic dialog protocol in three tiers
- Section K problem descriptions made searchable; keywords block in README
- FAQ in README; GitHub issue template

### Changed
- Checklist items: 80 → 82 (added 0.5a, D9)
- README: version badge, sections table (0 = 8, D = 9, total 82)

## [1.2] - 2026-08-27

### Added
- **Section 2.1** Preparation Phase (7 steps: P1–P7) — mandatory for auditing live systems
- **Section 2.3** Remediation methodology (roadmap, waves, commits)
- **Section 2.4** Diagnostic startup/shutdown scripts as architectural requirement
- **D8** Embedding model language match and versioned migration [CRIT]
- **E10** Protected/alive memory mechanism with capped count [REC]
- **E11** Position-aware injection for long contexts [IMP]
- **I7** Diagnostic dialog protocol — structured agent self-assessment [REC]
- **I8** Personality trait persistence across restarts [IMP]
- **I9** Log rotation — automatic, size-capped [IMP]

### Changed
- **B3** Strengthened: "Source diversity preserved as provenance, not duplicated memory"
- **E1** Clarified: dropping whole low-priority blocks is not blind truncation
- **E4** Relaxed: structured blocks may use lossless alternatives, not only preserved in full
- **F2** Rephrased: principle-based (no memory writes, no history, no feedback) instead of implementation-specific "bare"
- **F3** Bounded instead of impossible: maximum compression depth defined
- **G1** Added testable criterion: must distinguish at least two independently testable scopes
- **I4** Added security/privacy exception for hard deletion
- **J1** Coupled changes explicitly allowed when grouped and documented as single logical unit
- **P4** Added security/privacy exception for deletion during migration
- **P5** Changed from "fix before audit" to "triage and track separately"

## [1.1] - 2026-08-21

### Added
- All 80 checklist items across 11 sections (0, A–K)
- Reference loop model
- Audit methodology
- Quick diagnostics table (Section K)
- Verdict protocol with pass/fail rules

## [1.0] - 2026-08-19

### Added
- Initial 74-item checklist (internal draft)
- Sections 0, A–J

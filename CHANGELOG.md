# Changelog

All notable changes to the Memory Architecture Quality Standard.

## [Unreleased]
*Ideas and candidates for next version — not yet implemented.*

### Backlog
- ~~D9: Retrieval precision measurement on golden set~~ → implemented as D9: Conceptual Gating of External Tools
- G8: Forgetting cascade (GDPR right to be forgotten — coordinated deletion across all stores)
- `docs/VERIFICATION_QUERIES.md` — example SQL/commands for each [CRIT] item
- Section K: add "Tool" column with example verification tools
- `standard.json` / `standard.yaml` — machine-readable version
- CLI tool `maqs audit` — automated checking of verifiable items

### Community feedback (Edward Izgorodin, Mnemoverse, 2026-09-19)
*Architecture-level review of isolation and context-assembly sections. Not a complete audit or endorsement of the standard.*
- G1: Add negative fixtures — independently authenticated callers, wrong/omitted scope, read-only write attempt, access after revocation. Current wording proves filter presence, not boundary behavior.
- A1/E6-E7: Distinguish "admitted" from "trusted" — a record that passes admission must remain evidence; retrieval and compression must not upgrade it into instructions. Add fixtures for forged markers and instructions that survive summarization.
- Verification methodology: introduce negative fixtures concept — proving boundary behavior through attempted violations, not through filter existence.
- **Follow-up:** send revision link to Edward Izgorodin upon v1.4 publication (promised 2026-09-19)

### Internal feedback 2026-09-19
- F/G cross-section: Authority laundering — a low-trust record must not inherit trust level by being summarized or cited alongside a high-trust record. Compression must preserve or downgrade trust level, never upgrade it through co-occurrence. (Feedback from personal AI assistant)

### Incident: false-green tests (found during internal self-audit, 2026-09-20)
*42 async tests silently skipped, 63 warnings masking real defects, test artifacts in production directory.*
- J3 expand: a test that is never executed (silent skip, async without runner) is treated as incomplete, same as a fix without a test
- H5 expand: test isolation covers the assistant's filesystem, not only databases; production paths as test defaults are a violation; guard check "before/after" on live directories
- I2 expand: warnings in test runs are not noise — a run accepted with warnings is a false-green signal; acceptance requires warnings: 0 or explicitly documented per-warning exceptions
- I (new I10): Warning deduplication — same warning repeated N+ times per interval is aggregated with counter; consequent status ambiguity ("success" on unperformed work) escalated to B5
- Section K: add rows — "Warnings always existed, nobody reads them" → false green / W invariant; "async tests in unittest wrapper" → silent skip; "test files in assistant's live directory" → H5 filesystem gap
- Audit protocol: add "Warnings: N (all with documented per-item exceptions)" to verdict table; W1/W2 failure = blocker

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

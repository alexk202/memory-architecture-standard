# Changelog

All notable changes to the Memory Architecture Quality Standard.

## [Unreleased]
*Ideas and candidates for next version — not yet implemented.*

### Added
- **E12** Artifact–Memory Separation: external artifacts must
  remain distinguishable from memory and contextual
  representations of their content. Event/research memory may
  preserve why an artifact is being analyzed and which elements
  require attention, but must not silently substitute,
  reconstruct, or modify the current artifact representation.
  When current artifact data conflicts with Content Memory or
  prior expectations, the conflict must remain observable and
  the current artifact must retain factual precedence. [IMP]
- **P9** Controlled artifact experiment: when artifact–memory
  contamination is suspected, prepare a new artifact of a
  different type, verify syntax independently before delivery,
  deliver without prior disclosure, and record the result. A
  clean read constitutes acceptance of the delivery channel.
  [REC]
- **P9-b** Decoy verification: artifact contains a plausible but
  false element that memory would expect; any mention of absent
  decoy in the report = proof of confabulation. Canary catches
  "didn't read"; decoy catches "fabricated." Note: both tests are
  one-sided — positive result is proof, negative is inconclusive.
  Full coverage requires both. [REC] (internal feedback)
- **P10** External auditor isolation: any automated or agent-driven
  audit must run from an environment that has no write-access to
  production stores and shares no runtime state (processes, caches,
  loaded embedding models) with the audited system. Audit results
  are written only to an external report. [CRIT]
- **0.6a** (clarification to 0.6): For each store and for the
  assembled context, a local baseline is recorded (volume, typical
  context size, % model-generated content). Anomalies are defined
  relative to the system's own baseline, not universal numbers. [IMP]
- **F8** Model-output importance ceiling: records with provenance
  source=model_output (or equivalent) cannot receive importance
  above a defined ceiling until confirmed by an external source
  or the user. [IMP]

### Added (MAQS_BASE empirical analysis, 2026-10-04)
*Derived from systematic pass over 10,800 journal incidents across
journald, varlog, project logs, and claude sessions. Methodology:
read-only external audit (P10), three-axis taxonomy, lineage-backed
candidates. Attribution: agent execution, Stasik (specification),
Prima (taxonomy and C-code criteria), Aleksandr (approval).*
- **I11** Recovery loop cause diagnosis: any automatic restart
  (systemd/supervisor/self-heal) must be accompanied by a
  diagnostic trace of the root cause (stderr/exit code in a
  persistent journal). A recovery cycle without diagnosis is
  prohibited: after N repetitions — halt and alert, not eternal
  restart. Lineage: finik-indexer ×2422 restarts at 1.00h
  interval, 0 own messages in journal. [CRIT]
- **I12** Escalation budget: a repeated dependency failure with
  identical signature must escalate after N occurrences
  (alert/halt/flagged degradation), not poll indefinitely. A
  system aware of a failure that does not escalate degrades
  silently. Lineage: LMStudio ping ×21608, Connection refused
  for 8 days without reaction. [CRIT]

### Changed (MAQS_BASE empirical analysis, 2026-10-04)
- **I10** expanded: warning noise budget — after N identical
  warnings, deduplicate or escalate to a different level;
  ×8.5M identical NVRM GPU warnings over 100 days destroys
  observability (signal drowns in noise). I10 now covers both
  deduplication and budget enforcement.
- **D8** expanded: incompatible embedding dimensions must produce
  an explicit rejection with diagnostics, not a burst of
  warnings during search. Lineage: Incompatible dimension
  ×1000+ across months (Fynik embedding model replaced without
  reindexing — the canonical D8 example).
- **I2** expanded: empty diagnostic strings ("❌ delete_line:"
  without file, cause, or object) are prohibited — visibility
  of monitoring without material for investigation is worse
  than honest silence. Lineage: ×935 empty error lines over
  weeks (Klodik).

### Changed
- **E4** clarified by E12: structured content must be preserved
  not only against lossy compression, but also against
  substitution by prior contextual or memory-derived
  representations.
- **I1** applies to artifact/context contamination: monitoring
  should detect cases where prior memory appears in analysis of
  a current artifact without being present in the artifact
  itself.
- **J3** extended: artifact-memory conflict cases should have
  regression guard tests where applicable.

### Backlog
- G8: Forgetting cascade (GDPR right to be forgotten —
  coordinated deletion across all stores)
- docs/VERIFICATION_QUERIES.md — example SQL/commands for
  each [CRIT] item; expand with filesystem and process checks
  (log sizes, orphaned index files, mtime divergence between
  related stores), not only SQL
- docs/ARTIFACT_MEMORY_PIPELINE.md — full research protocol
  for artifact-memory separation experiments
- docs/CONTEXT_PROVENANCE.md — provenance labels
  (artifact_now / memory / model_output) in assembled context;
  makes E6/E12/F7 mechanically verifiable, not discipline-dependent
  (feedback from personal AI assistant)
- Section K: add "Tool" column with example verification tools
- Section K symptom row (pending confirmation):
  Current artifact is valid, but agent reports remembered
  structure → Artifact-Memory contamination → E12, I1
- standard.json / standard.yaml — machine-readable version
- CLI tool maqs audit — automated checking of verifiable items;
  --read-only / --external as the only permitted production mode
- P9 refinement: canary elements — artifact must contain unique
  data guaranteed absent from memory; canary reproduced = proof
  of reading; canary absent from report = inconclusive (not proof
  of non-reading). One-sided test. (internal feedback)
- Write-before-read verification: write/modify operation must
  follow a read of current state; tools must reject write-before-read
  explicitly. Lineage: claude sessions ×3 (is_error:true).
  (MAQS_BASE, H-section candidate)
- Regex input bound: greedy regex on external text must be preceded
  by input length limit or linear strategy (tokenization/windows/
  atomic groups); regression with timing, not just result check.
  Lineage: SCAR-1, >120s hang on 1MB line. (MAQS_BASE, A-section
  candidate)
- Format-aware matching: structured logs matched by event fields,
  not serialized string; uncovered records have a counter, not
  disappear. Lineage: SCAR-4, ~75% needs_review pseudo-incidents.
  (MAQS_BASE)
- Edit-state verification (E13): edit by "old" state verified for
  freshness (state hash/version) before application; divergence →
  re-read. Lineage: claude sessions ×2. (MAQS_BASE)
- Context overflow guard: context submission limited with explicit
  rejection and hint (offset/limit), not truncation. Lineage:
  claude session ×1. (MAQS_BASE, observation only)
- Type contract verification: static contracts (type annotations)
  verified by linter in mandatory run. Lineage: LSP findings ×3.
  (MAQS_BASE)
- Section K rows (MAQS_BASE): "Service restarts every hour, nobody
  knows why" → recovery loop without cause → I11; "Dependency
  refused for days, system polls silently" → unescalated failure
  → I12; "8M identical warnings in 100 days" → noise budget → I10
- Axis C (mechanism taxonomy): C1 sequence_violation, C2
  state_desynchronization, C3 resource_limit_exceeded, C4
  format_filter_mismatch, C6 regex_pathologies, C7
  recovery_loop_without_cause_diagnosis, C8
  unescalated_persistent_failure. Reference: docs/TAXONOMY.md
  (MAQS_BASE)
- P9-c: memory-echo probe — element that is true in memory but
  absent from artifact; appearance in report = proof of memory
  supplementation (E12 violation: addition is also modification).
  Canary catches "didn't read"; decoy catches "fabricated";
  echo catches "supplemented with truth." Three diseases, three
  tests. (internal feedback)

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

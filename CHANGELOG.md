# Changelog

All notable changes to the Memory Architecture Quality Standard.

**Criticality:** [CRIT] blocker — direct risk of data loss, poisoning, or uncontrolled degradation · [IMP] silent quality degradation risk · [REC] maturity and maintainability

## [Unreleased]
**SUPP-EXT-01** External code-semantics tools: agents without
  built-in semantic code navigation (symbol/references lookup,
  project memory) are strongly recommended to use external tools
  of the Serena class (LSP-based semantic servers, semantic search,
  project-scoped memory). Rationale: flat, file-by-file audit loses
  cross-module relationships (proxy calls, dynamic imports, duplicated
  logic) — the class of errors invisible to line-level review.
  Constraint: valid only in read-only mode with respect to the
  audited system, with tool state kept external (P10-compatible);
  any tool with write access to the audited store is out of scope
  of this recommendation. [REC]
  *Candidates for v1.6 — derived from MAQS_BASE Stage 6 empirical
  analysis (101,943 incidents from 8 assistant directories → 7,959
  canonical). Methodology: read-only external audit (P10), three-axis
  taxonomy, lineage-backed candidates, consilium review with
  unanimous/majority decisions. Attribution: agent execution with
  internal review and approval by the project owner.*

### Added (MAQS_BASE Stage 6, unanimous)
- **C8** Traceback coverage rule: every traceback class observed
  in production must map to at least one pattern-coverage rule
  (C1–C7 or dedicated handler). A traceback class with zero
  coverage is a gap. Lineage: 20,728 tracebacks across 8
  assistant directories with 0 pattern coverage — axis C rules
  exist but produced no triggers in the entire corpus. [CRIT]
- **I13** Secret exposure guard: secrets (API keys, tokens,
  passwords) must never appear in plain text in logs, error
  messages, or diagnostic output. A masker/redactor must be
  applied before write. Includes credential-in-URL class: both
  query-parameter form (`?token=...`) and path-embedded form
  (`bot<id>:AA...` in request path). Lineage: 1 real secret
  value + credential-in-URL patterns found in Stage 6 scan. [CRIT]

### Added (MAQS_BASE Stage 6, majority)
- **I14** Error handler registration: if an exception class is
  probed (caught and re-raised or logged) but has no registered
  handler or escalation path, the probe is incomplete —
  detection without reaction is not coverage. [REC]

- **I15** Layer-aware diagnostics: memory diagnostics must identify
  which memory layer a query addresses (persistent stores, session
  context, transient state) before interpreting the answer. Expected
  answer quality differs by layer: verbatim recall is expected from
  persistent stores, approximate or noisy answers are normal for
  fading session context. A noisy answer from a transient layer is
  not evidence of degradation; a precise answer from a persistent
  layer is not evidence of contradiction. Layer identification is a
  prerequisite for valid interpretation. [REC]

### Changed (MAQS_BASE Stage 6, unanimous)
- **D8** pinned axes: incompatible embedding dimensions map to
  axes A3 × B1 + C2 (not A9 × B2 as previously categorized).
  15/15 incidents were in the wrong category; the correct
  assignment is: A3 (type mismatch), B1 (hard crash), C2
  (validation failure). [CRIT]
- **I10** expanded: warning noise budget — DEBUG-level messages
  contribute 755 weight out of ~7,000 total; a DEBUG ceiling
  pre-filter is required before incident classification.
  Messages at DEBUG level are excluded from the incident
  corpus unless explicitly promoted. [IMP]

### Changed (MAQS_BASE Stage 6, majority)
- **I12** Escalation budget B-axis: fixed at B2 ("visibility
  without reaction") — a system that logs a dependency failure
  but takes no escalation action (alert/halt/degrade) operates
  at B2 regardless of log verbosity. Previously ambiguous
  between B2 and B4. [CRIT]
- **Format-aware matching** expanded: incident classification
  must account for log level, file class (journal vs application
  log vs config), and negative signals (success messages
  incorrectly classified as incidents). Lineage: success-as-
  incidents 3/1,030 weight, config noise 6/28 weight. [IMP]

### Procedural (MAQS_BASE Stage 6)
- Needs-review cluster resolution: clusters are resolved by
  weight (sum of incident weights), not by count. Top-15
  clusters cover 69% of needs_review incidents.
- `_receive_event` × 1,664 — noise source identified;
  procedural deduplication rule applied.

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
- standard.json / standard.yaml — machine-readable version
- CLI tool maqs audit — automated checking of verifiable items;
  --read-only / --external as the only permitted production mode
- Write-before-read verification (MAQS_BASE, H-section candidate)
- Regex input bound (MAQS_BASE, A-section candidate)
- Edit-state verification E13 (MAQS_BASE)
- Context overflow guard (MAQS_BASE, observation only)
- Type contract verification (MAQS_BASE)
- Axis C mechanism taxonomy: docs/TAXONOMY.md (MAQS_BASE)

### Notes (v1.6 RC)
- Checklist items: 89 → 93 (added C8, I13, I14, I15)
- Protocol table updated: C=8, I=16
- MAQS_BASE Stage 6: 101,943 incidents → 7,959 canonical,
  1,928 needs_review
- Numbering: I13 = Secret Exposure Guard, I14 = Error Handler
  Registration (resolved from consilium discussion)
- I11 (Recovery loop) and I12 (Escalation budget) from v1.5
  confirmed by Stage 6 data with exact lineage match
- Top needs_review clusters (webhook-secret Permission denied
  ×22, context-truncate ×25) staged for Stage 7 review
- 4 unanimous decisions, 3 majority decisions, 2 procedural rules
- Format-aware matching moved from Backlog to Changed

## [1.5] - 2026-10-05

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
- **P9** Controlled artifact experiment (base): when artifact–memory
  contamination is suspected, prepare a new artifact of a
  different type, verify syntax independently before delivery,
  deliver without prior disclosure, and record the result. A
  clean read constitutes acceptance of the delivery channel. [REC]
- **P9 diagnostic triad** (P9-a / P9-b / P9-c): all three probes
  are one-sided — a positive result is proof, a negative result
  is inconclusive. See docs/P9_DIAGNOSTIC_GRID.md.
- **P9-a** Canary probe: unique data embedded mid-body, absent
  from all memory stores. Reproduced = proof of reading.
  Absent = inconclusive. [REC] (internal feedback)
- **P9-b** Decoy verification: plausible but false element that
  memory would expect; any mention = proof of confabulation.
  Absent = inconclusive. [REC] (internal feedback)
- **P9-c** Echo probe: memory-true element absent from artifact,
  thematically tempting. Appearing = proof of supplementation
  (E12 violation). Absent = inconclusive. [REC] (internal feedback)
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
candidates. Attribution: agent execution with internal review
and approval by the project owner.*
- **I11** Recovery loop cause diagnosis: any automatic restart
  (systemd/supervisor/self-heal) must be accompanied by a
  diagnostic trace of the root cause (stderr/exit code in a
  persistent journal). A recovery cycle without diagnosis is
  prohibited: after N repetitions — halt and alert, not eternal
  restart. Lineage: indexer service ×2422 restarts at 1.00h
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
  ×1000+ across months (embedding model replaced without
  reindexing — the canonical D8 example).
- **I2** expanded: empty diagnostic strings ("❌ delete_line:"
  without file, cause, or object) are prohibited — visibility
  of monitoring without material for investigation is worse
  than honest silence. Lineage: ×935 empty error lines over
  weeks (local assistant).

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

### Notes
- Checklist items: 84 → 89 (added 0.6a, E12, F8, I11, I12)
- Protocol table updated: 0=9, E=12, F=8, I=12
- Preparation phase: P1–P8 → P1–P10 (added P9 diagnostic triad, P10 external auditor isolation)
- K table: +3 symptom rows (recovery loop, unescalated failure, noise budget)
- MAQS_BASE empirical analysis: 10,800 journal incidents processed
- Edward Izgorodin (Mnemoverse) credited for negative fixtures concept (v1.4)

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

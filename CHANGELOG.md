# Changelog

All notable changes to the Memory Architecture Quality Standard.

**Criticality:** [CRIT] blocker — direct risk of data loss, poisoning, or uncontrolled degradation · [IMP] silent quality degradation risk · [REC] maturity and maintainability

## [Unreleased]

### Backlog (pending)

- MAQS_BASE Stage 7: review of staged needs_review clusters
  (webhook-secret Permission denied ×22, context-truncate ×25);
  candidates pass the admission gate (docs/ADMISSION_CRITERIA.md §2),
  growth budget (§5) and release sync checklist (§9) before entering
  a release
- E14 Edit-state verification (MAQS_BASE) — renumbered from E13
  (v1.7); awaiting measured lineage
- G8: Forgetting cascade (GDPR right to be forgotten —
  coordinated deletion across all stores)
- docs/VERIFICATION_QUERIES.md — example SQL/commands for
  each [CRIT] item; expand with filesystem and process checks
  (log sizes, orphaned index files, mtime divergence between
  related stores), not only SQL; on live WAL databases the
  before/after isolation guard compares rows/content, not the
  file md5 (a checkpoint changes the hash at zero row delta,
  producing a false failure signal)
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
- Context overflow guard (MAQS_BASE, observation only)
- Type contract verification (MAQS_BASE)
- Axis C mechanism taxonomy: docs/TAXONOMY.md (MAQS_BASE)
- D1: punctuation normalization in lexical gate tokenization — awaits
  product lineage per §2.5; no development-lineage exception.

## [1.8] - 2026-10-27

- Test-evidence pattern candidate №11 "native isolation available but not enabled" logged in docs/patterns/TEST_EVIDENCE_PATTERNS.md (2026-10-25 mem0 run_id line: the native per-question history isolation was measured by the P4 incident demo AFTER the integration's own H5 guard had found the channel; candidate only, not canonized in this release).

### Added (glossary, 2026-10-24)
*Two verdict-reclassification terms added to the Glossary (STANDARD.md),
formalizing the P4 relabel precedent: source — external reviewer feedback
(attribution withheld by request), linked to maqs-way 469e237 (audit doc
reclassification) and the mem0/letta audit relabels. The terms separate
"what code reading proves" from "what running a defined check would prove":
a static-reading audit may credit implementation evidence (file:line
references) but must not imply behavioral results; a defined-but-not-run
behavioral check is explicitly pending, and any future result must name the
tested version and setup. Both terms enter the next release with the
owner's signature per the release sync checklist.*

- **Static implementation evidence** — a verdict based on reading the code
  with file:line references: the mechanism is present and wired in the
  inspected version. It makes no claim about runtime behavior.
- **Behavioral verification pending** — the behavioral check for an item
  is defined (for example, an attempted violation that must fail) but has
  not been run. Any future result must name the tested version and setup;
  it is not a general certification of the system.

### Changed (local assistant re-audit, 2026-10-24)
*Derived from a live local-assistant audit against v1.7 and its remediation.
Each extension passed admission criteria (docs/ADMISSION_CRITERIA.md) with
measured lineage. Editorial rule applied: each extension names a failure
mechanism, not an episode; draws a boundary, not a list; is verifiable by
procedure or observation. Attribution: internal review and approval by the
project owner.*

**Extensions (6):**

- **A2 / I13** expanded: masking is verified against secrets adjacent to
  other characters in any context, not only free-standing tokens (e.g.,
  a token inside a URL path after an identifier). A masking suite whose
  fixtures contain only free-standing secrets can pass green while
  production forms leak.
  Lineage: a bot token leaked into a live log for a year while masking
  tests were green; the pattern's leading boundary anchor did not match
  the prefix-glued form; found when an embedded-form fixture failed.
- **E7** expanded: the set of code-generated render markers must be
  reconcilable mechanically — every marker the renderer emits appears in
  the imitation filter's inventory. Drift (a marker entering the renderer
  without entering the filter) is an E7 failure, verified by diffing the
  two lists, not by auditor recall.
  Lineage: 3 markers unprotected for weeks; 6 more added during
  remediation, each requiring a manual filter update.
- **H5** expanded: the before/after isolation guard executes on every
  suite run, integrated into the test runner's session hooks, not as a
  periodic manual check. A green suite without an in-runner guard is not
  evidence of isolation.
  Lineage: a test ran against live stores for 54 days across at least
  three green runs. Second case — the standard author's own project
  (2026-10-25): a guard built to this extension (live roots snapshotted
  before every runner, re-verified after, any divergence fails the run)
  found in its first full guarded run that every test had been writing
  its conversations into the live memory history store and reading a
  10-message tail of previous tests back into every extraction prompt —
  14.8% of stored facts contaminated, invisible for nine days while
  every headline metric stayed healthy; the isolated re-measurement left
  R@5 = 1.000, so it was the guard, not the green history, that surfaced
  the leak.
- **I9** expanded: the log write path has a single active writer across
  process starts. The launch wrapper appends, never truncates: truncation
  at every start destroys the previous session's incident evidence and
  silently defeats size-based rotation. (Example of the same mechanism:
  a second handler writing to the same file doubles every record.)
  Lineage: truncation at every start erased the previous session,
  including leak evidence; rotation never fired in a year.
- **§2.2.3 (audit methodology)** expanded: evidence must establish
  reachability of the claimed defect, not only presence of a pattern —
  gate conditions (flags, callers, enclosing scopes, per-instance schema)
  are part of the evidence. A pattern that exists but is unreachable is
  not a failure. Schema and key claims are verified per instance (catalog
  query), not inferred from naming. A verdict based on reading alone is
  labeled "static implementation evidence" (see Glossary). A verdict later
  found false is corrected in the same report, with the disproving check
  attached.
  Lineage: two false verdicts in one audit (schema inferred from naming;
  pattern found but gates not traced), both corrected in the report.
- **A3** expanded: service and operational events (startup/shutdown
  markers, health snapshots) are not written into user memory stores
  under synthetic scope keys. Where legacy records exist, they are typed
  and invisible to every retrieval reader, including cross-scope scans.
  Lineage: 13 of 15 "dialogs" in the memory store were shutdown markers,
  creating phantom scopes in cross-dialog recall.

**Markup (applied in this release, no change in meaning):**
- SUPP-EXT-01 shown as a recommendation without a checkbox, under a note
  "Not checklist items and not counted in the 96 (category SUPP,
  docs/ADMISSION_CRITERIA.md)"; the Supplementary section moved from
  between I and J to after J, before K. Mechanical count of checklist
  items = 96, matching README badge, text and table.
- Audit report template (examples/AUDIT_REPORT_TEMPLATE.md): per-section
  item counts synced with STANDARD.md (0: 9 -> 10, E: 12 -> 13); the
  template had lagged behind recent releases. No change in meaning; item
  count unchanged (96).

**Docs (one line each):**
- `docs/patterns/TEST_EVIDENCE_PATTERNS.md` — pattern №10
  "error-vs-empty discriminator": a negative fixture injects an error into
  the source to prove an empty result comes from matching, not from a
  swallowed exception.

### Changed (external project re-audit, 2026-10)
*Derived from a live external project re-audit case: baseline audit
followed by remediation and re-audit against the same standard version
and item set. Each extension passed admission criteria
(docs/ADMISSION_CRITERIA.md): architecturally general, memory-specific,
not already covered at stated scope, verifiable, with measured lineage
from the re-audit delta. Attribution: internal review and approval by the
project owner.*

**Extensions (4):**
- **I10** expanded: warnings in [CRIT] zones are scored as failures
  unless explicitly resolved; this extends to test runs — a warning
  count > 0 in critical zones is a test failure. Lineage: green test
  run with unresolved warnings in critical zones passed as "green" in
  baseline audit; re-audit scored it as failure.
- **A5** expanded: provenance is required for all write channels,
  including external sync, attachments, and plugin inputs. Lineage:
  records entering memory through a sync channel bypassed provenance
  validation that was enforced only on the primary input path. (Item ID
  corrected from E6 to A5 at release: E6 governs privileged prompt
  blocks; provenance is A5.)
- **B4** expanded: atomicity covers all state writes, including append
  operations and compound file+state pairs; partial atomicity does not
  satisfy B4. Lineage: append-style writes to a state file were not
  covered by the transactional wrapper that protected multi-store DB
  writes; a crash between file write and state update left
  inconsistent state.
- **I13** expanded: masking must cover all output points through a
  single mechanism; per-channel point fixes do not satisfy I13.
  Lineage: secret masking applied in log output but not in error
  messages routed through a separate channel; the same secret appeared
  in both paths, masked in one.
  Re-audit amendment (2026-10-23): output points include loggers owned
  by dependencies (HTTP clients, SDKs, drivers) that write secrets
  before application code runs; redaction installed at the handler
  level is the single mechanism that covers them; masking at
  application call sites does not satisfy I13 for this class.
  Additional lineage: bot token in every polling log line (15+30 rows
  persisted), written by the HTTP client's own logger, not by
  application code.

**Section 2.2 amendment:**
- Step 6 added: separated criticality counting — summary formulations
  must not merge failures ("no") and partial implementations
  ("partial") into a single number. Required format: "N critical
  failures (of which M in the 'partial' category) + P [CRIT]-tagged
  items with a 'partial' verdict, without double counting." Per-section
  codes must reconcile to the totals without intersections; reader
  reproducibility is mandatory. See `docs/AUDIT_GUIDE.md`.

**New documentation:**
- `docs/AUDIT_GUIDE.md` — audit procedure: units of comparison,
  standard delivery isolation, warnings and test runs, report format,
  publication modes (aggregate / full analysis / silence), responsible
  disclosure protocol, case register.
- `examples/` — aggregate and full analysis mode templates
  (structure defined; content added per case).
- `docs/patterns/TEST_EVIDENCE_PATTERNS.md` — 9 test-evidence patterns
  (one verdict channel, determinism isolation, fixtures via migration
  path, anti-phantom contracts, negative fixtures, fail-closed probes,
  conftest redirect, source-guard + behavioral twin, subprocess probes)
  — non-normative companion; MAQS classifies what to prove, patterns
  show how. Includes TR39 skeleton note pinned for E7.

### Changed (live assistant memory system re-audit, 2026-10-23)
*Derived from external re-audit of one live assistant memory system:
baseline audit → verification of a 22-commit remediation session →
full 96-item pass → 34-fix wave (233→320 passed). All candidates passed
admission criteria (docs/ADMISSION_CRITERIA.md); all classified as
extensions (litmus §6: existing wording vague enough to miss in practice).
Checklist unchanged: 96. Attribution: agent execution with internal
review and approval by the project owner.*
*Transparency: 6 candidates (J7, I17, J8, I18, C9, 0.9) rejected or
deferred per admission criteria — classification instead of growth.*
*Tagging: worst-case principle — a defect that masks a potentially
critical problem inherits its level; an invisible critical defect is
worse than a visible one. All 7 extensions tagged [CRIT].*

**Extensions (7):**

*Evidence quality:*
- **J3** expanded: "executed" = verdict delivered to the scoring channel
  and cannot be silently ignored — (a) exactly ONE verdict channel
  (a dual runner where each side ignores the other's result = false
  green); (b) deterministic — no races with background workers and no
  side-effects on shared process state (event loop, global registries);
  (c) guard operates on schema/state produced by the real migration
  path (hand-made fixtures drift from production stores); (d) guard
  asserts behavior, not source text (`assert THRESHOLD == 5` is
  constant-checking — documentation, not a test). Lineage: 4 masked
  failures under a dual-runner bool protocol; green-by-scheduling
  cooldown guard; 3 fixtures drifted from the migrated schema. Live
  lineage: green source-guard while the gate was dead — service down
  ~30 min, TypeError on every update (type-incompatible control
  registration); a behavioral guard closed the shared event loop
  (`asyncio.run()`) → 8 order-dependent failures. [CRIT]
- **0.5a** expanded: production call site is not enough — a control
  must be ABLE TO FIRE under production configuration: trigger
  conditions must reference state that exists in production (columns,
  tables, flags, platform capabilities). An invoked-but-unsatisfiable
  control (phantom schema, silently absent platform dependency) is
  the same false safety signal as dead code. Verification: negative
  live probe or trace of trigger conditions against production state.
  Lineage: phantom schema columns; platform-inert escalation gate
  (`date -d`, silently empty off GNU); dead API methods behind live
  routes; UNIQUE index existing only in the live DB (not created by
  code). Live lineage: 5th mechanism — control registered in the
  chain, invoked on every update, physically unable to fire once
  (library-version incompatibility). [CRIT]
- **J2** expanded: the after-measurement is a reproducible artifact
  (run output, counter, diff), not an assertion; every claim in a
  remediation report is either evidence-linked or explicitly marked
  unverified. "Verified" = "reproduced", not "should work". Lineage:
  "233 passed, 0 warnings" claimed with a live DeprecationWarning in
  the same run; "8/10 [CRIT] fixed" vs 2 false claims + 1 regression
  found by independent re-verification. [CRIT]

*State integrity:*
- **I3** expanded: store verification must control sidecar/derived
  recovery state (write-ahead logs, shared-memory maps, replica
  caches): a broken primary reads as healthy while a sidecar replays
  old state; a check performed in the presence of foreign sidecars
  is not a check. Lineage: corrupted primary read as healthy via
  WAL replay. [CRIT]
- **C1** expanded: diagnostic artifacts about memory (context
  snapshots, self-report dumps, diagnostic exchanges) are stores for
  growth-map purposes (per Glossary Store definition): retention
  policy, size caps, isolation from test records. Lineage: 443-row
  append-only snapshot without rotation or cap; 239 test rows mixed
  with 204 live. [CRIT]

*Configuration:*
- **0.5** expanded: "code" includes configuration — multiple sources
  of one parameter with a launch-path-dependent winner (env load
  order, export semantics) are divergent parallel versions; the
  winner must be deterministic and unique. Divergence between sources
  is a 0.5 finding for parameters affecting behavior (flags, store
  paths), even if both values are individually valid. Lineage:
  behavioral flag true/false split across two .env files (winner
  depended on launch method); DB_PATH defaults split across 7
  modules (dead vs live store). [CRIT]

*Security:*
- **E7** expanded: marker/keyword filtering must operate on a
  normalized form (Unicode NFC/NFKC + lookalike folding): filtering
  the raw string passes homoglyph/digit bypass variants; a filter
  that passes a normalization variant of a protected marker does not
  satisfy E7. Lineage: homoglyph/digit-variant instruction ("0" for
  "и") bypasses a literal-match sanitizer. [CRIT]

**Routing litmus (J3 vs 0.5a; one live incident legitimately supports
both — distinct defect classes, §2.5):**
- J3: "Remove the behavioral check, keep the source scan — does the
  evidence survive?" No → J3 not met.
- 0.5a: "Enable the control in production configuration — can it
  fire at least once?" No → 0.5a not met.

**H5 lineage note (not an extension — filesystem covered by v1.4
wording):** isolation guards must enumerate ALL live files
(idempotency journals, diagnostics, uploads), not only databases.
Lineage: test update_id written to live processed_updates.jsonl;
conftest guard covered only DB paths.

## [1.7] - 2026-10-21

### Added (live remediation session, 2026-10-21)
*Derived from full remediation of one live assistant memory system
(~10,000 records, 5 storage layers, 14 modules, ~70 public functions).
Methodology: single-system manual session — measurements are per-DB
counts with record IDs and backups, not journal corpus frequencies.
Each candidate passed admission criteria (docs/ADMISSION_CRITERIA.md):
architecturally general, not covered by v1.6, verifiable by auditor,
with measured lineage. Attribution: agent execution with internal
review and approval by the project owner.*
- **0.8** Retrieval path completeness: every store that participates
  in writing must be reachable by the primary retrieval path. A store
  written to but not queried — or queried only in a fallback branch
  that does not trigger — is silent data loss at assembly time. The
  architecture map (0.2) must verify not only read/write ownership
  but path reachability in the working retrieval code. Lineage:
  9,848 records in one store with 0% vector coverage; keyword search
  existed only in an unreachable fallback branch; manual query for
  a known term present in three tables returned zero results in
  assembled context. [CRIT]
- **E13** Context key rendering completeness: every key produced by
  the context assembler must be consumed by the prompt renderer. A
  key that is assembled, filtered, and then not rendered silently
  discards retrieval results at the last step. Lineage: one context
  key was assembled and passed through context graph filtering but
  had no rendering clause in the prompt builder; vector search results
  vanished between assembly and prompt. Additionally: a diagnostic
  snapshot script carried its own copy of the assembly logic without
  this key — two divergent truths about the prompt. [IMP]
- **I16** Diagnostic self-contamination: a diagnostic exchange
  (I7 self-report, health check) is itself a record written into the
  diagnosed memory. After the finding is resolved, the diagnostic
  record must surface paired with its resolution (link, marker, or
  co-injection) — not as "current state." An unresolved diagnostic
  complaint recursively confirms itself. Lineage: I7 self-report
  (importance 0.8, short-term layer) persisted as the fact "context
  is fragmentary" after the underlying issue was fixed; a predecessor
  record with the same complaint existed 3 months earlier (2026-07),
  also unlinked from its resolution — the pattern had already
  reproduced. [IMP]
- **P11** Agent audit discipline: the auditing agent must not invoke
  any method of the audited system that has write side-effects
  (decay, access counters, embedding insertion, lazy initialization)
  on live stores — even when the method is semantically a "read" or
  "query." Diagnostic probes run on file-level copies; any exception
  (live probe with owner permission) requires pre/post counter
  verification. Violation = audit contamination; affected
  measurements are invalid. Complements P10 (environment isolation):
  P10 constrains the environment, P11 constrains the agent's
  behavior within it. Lineage: 117 anonymous query embeddings
  written to live vector store + decay ×0.9 applied to live temporal
  records during diagnostic probes; remediation could not distinguish
  probe damage from historical mechanism damage. [CRIT]

### Changed (live remediation session, 2026-10-21)
- **A1** expanded: identity extraction must distinguish between the
  chat speaker's self-introduction and first-person references in
  attached file content or relayed messages from other agents. A
  file's first-person text is not the speaker. Lineage: a curated
  collection of first-person quotes from another agent overrode the
  owner's name in user_information; every system prompt after that
  addressed the wrong person; 846 junk personal_info rows accumulated
  from a broad regex `r'[Яя] ([А-Яа-я]+)'`. Secondary defect: a
  strict extractor pattern never fired because it did not match
  sentence-initial capitalization — broad + dead = double failure. [CRIT]
- **B1** expanded: application-level deduplication declares ONE
  semantic key per event, valid across ALL write paths. Lineage:
  605 duplicate rows — one response written by both sync and async
  learning paths with different keys (trigger_pattern vs
  response_pattern); minute-window guard was the fix, not a proper
  semantic key. [CRIT]
- **D7** expanded: all readers of the same store apply a uniform
  decay/side-effect policy at read time. Lineage: one reader applied
  importance decay on inject (−1, floor 1), another reader of the
  same store sorted by raw importance without decay — 64 legacy
  rows held top-5 position for over a year. [IMP]
- **D8** expanded: migration-or-version-marker contract covers all
  scored/ranked representations, not only embedding dimensions.
  Mixed scales in one sortable column (importance, confidence,
  similarity) are prohibited without a version marker. Same class
  as embedding reindexing: the representation scheme changed, the
  existing data was not migrated. Lineage: 64 legacy rows on a
  1–10 scale vs 3,088 rows on a ≤1 scale in one column; ORDER BY
  importance DESC without version → top-5 of every system prompt
  frozen on records from April 2025; I7 self-report: "last week —
  almost empty, a blank spot" despite fresh records existing. [CRIT]
- **F5** expanded: the search query itself must not be persisted in
  the searched store as a side-effect. Self-match (similarity 1.0)
  displaces real results from the retrieval limit. Lineage: 117
  anonymous embeddings accumulated from search queries; each query
  matched itself at rank 1, consuming one of two vector search
  slots. [IMP]
- **I3** expanded: backup before a DB operation = unique traceable
  name (source prefix, no basename collisions between same-named
  DBs in different directories) + integrity_check + row counts
  after copy. Lineage: a "backup" contained a different (older) DB —
  two same-named files in different directories, the second
  overwrote the first via basename; marked .INVALID with README. [IMP]
- **I15** expanded: layer-aware diagnostics require a pinned
  timestamp format per store; mixed formats (ISO-T local time vs
  SQL-style UTC) force every consumer to carry a dual parser and
  silently shift by timezone offset. Lineage: `_format_memory_time`
  treated naive T-strings as UTC (+3h shift); empirically T-format
  was always Python-local, space-format was always SQLite-UTC. [REC]
- **P10** expanded: `mode=ro` does not guarantee isolation when
  dependencies contain lazy-initialization write paths (table
  creation, seed data). A read-only diagnostic tool that
  lazy-initializes storage on first invocation writes to the live
  DB. Lineage: a prompt snapshot utility connected a storage layer
  with its own initialization; on a live DB the "snapshot" would
  have silently written seed data. [CRIT]

### Notes (v1.7)
- Checklist items: 93 → 96 (added 0.8, E13, I16)
- Preparation phase: P1–P10 → P1–P11 (added P11 agent audit discipline)
- Protocol table updated: 0=10, E=13, I=16
- 8 existing items expanded with new lineage
- Section K: +1 symptom row (retrieval results assembled but absent
  from rendered prompt → E13)
- Backlog: "Edit-state verification" renumbered E13 → E14 (E13 assigned
  to context key rendering)
- Source: single live system, manual session — not journal corpus;
  candidates validated by admission criteria, not MAQS_BASE pipeline
- Admission gate for future candidates codified in
  docs/ADMISSION_CRITERIA.md

## [1.6] - 2026-10-09

### Added
- **SUPP-EXT-01** External code-semantics tools: agents without
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

### Added (MAQS_BASE Stage 6, unanimous)
*Derived from MAQS_BASE Stage 6 empirical analysis (101,943
incidents from 8 assistant directories → 7,959 canonical).
Methodology: read-only external audit (P10), three-axis taxonomy,
lineage-backed candidates, consilium review with unanimous/majority
decisions. Attribution: agent execution with internal review and
approval by the project owner.*
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

### Notes (v1.6)
- Checklist items: 89 → 93 (added C8, I13, I14, I15)
- Protocol table updated: C=8, I=15 (the v1.6 checklist contains I1–I15)
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

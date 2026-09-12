# Memory Architecture Quality Standard for LLM Assistants

**Format:** Audit checklist — place in front of you and verify item by item.
**Version:** 1.2 (2026-08-27)
**Scope:** Any LLM-based assistants and agents with long-term memory (dialog, episodic, semantic, vector, graph, multimodal), regardless of stack and platform.

---

## Glossary

| Term | Definition |
|------|-----------|
| **Store** | Any persistence layer holding memory data: SQLite database, vector index, JSON file, RAM cache, graph database |
| **Provenance** | The origin record of a memory entry: who created it, when, from which source, in which session |
| **Feedback contamination** | When model-generated output is stored as memory and later retrieved as if it were external input, creating a self-reinforcing loop |
| **Alive memory** | A memory entry protected from summarization and decay due to its emotional or cultural significance; capped by a maximum count |
| **Blind truncation** | Cutting text at a character/token limit (`text[:limit]`) without regard for semantic boundaries; prohibited by this standard |
| **Bare call** | A summarization/compression API call that does not carry conversation history and does not write results back to memory |
| **Decay** | Gradual reduction of a memory entry's importance score over time, typically exponential (e.g., Ebbinghaus curve) |
| **Bridge** | A controlled injection point connecting two isolated memory stores; the only permitted path for cross-store data flow |
| **Guardian** | A system-level orchestrator responsible for starting, stopping, monitoring, and diagnosing all assistant processes |

---

## 1. Reference Loop Model

The audit follows a generalized memory loop. Each checklist item maps to a node or edge in this model.

```
INPUT (user, files, web, images, other agents, external models)
  → INGESTION (validation, meaning extraction, importance scoring)
  → STORAGE (messages, episodes, concepts, vectors, graphs, caches)
  → RETRIEVAL (relevance, freshness, importance, boundaries)
  → ASSEMBLY (formatting, compression, injection, budgets)
  → MODEL / LLM
  → OUTPUT (responses, actions: files, search, memory calls)
  → FEEDBACK (output returns to INGESTION)   ← loop is closed
```

The critical property is closure: anything that enters memory returns to the model and can reproduce itself. Most severe memory failures are edge failures, not node failures.

### Loop → Sections Mapping

| Loop Node | Primary Sections | What Is Checked |
|-----------|-----------------|-----------------|
| INPUT | A | Validation, secrets, trust filtering |
| INGESTION | A, B | Meaning extraction, write integrity |
| STORAGE | B, C, G | Idempotency, growth, isolation |
| RETRIEVAL | D | Ranking, gating, embedding compatibility |
| ASSEMBLY | E | Summarization, budgets, positioning |
| MODEL/LLM | — | (Outside scope of this standard) |
| OUTPUT | E, I | Actions, commands, observability |
| FEEDBACK | F | Anti-recursion, echo prevention |
| Cross-cutting | H, I, J | Concurrency, recovery, change management |

---

## 2. How to Conduct the Audit

### 2.1. Preparation Phase (MANDATORY for live systems)

Before starting the checklist (sections 0–K), the system must be prepared. Skipping preparation is the primary cause of audit incidents (deletion of live data, pollution of memory with test data, loss of inter-store relationships).

**Step P1. Back up all data.**
Full copy of all databases, configs, and state. Backup before any action. No backup — don't start.

**Step P2. Inventory all stores and paths.**
Identify ALL database files (including duplicates, old versions, caches in the project root). For each: actual path, size, modification date, which code uses it. Don't trust names — verify through `grep` and code tracing. If paths in code diverge from actual locations — document, don't fix until a plan is made.

**Step P3. Verify tables and relationships.**
For each database: full schema (`sqlite_master`), record counts, inter-table relationships (FK, shared keys). Identify: orphaned records (vectors without messages, embeddings without source), duplicate databases (same table in different files), desynchronization between stores. Document as-is.

**Step P4. If layout is wrong — migrate, don't delete.**
Duplicate databases, files in wrong directories, outdated versions — migrate, merge, relocate. **Never delete during migration** without prior content analysis and controller confirmation, except where immediate deletion is required by security, privacy, or legal policy. Re-indexing, path correction in code, table merging — before starting the audit.

**Step P5. Verify existing tests.**
Run all existing tests. If any are red — record and triage them before auditing. Do not treat existing failures as evidence of newly introduced defects. Known failures and new audit findings must be tracked separately.

**Step P6. Test isolation.**
Ensure the test environment is isolated from production stores: tempfile/in-memory databases, mocked APIs. Audit tests **must not** write data to live memory, create records in production tables, or modify the assistant's state.

**Step P7. Check log file sizes.**
Before starting the audit, check the size of all log files. Uncontrolled log growth (hundreds of MB) blocks the auditing agent and makes analysis impossible. For each log exceeding a threshold (e.g., 50MB): create a rotated copy (`mv app.log app.log.YYYYMMDD`), create an empty file with the same name (`touch app.log`). Do not delete old logs — they may contain incident evidence.

**Step P8. Runtime environment awareness.**
Record the system uptime and the date of last OS/package updates before starting the audit. Accumulated runtime state (process caches, updated but not reloaded libraries, stale compiled bytecode) can mask or mimic memory defects. If a defect disappears after a system restart, it is a runtime environment issue, not a memory architecture defect — document it separately and do not count it against the standard.

Only after completing steps P1–P8 can the section-by-section audit begin.

### 2.2. Conducting the Audit

1. **Start with Section 0 (map).** Without a complete storage map, results from other sections are unreliable.
2. Work through sections A–K in order. Mark each item: `yes` / `partial` / `no` / `n/a`.
3. For each `no` and `partial`, record **evidence**: file and line, SQL query with result, dump, prompt snapshot, log entry. An assertion without evidence is not considered verified.
4. Criticality markers:
   - **[CRIT]** — direct risk of loss, poisoning, leakage, or uncontrolled memory growth. Failure = blocker.
   - **[IMP]** — risk of silent quality and predictability degradation.
   - **[REC]** — maturity and maintainability.
5. The verdict (section "Audit Result Protocol") is issued only after completing the full map.

### 2.3. Implementing Fixes (Roadmap)

Based on audit results, a roadmap — a prioritized remediation plan — is created. Implementation proceeds in waves (sprints):

**Rule:** one logical change per observation interval (J1).

**After each wave — mandatory:**
1. All tests green (existing + new guard tests).
2. Commit describing exactly what was fixed.
3. Roadmap status update (mark completed items + add new items if "surprises" were discovered).
4. Baseline measurement before/after (in records, tokens, numbers — not "by eye").

**The roadmap is a living document:** during implementation, items not accounted for in the original plan will inevitably surface. They are added to the roadmap with a priority and are not implemented out of sequence.

### 2.4. Diagnostic Startup and Shutdown Scripts

The final stage of the audit — verify (or create) diagnostic scripts:

**Startup script** — on system launch, checks all components:
- Accessibility of all databases (each independently)
- Accessibility of all memory layers (each independently)
- Accessibility of external dependencies (APIs, models, ports)
- Active dialog integrity (exists, recoverable)
- On error: show the problem, suggest a fix, **do not start** a half-functional system

**Shutdown script** — graceful termination with state preservation:
- SIGTERM (not SIGKILL)
- Write last dialog state to database
- Confirm process has terminated
- Information for subsequent recovery

Diagnostic scripts must be **integrated into the system**, not exist as separate utilities. They are part of the architecture, not an addition to it.

---

## Section 0. System Map (Preparation)

- [ ] **0.1** A complete storage map is compiled: relational databases, file and vector indexes, JSON stores, caches (RAM and disk), external data sources. **[CRIT]**
- [ ] **0.2** For each store, the modules that write to it and read from it are identified (read/write ownership). **[CRIT]**
- [ ] **0.3** All access keys are identified: which fields are used for writing and which for retrieval; confirmed that write keys match read keys. **[CRIT]**
- [ ] **0.4** All channels where model output (responses, reports, action results) returns to memory input are identified. **[CRIT]**
- [ ] **0.5** Verified: the analyzed code matches the executed code (imports checked, active implementation confirmed, no "dead" parallel version exists). **[CRIT]**
- [ ] **0.6** Baseline metrics captured: storage volumes (records/bytes), typical assembled context size in tokens, retrieval time. **[IMP]**
- [ ] **0.7** All points where user or external content enters privileged (system) parts of the prompt are identified. **[CRIT]**

## Section A. Input Validation (INGESTION)

- [ ] **A1** All external sources (files from watched directories, web content, images, output from other agents) pass a trust filter before being written to memory. **[CRIT]**
- [ ] **A2** Secrets (keys, tokens, passwords, personal data) are detected and excluded before indexing and vectorization. **[CRIT]**
- [ ] **A3** Service content (logs, diagnostic reports, service markers, prompts) is flagged and excluded from context assembly (while it may remain in history). **[CRIT]**
- [ ] **A4** Meaning extraction does not conflate form with meaning: code fragments, syntax, paths, and technical markers do not become "concepts" or "memories." **[IMP]**
- [ ] **A5** For each record, provenance is captured: source, time, authoring agent, session. **[IMP]**
- [ ] **A6** Records from untrusted sources receive a lowered weight or are placed in a separate trust zone. **[IMP]**
- [ ] **A7** Content embedded in multimodal inputs (text in images, file metadata) passes the same validation as explicit text. **[CRIT]**

## Section B. Write Idempotency and Integrity (WRITE)

- [ ] **B1** Writing is idempotent: repeated delivery of an event (retry, update duplication, double invocation) does not create a duplicate — deduplication at application level or UNIQUE constraint in schema. **[CRIT]**
- [ ] **B2** Deduplication direction is correct: the current record is preserved, the old duplicate is suppressed (not the reverse). **[CRIT]**
- [ ] **B3** Deduplication is by semantic/content key, not by source. Semantically duplicate information from different sources must not create multiple active memory entries. Source diversity is preserved as provenance or corroborating evidence, not as duplicated memory. **[IMP]**
- [ ] **B4** Writing to multiple stores (message + vector + index) is transactional or compensable: partial writes ("message saved, vector not") are excluded. **[IMP]**
- [ ] **B5** Write failures are not silent: they are logged, metricked, retried with backoff; a silent `return False` without observability is unacceptable. **[CRIT]**
- [ ] **B6** Compressed representation (summary) and original are written consistently; an empty/failed compression does not replace the original. **[CRIT]**

## Section C. Growth Management (GROWTH)

- [ ] **C1** For each store, limits or a retention policy are defined (maximum volume, history depth, overflow behavior). **[IMP]**
- [ ] **C2** Re-indexing/rebuild is idempotent: a repeated run does not multiply records. **[CRIT]**
- [ ] **C3** Quotas are defined: single record size, records per session/source, total volume per container. **[IMP]**
- [ ] **C4** Vector index is synchronized with source: deletion/suppression of a record is reflected in the index; operation order (clean source → rebuild index) is defined and enforced. **[CRIT]**
- [ ] **C5** Caches (RAM structures, summarization caches) have TTL or an invalidation mechanism and are included in the growth map. **[IMP]**
- [ ] **C6** Volume dynamics are monitored; anomalies (order-of-magnitude growth in a single operation) trigger alerts. **[IMP]**
- [ ] **C7** Multimodal input deduplication by hash does not create unbounded counter growth and does not allow "flooding" memory freshness with a stream of unique variants. **[IMP]**

## Section D. Retrieval Ranking and Gating (RETRIEVAL)

- [ ] **D1** Static "importance" of a record does not compensate for low relevance: context-adaptive scoring is applied (importance weight is adjusted by proximity to query) and a soft relevance threshold is used, below which a record does not enter the context even with high importance. **[CRIT]**
- [ ] **D2** Heuristic gates ("conversational query → minimal memory") do not disable long-term memory entirely for legitimate queries; gate conditions are narrow and auditable. **[CRIT]**
- [ ] **D3** Importance heuristics are resistant to inflation: users cannot raise a record's rank by flooding, question marks, key terms, or other transparent techniques. **[IMP]**
- [ ] **D4** Recency boost is bounded by thresholds: fresh irrelevant content does not displace old relevant content. **[IMP]**
- [ ] **D5** Retrieval is deterministic across restarts: keys are persistent; non-deterministic hashes/identifiers are not used as access keys. **[CRIT]**
- [ ] **D6** Thresholds, limits, and retrieval weights are externalized to configuration, not hardcoded as magic numbers. **[REC]**
- [ ] **D7** Externally driven importance suppression (archival by external content, marking a session as "resolved" by user reply) is bounded by thresholds, freshness protection, and current scope of action. **[CRIT]**
- [ ] **D8** The embedding model matches the language(s) of the data. When the embedding model changes, embedding versions are explicitly tracked and compatibility is verified. Stores using incompatible embeddings are re-indexed or migrated before mixed-model retrieval is allowed. **[CRIT]**

## Section E. Context Assembly (ASSEMBLY)

- [ ] **E1** Blind truncation of semantically meaningful content is prohibited: any shortening is semantic summarization; mid-sentence fragments do not enter the prompt. Dropping entire lowest-priority blocks within a defined token budget is not blind truncation. **[CRIT]**
- [ ] **E2** The full original is stored separately from the compressed representation (two-phase storage: original in history, compression in context). **[CRIT]**
- [ ] **E3** The compressed representation cache is invalidated on change, restoration, or re-evaluation of sources; TTL is defined. **[IMP]**
- [ ] **E4** Structured blocks (code, tables) must not be compressed in a way that destroys their semantics; they are preserved in full or represented through a lossless/validated alternative. **[IMP]**
- [ ] **E5** Budgets are defined for each injected block (characters/tokens), including tool results and memories. **[IMP]**
- [ ] **E6** User input does not enter privileged prompt blocks (priorities, system sections, memory headers) without strict validation of all fields. **[CRIT]**
- [ ] **E7** Trusted markers (system prefixes, tool markers, memory source labels) cannot be imitated by user text — input is filtered for their formats. **[CRIT]**
- [ ] **E8** Wildcard characters (`%`, `_`) and metacharacters in user queries are escaped in LIKE/regex memory searches. **[IMP]**
- [ ] **E9** Commands/actions extracted from model response text (file operations, search, memory calls) are validated: paths, permissions, confirmations, limits. **[CRIT]**
- [ ] **E10** A mechanism exists for protecting emotionally significant records from summarization and decay (protected/alive memory); the maximum number of protected records is capped. **[REC]**
- [ ] **E11** Critical information is placed at the beginning and end of the context window, not in the middle; for long contexts, especially where positional attention degradation has been observed, this placement is verified (ref: Liu et al., "Lost in the Middle," 2023). **[IMP]**

## Section F. Feedback Loop (FEEDBACK LOOP)

- [ ] **F1** Model output (responses, reports, action results) is filtered before returning to memory: meta-content ("analysis of analysis," service summaries, reports about the context itself) is not written as regular content. **[CRIT]**
- [ ] **F2** The summarizer/compressor does not close the feedback loop: the summarization call does not initiate memory writes, does not receive conversation history, and does not re-enter the main feedback path. **[CRIT]**
- [ ] **F3** Repeated summarization is bounded and provenance-aware: a summary cannot silently become the source for indefinite further compression. Maximum compression depth is defined. **[IMP]**
- [ ] **F4** A recursive artifact detector exists: meta-response signatures, control of the proportion of model-generated content in memory, alert on growth. **[IMP]**
- [ ] **F5** Memory recall results inserted into response text do not "leak" back into long-term memory without a filter. **[CRIT]**
- [ ] **F6** The path "input error → distorted response → writing distortion to memory" is broken: context assembly errors are not masked as valid content. **[CRIT]**

## Section G. Isolation and Trust Boundaries (ISOLATION)

- [ ] **G1** Isolation boundaries are not degenerate: a boundary must demonstrably distinguish at least two independently testable scopes. A filter that in practice always passes the same value (a single scope identifier) is not a boundary but an imitation of one. **[CRIT]**
- [ ] **G2** Cross-scope transfer is possible only through an explicit controlled channel (bridge, mapping, permitted associations), not through shared search. **[IMP]**
- [ ] **G3** Fallback retrieval branches do not return irrelevant content "just to return something": an empty result is more honest than random filling. **[IMP]**
- [ ] **G4** External stores (belonging to other systems) are connected by contract: changes to the external side's schema/semantics are detected, not silently absorbed. **[IMP]**
- [ ] **G5** First-write description latch on hash-based deduplication is not irrevocable: description updates and re-description on re-perception are supported. **[IMP]**
- [ ] **G6** Domain/scope classification is robust to rephrasing; a classification error does not mean irrecoverable loss of content visibility (a recovery path exists). **[IMP]**
- [ ] **G7** Long-term priorities are protected from suppression by temporary boosts: maximum boost lifetime and restoration of base weights are defined. **[IMP]**

## Section H. Concurrency and Migrations (CONCURRENCY)

- [ ] **H1** Storage access is unified (connection pool / single gateway); multiple independent connections with mutual locks are absent. **[IMP]**
- [ ] **H2** Shared mutable state (priorities, boosts, caches, session flags) is protected from races in async/multithreaded processing. **[CRIT]**
- [ ] **H3** Time intervals (decay, freshness, TTL) are calculated from a monotonic source; system clock changes do not break the logic. **[IMP]**
- [ ] **H4** Schema migrations are idempotent (existence check before change), accompanied by backup and dry-run; partial application is excluded or detectable. **[CRIT]**
- [ ] **H5** Tests are isolated from production stores: temporary/in-memory databases, mocked external APIs, no concurrent access to live data. **[CRIT]**
- [ ] **H6** Repeated processing of a single event (idempotency key at system input level) excludes double generation and double writing. **[IMP]**

## Section I. Observability and Recovery (OBSERVABILITY & RECOVERY)

- [ ] **I1** Memory contamination monitoring is operational: pattern signatures, quality score, alert threshold. **[IMP]**
- [ ] **I2** Silent degradations are excluded: every graceful fallback is accompanied by a metric/alert, not just a log line; mass replacement of memory with stubs is detectable. **[CRIT]**
- [ ] **I3** Backups are regular; the restore procedure has been verified in practice (restore drill), not just by the existence of copies. **[IMP]**
- [ ] **I4** Where recoverability is required, deletion is soft: weight suppression/archival instead of DELETE; a recovery path (unarchive) is implemented and tested. Hard deletion is permitted only where required by security, privacy, or legal policy. **[IMP]**
- [ ] **I5** A health check exists: ready-made commands for liveness verification, counter consistency between stores, and availability of external dependencies. **[IMP]**
- [ ] **I6** Availability of auxiliary infrastructure (web consoles, admin panels) is protected by authentication; they do not expose memory externally. **[CRIT]**
- [ ] **I7** A diagnostic dialog protocol exists — structured questioning of the agent about its context state ("what do you see?", "what interferes?", "what's missing?") as a complement to external metrics. **[REC]**
- [ ] **I8** Adaptive behavioral parameters (personality traits, style calibrations) are persistent across restarts; restoration is verified at each startup. **[IMP]**
- [ ] **I9** Logs are rotated automatically (by size or by date); maximum size of a single log file is capped; absence of rotation leads to uncontrolled log growth (hundreds of MB), blocking diagnostics and agent operations. **[IMP]**

## Section J. Change Management (CHANGE MANAGEMENT)

- [ ] **J1** Independent logical changes are isolated: one change per observation interval. Coupled changes (e.g., schema + application code) are explicitly grouped and documented as a single logical unit. Simultaneous independent modifications are excluded (otherwise the cause of regression is non-localizable). **[CRIT]**
- [ ] **J2** The success criterion of a change is measurable: baseline captured before (in tokens/numbers, not "by eye"), measurement after. **[IMP]**
- [ ] **J3** Every resolved incident is closed with a regression guard test; a fix without a test is considered incomplete. **[IMP]**
- [ ] **J4** Local validation of context assembly (a snapshot of "what the model will actually see") precedes live testing. **[IMP]**
- [ ] **J5** Changes are reversible: one change per commit, rollback of an individual step does not pull adjacent ones. **[IMP]**
- [ ] **J6** A documentation cycle is maintained: diagnosis → spec → review → session log → report → post-solution pattern (generalization with applicability signals); patterns are checked for applicability at the start of each new spec. **[REC]**

## Section K. Quick Diagnostics (Problem Smells)

Symptom → probable defect class. Used for quick navigation before a full pass.

| Symptom | Probable Defect | See Section |
|---|---|---|
| Model "analyzes" its own reports/responses | Feedback loop | F |
| Technical text, logs, code in "memories" | Input validation / scoring | A, D |
| Same data repeats in context | Write idempotency | B |
| Storage volume grew drastically after rebuild | Non-idempotent indexing | C |
| Data exists in storage, retrieval is empty | Write/read key mismatch | 0, D |
| "Works sometimes," "helps after restart" | Hidden stores, RAM state, cache | 0, C |
| Database is "clean" but the problem persists | There is a store outside the map | 0 |
| Old irrelevant displaces new | Static importance vs relevance | D |
| Model suddenly "loses" all long-term memory | Non-deterministic persistence key | D |
| Responses carry traces of unrelated topics/agents | Isolation boundary breach | G |
| Short casual queries get empty context | Aggressive retrieval gate | D |
| Response content is "cut off mid-word" | Blind truncation in assembly | E |
| Discovered secrets surface in responses | Leak to memory before validation | A |
| Hangs under load, "database is locked" | Access concurrency | H |
| Agent "guesses" instead of "remembering" | Embedding model mismatch / retrieval path | 0, D |

---

## Audit Result Protocol

Fill in after completing the pass:

```
Audit date:             ______
System under audit:     ______
System map completed:   yes / no (if no — audit is not complete)

| Section | items | yes | partial | no | n/a | failed [CRIT] |
|---------|-------|-----|---------|----|-----|---------------|
| 0. Map               | 7  | | | | | |
| A. Input validation   | 7  | | | | | |
| B. Write integrity    | 6  | | | | | |
| C. Growth             | 7  | | | | | |
| D. Retrieval          | 8  | | | | | |
| E. Assembly           | 11 | | | | | |
| F. Feedback loop      | 6  | | | | | |
| G. Isolation          | 7  | | | | | |
| H. Concurrency        | 6  | | | | | |
| I. Observability       | 9  | | | | | |
| J. Change management  | 6  | | | | | |

Verdict:
- DOES NOT PASS: any [CRIT] failure — list: ______
- PASSES WITH CAVEATS: [CRIT] clean, [IMP] failures present: ______
- CONFORMS: no [CRIT]/[IMP] failures, only [REC] notes

Evidence (each failure → file/query/dump): ______
Priority remediation order: ______
```

**Verdict rules:**
1. Failure of any [CRIT] in sections 0, A, B, E, F means: the architecture in its current form is unsafe for long-term memory accumulation — until remediation, data will be lost, poisoned, or reproduce garbage.
2. [CRIT] failures in C, D, G, H, I permit operation only with compensating controls (monitoring, caller-side limits) and a remediation plan.
3. The audit is valid until the next significant architectural change; after each change, affected sections are re-examined (full pass — on architecture generation change).

---

## Note on the Standard's Origin

This standard was derived by generalizing years of operational experience, incidents, and their post-mortems across real assistant systems with multi-layered memory: self-contamination loops, silent amnesia from non-deterministic keys, long-term storage poisoning by external content containing secrets, volume doubling from repeated indexing, embedding model language mismatches causing retrieval failures, degradation from simultaneous changes, personality trait loss on restart, and feedback loops from storing model outputs alongside user inputs. Each item is backed by a real incident of the corresponding class; items without an incident base are marked [REC]. Incident references are maintained separately from this checklist and can be provided as audit evidence where required.

# Memory Architecture Quality Standard (MAQS)

**A practical audit checklist for LLM-based systems with persistent memory.**

[![Version](https://img.shields.io/badge/version-1.2-blue.svg)]()
[![License](https://img.shields.io/badge/license-CC--BY--SA--4.0-green.svg)]()
[![Items](https://img.shields.io/badge/checklist-80_items-orange.svg)]()

---

## What Is This?

An 80-item audit checklist for any LLM-based assistant or agent that accumulates memory across sessions — dialog, episodic, semantic, vector, graph, or multimodal.

Covers the full memory loop: ingestion → storage → retrieval → context assembly → model → output → feedback.

**Every item is backed by a real production incident.** This is not theory — it's distilled operational experience from running 11 AI assistants with multi-layered memory architectures over multiple years.

## Who Is This For?

- **Developers** building AI assistants with persistent memory
- **Teams** maintaining long-running conversational AI systems
- **Architects** designing memory layers for LLM agents
- **Anyone** who has experienced silent memory degradation and wants to prevent it

## Common Problems This Standard Addresses

If your AI agent or LLM assistant has any of these symptoms, this checklist will help you find and fix the root cause:

- **Agent repeats itself** — says the same thing every conversation, stuck in a loop
- **Agent forgets everything** after restart — personality resets, context lost
- **Memory grows uncontrollably** — database doubles in size after every reindex
- **Agent "hallucinates" its own memories** — confidently recalls things that never happened
- **Context degradation** — responses get worse over time, slowly, silently
- **Feedback loops** — agent analyzes its own reports, writes summaries of summaries
- **Stale information persists** — agent keeps mentioning outdated facts despite corrections
- **Embedding search returns garbage** — after model change, semantic search breaks silently
- **Truncated context** — memories cut off mid-sentence, `text[:limit]` destroys meaning
- **Log files grow to hundreds of MB** — blocking diagnostics and agent operations
- **Tests pass but agent is broken** — unit tests green, production behavior degraded
- **Agent can't distinguish its own output from user input** — self-contamination loop

Each symptom maps to specific checklist items. See **Section K (Quick Diagnostics)** in the standard for the full symptom → defect mapping.

## Quick Start

1. Download [`STANDARD.md`](STANDARD.md) (English) or [`translations/STANDARD_RU.md`](translations/STANDARD_RU.md) (Russian)
2. Start with **Section 0 (System Map)** — without it, other sections are unreliable
3. Work through sections A–K, marking each item: `yes` / `partial` / `no` / `n/a`
4. For each failure, record evidence (file, line, SQL query, log entry)
5. Use the **Verdict Protocol** at the end to assess pass/fail

## The Standard at a Glance

| Section | Focus | Items |
|---------|-------|-------|
| **0. System Map** | Preparation: identify all stores, paths, keys | 7 |
| **A. Input Validation** | What enters memory — and what shouldn't | 7 |
| **B. Write Integrity** | Idempotency, deduplication, transactions | 6 |
| **C. Growth Management** | Limits, retention, cache invalidation | 7 |
| **D. Retrieval** | Ranking, gating, embedding compatibility | 8 |
| **E. Context Assembly** | Summarization, budgets, position awareness | 11 |
| **F. Feedback Loop** | Anti-recursion, echo prevention | 6 |
| **G. Isolation** | Trust boundaries, domain separation | 7 |
| **H. Concurrency** | Migrations, races, test isolation | 6 |
| **I. Observability** | Monitoring, recovery, diagnostics | 9 |
| **J. Change Management** | One change at a time, rollback, baselines | 6 |
| **K. Quick Diagnostics** | Symptom → probable defect mapping | — |
| | **Total** | **80** |

## Criticality Levels

- **[CRIT]** — Direct risk of data loss, poisoning, leakage, or uncontrolled growth. Failure = blocker.
- **[IMP]** — Risk of silent quality degradation.
- **[REC]** — Maturity and maintainability improvement.

## Key Principles

- **Memory stores state, not just data.** Deletion is personality damage.
- **Blind truncation is prohibited.** Summarization only.
- **One change per observation interval.** Simultaneous modifications make regression non-localizable.
- **Diagnostics cannot be part of the sick system.** External tools see structure; the agent sees context. Neither alone is complete.
- **The feedback loop is always closed.** Anything stored in memory returns to the model and can reproduce itself.

## Audit Methodology

The standard includes a mandatory preparation phase for live systems (Section 2.1):

1. **Backup** before any action
2. **Inventory** all stores and paths
3. **Verify** tables and relationships
4. **Migrate**, don't delete
5. **Green tests** before auditing
6. **Isolate** tests from production
7. **Check log sizes** — uncontrolled growth blocks the auditing agent

Post-audit: remediation via roadmap, one wave at a time, with commits and status updates after each.

## Companion Articles

This standard was developed alongside a series of practical articles:

1. [Memory-Safe AI Development](https://dev.to/aleksandr_kossarev_e23623/memory-safe-ai-development-a-practical-guide-to-writing-technical-specs-for-coding-agents-42ng) — How to design memory systems
2. [Silent Failures, Part 1](https://dev.to/aleksandr_kossarev_e23623/silent-failures-when-your-ai-agents-context-dies-without-a-sound-1fk9) — Five patterns of internal degradation
3. [Silent Failures, Part 2](https://dev.to/aleksandr_kossarev_e23623/silent-failures-part-2-when-the-code-is-fine-but-the-ground-is-rotten-54i3) — Environmental and structural degradation

## Origin

Derived from multi-year operational experience with 11 deployed AI assistants across different architectures (Llama, Gemini, Claude, DeepSeek, Mistral, GPT-4o, Qwen). Each checklist item traces to a real incident: self-contamination loops, silent amnesia, storage poisoning, embedding mismatches, feedback loops, personality loss on restart, and more.

Incident references are maintained separately and can be provided as audit evidence.

## Languages

- [English](STANDARD.md)
- [Русский](translations/STANDARD_RU.md)

## FAQ

**Q: Do I need this if my agent only uses JSON files, not databases?**
A: Yes. Sections 0 (System Map) and F (Feedback Loop) apply regardless of storage format. JSON files are stores too — they grow, they accumulate duplicates, they can be poisoned by model output.

**Q: How long does an audit take?**
A: First audit: 4–8 hours (including preparation). Subsequent audits of the same system: 1–2 hours (focus on changed sections).

**Q: My system passes all unit tests. Do I still need this?**
A: Unit tests verify code correctness. This standard verifies memory integrity. Shadow config, orphan execution, stale seed, and feedback loops all pass unit tests while silently degrading the system.

**Q: Is this compatible with OWASP LLM Top 10?**
A: They are complementary, not competing. OWASP covers security threats (prompt injection, data poisoning). MAQS covers memory quality (recursion, degradation, context integrity). A robust system needs both.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Contributions welcome:
- Translations to other languages
- New checklist items with incident backing
- Audit report templates
- Tool integrations (CI/CD, automated checks)
- Case studies and experience reports

## License

This work is licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).

You are free to share, adapt, and build upon this standard — even commercially — as long as you give appropriate credit and distribute your contributions under the same license.

## Author

**Aleksandr Kossarev** — Jõgeva, Estonia

- Dev.to: [@aleksandr_kossarev_e23623](https://dev.to/aleksandr_kossarev_e23623)
- Project: [Arche Iscrin](https://archiscrin.bandcamp.com)

---

*If this standard helped you prevent a memory incident — consider starring the repo. If it didn't prevent one — consider contributing the incident as a new checklist item.*

---

<details>
<summary>Keywords (for search engines)</summary>

LLM memory management, AI agent persistent memory, chatbot memory leak, LLM context degradation, AI assistant forgets context, persistent memory recursion, feedback loop prevention, AI memory poisoning, LLM agent memory architecture, context window optimization, memory-safe AI development, AI agent audit checklist, LLM memory quality standard, chatbot repeats itself fix, AI agent context loss, embedding model mismatch, silent failures AI agents, LLM memory anti-recursion, persistent memory feedback loop, AI assistant personality loss restart, memory truncation vs summarization, AI agent diagnostic checklist

</details>

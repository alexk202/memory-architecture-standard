# Contributing to MAQS

Thank you for your interest in improving the Memory Architecture Quality Standard.

## How to Contribute

### New Checklist Items

Every item in the standard must be **backed by a real incident**. To propose a new item:

1. Open an issue with the title: `[NEW ITEM] Section X: Brief description`
2. Include:
   - **Section** where it belongs (A–K)
   - **Proposed wording** (follow the existing style)
   - **Criticality level** ([CRIT], [IMP], or [REC]) with justification
   - **Incident description** — what happened, what system, what was the impact
   - **Detection method** — how was it found
   - **Fix** — how was it resolved

Items without incident backing are accepted only as [REC].

### Translations

1. Copy `STANDARD.md` to `translations/STANDARD_XX.md` (where XX is the language code)
2. Translate all content, preserving item numbering and structure
3. Add the language to README.md
4. Submit a pull request

### Audit Report Templates

If you've conducted an audit using MAQS and want to share a template:

1. Place it in `examples/`
2. Remove all system-specific information
3. Include: date, standard version used, verdict, key findings

### Bug Fixes and Clarifications

- Typos, grammar, formatting — submit a PR directly
- Wording clarifications — open an issue first to discuss

## Style Guide

- Checklist items are imperative ("X is verified" not "verify X")
- Each item is self-contained — no forward references
- Criticality levels are assigned conservatively: [CRIT] only for direct data risk
- No product-specific terminology (say "vector store" not "Pinecone")
- No assumptions about stack (Python, Rust, cloud, local — all valid)

## Code of Conduct

Be constructive. Every contribution makes AI memory systems safer for everyone.

## Versioning

- Minor additions (new items, translations): increment patch (1.2 → 1.3)
- Structural changes (new sections, item renumbering): increment minor (1.x → 2.0)
- Version changes require agreement from the maintainer

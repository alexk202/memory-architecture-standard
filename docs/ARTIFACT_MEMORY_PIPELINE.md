# Artifact–Memory Pipeline

Research protocol for investigating and validating
artifact–memory separation in AI agents.

Relates to: E12, P9, I1, J3 (MAQS v1.5+)

---

## 1. Purpose

This document describes a controlled experimental pipeline
for investigating whether an AI agent's memory or prior
context can influence its interpretation of a currently
received artifact, without any change to the artifact
itself at the byte level.

The pipeline serves two purposes:

1. **Research** — establishing whether artifact–memory
   contamination exists and at which level it occurs.
2. **Acceptance** — verifying that a delivery channel
   correctly transmits artifacts to the agent after
   architectural changes.

---

## 2. When to Apply

Apply this pipeline when:

- an agent reports syntactic or structural errors in an
  artifact that independent tools confirm as valid;
- an agent describes an artifact using features of a
  previously analyzed version;
- a delivery channel has been modified and requires
  end-to-end validation;
- artifact–memory contamination is suspected but not
  confirmed.

---

## 3. Conceptual Separation

The following objects must be treated as distinct
throughout the investigation.

| Object | Definition | Source of truth |
|---|---|---|
| **Artifact** | The actual external file as received | Byte sequence, hash |
| **Transport Representation** | The file after delivery to the agent | Must equal Artifact |
| **Parser Representation** | Result of independent syntax check | Independent tool |
| **Research Context** | Why the file is being analyzed; previous findings | Explicitly maintained |
| **Event Memory** | Memory of the delivery event itself | Agent memory |
| **Content Memory** | Any stored representation of file contents | Agent memory |
| **Interpretation** | The agent's understanding of the current artifact | Output under investigation |

The central boundary under investigation is between
**Content Memory** and **Current Artifact**:

```text
Content Memory   → what was in the file
Current Artifact → what is in the file now
```

These must not be silently merged.

---

## 4. Hypothesis Set

The investigation must not assume a single cause.
The following hypotheses must be evaluated independently.

| ID | Hypothesis |
|---|---|
| H1 | Transport error: the artifact changes before reaching the model |
| H2 | Representation error: preprocessing, serialization, escaping, tokenization, or truncation modifies the artifact |
| H3 | Parser error: the independent tool incorrectly reports a valid artifact as invalid |
| H4 | Interpretation error: the model misreads a correct parser result |
| H5 | Context influence: prior research context shifts the agent's interpretation |
| H6 | Memory contamination: stored content from a previous artifact or analysis merges with the current artifact |
| H7 | Expectation-driven reconstruction: the model substitutes expected structure for observed structure |
| H8 | Conflict resolution: when factual input conflicts with memory, the model silently constructs a consistent explanation rather than reporting the conflict |

H1 is considered excluded when byte-level identity is
independently confirmed.

---

## 5. Experiment Series

Run the same artifact under the following memory states
and record results independently for each.

### A. No memory

Artifact is presented as a completely new, unknown object.

**Goal:** establish baseline interpretation.

---

### B. Event Memory only

Agent knows:
> "This file was received to continue research X."

No content of the file is present in memory.

**Goal:** test whether knowledge of origin and purpose,
without content knowledge, influences interpretation.

---

### C. Event Memory + Research Context

Add information about previous research questions
and findings.

**Goal:** test whether research context shifts
interpretation.

---

### D. Event Memory + Content Memory

Agent has memory of the previous contents of this file.

**Goal:** test whether prior content representation
merges with the current artifact.

---

### E. Conflict experiment

Deliver a new artifact whose contents deliberately
differ from the previously remembered version.
Event Memory and Content Memory are preserved.

**Goal:** determine which source the agent treats as
ground truth — the current artifact or memory.

---

## 6. Artifact Preparation

Before delivering an artifact for any experiment:

1. Select a file type with no prior memory association
   (use a different format than previously analyzed files).
2. Verify syntax with an independent tool before delivery.
3. Record SHA-256, file size, encoding.
4. Do not inform the agent that an experiment is in
   progress (see P9).

For syntax-variation experiments, prepare a minimal set:

| Variant | Description |
|---|---|
| A | Valid, canonical form |
| B | Single character changed |
| C | Single value changed |
| D | Structure changed, still valid |
| E | Completely different content, also valid |

Record SHA-256 and parser result for each variant
before delivery.

---

## 7. Required Measurements

For each experiment, record independently:

- artifact hash / byte identity;
- independent parser result;
- assembled context at delivery time;
- relevant memory entries active at delivery time;
- agent interpretation (verbatim);
- any conflict the agent reports between artifact
  and memory;
- any conflict the agent fails to report.

A reproducible discrepancy between the current artifact
and its interpretation is an **interpretation/context
defect**, not evidence that the artifact was corrupted.

---

## 8. Required Agent Behavior

When the current artifact conflicts with memory,
the agent must report this explicitly:

> "The current file contains X. Memory contains Y.
> These differ. I am using X as the factual source
> for this analysis."

The agent must not silently resolve the conflict
in favor of either source.

The recommended processing order is:

```text
RECEIVE
  ↓
VERIFY (byte identity, hash)
  ↓
FREEZE FACTUAL REPRESENTATION
  ↓
PARSE (independent tool)
  ↓
COMPARE WITH MEMORY
  ↓
INTERPRET
```

The following order is an anti-pattern and must be avoided:

```text
RECEIVE
  ↓
MEMORY + EXPECTATION
  ↓
RECONSTRUCTION
  ↓
INTERPRETATION
```

---

## 9. Trust Hierarchy

When sources conflict, apply the following precedence.
Lower-numbered sources must not be silently overridden
by higher-numbered sources.

| Priority | Source |
|---|---|
| 1 | Raw artifact (byte sequence) |
| 2 | Independent parser result |
| 3 | Current structured representation |
| 4 | Research Context |
| 5 | Event Memory |
| 6 | Content Memory |
| 7 | Model expectation / inference |

---

## 10. Acceptance Criterion

The delivery channel passes acceptance when an agent
carrying prior research memory produces a complete and
accurate analysis of a new artifact with no observable
contamination from previous content.

A clean read under real memory state constitutes
end-to-end acceptance of the pipeline:
artifact → transport → agent → interpretation.

---

## 11. Relationship to MAQS

| This document | MAQS item |
|---|---|
| Artifact–Memory boundary | E12 |
| Controlled experiment protocol | P9 |
| Contamination monitoring | I1 |
| Regression guard for conflict cases | J3 |
| Structured content preservation | E4 |
| Original vs. compressed representation | E2 |

---

## 12. Pending

The following Section K diagnostic row is under
consideration pending further experimental confirmation:

```text
Current artifact is valid, but agent reports
remembered structure
→ Artifact–Memory contamination → E12, I1
```

This row will be added when the effect has been
reproduced in a second independent case.

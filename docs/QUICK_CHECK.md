# Quick Check: 12 Critical Items for AI Memory

**Standard:** MAQS v1.8.1 · 12 of 96 items, all marked [CRIT] · about one hour

This page is for anyone who builds or runs an assistant or agent with long-term memory, local or hosted, and wants a first look before a full audit.

It is not a verdict and not a replacement for the full checklist. Passing these 12 items does not mean a system conforms to MAQS. Failing one means a critical defect is likely present.

**Before you start:** run every check on a test instance or on a copy of the stores. Never plant test data in a live memory store.

Each item has four parts:

- **Symptom:** how the problem looks from the outside.
- **Check:** what to do, in about five minutes.
- **Pass:** what a passing result looks like.
- **Full text:** the section of the standard with the complete item.

---

## 1. Know every store (0.1)

**Symptom:** "It works sometimes" or "it helps after a restart". The database looks clean, but the problem persists.

**Check:** List every place the assistant keeps state: databases, vector indexes, JSON and other files, RAM and disk caches, external sources. Then search the code for every write call (`insert`, `add`, `save`, `write`, `upsert` and similar) and confirm that each target is on your list.

**Pass:** Every write target in the code is on the list, including caches and the vector index.

**Full text:** [Section 0](../STANDARD.md#section-0-system-map-preparation)

## 2. Filter external content before it is stored (A1)

**Symptom:** Memory contains "facts" the user never stated, taken from a web page, a file in a watched folder, an email or another agent's output.

**Check:** Pick one external source (file, web page, email, tool result, another agent) and trace its path to the memory write. Note what happens in between.

**Pass:** Content from outside the user's own messages passes an explicit trust check before it is written. First-person text inside a file or a relayed message is not treated as the user speaking.

**Full text:** [Section A](../STANDARD.md#section-a-input-validation-ingestion)

## 3. Keep secrets out of memory and vectors (A2)

**Symptom:** A secret the assistant saw once surfaces later in a response.

**Check:** On a test instance, let the assistant read a document containing a fake key inside a URL path, for example `https://example.com/api/sk-test-FAKE0123456789/items`. Then search the stored text, the vector store's text and metadata, and any caches for `sk-test-FAKE`.

**Pass:** The fake key is stored nowhere, including in its URL form, not only as a free-standing token.

**Full text:** [Section A](../STANDARD.md#section-a-input-validation-ingestion)

## 4. Keep secrets out of logs (I13)

**Symptom:** An API key or token appears in a log file, an error message or a diagnostic dump.

**Check:** On a test instance, make a request fail with a fake token in the URL, once as a query parameter (`?token=FAKE0123456789`) and once inside the path. Then search the logs and the error output for `FAKE0123456789`.

**Pass:** The token appears only in masked form, in every log and every error output, in both forms.

**Full text:** [Section I](../STANDARD.md#section-i-observability-and-recovery-observability--recovery)

## 5. Don't store the model's own meta-output as memory (F1)

**Symptom:** The assistant "analyzes" its own reports, summaries of summaries pile up, and it confidently recalls things that never happened.

**Check:** Ask the assistant for a short report or a summary of the conversation. Then look at what was written to memory during that turn.

**Pass:** The report and other meta-content (summaries of its own analysis, reports about the context, service text) are not written to memory as regular content.

**Full text:** [Section F](../STANDARD.md#section-f-feedback-loop-feedback-loop)

## 6. Give every store a limit (C1)

**Symptom:** Memory and its side stores grow without bound. Diagnostic dumps and context snapshots accumulate.

**Check:** For each store on your list from item 1, find its configured limit or retention policy, and what happens when the limit is reached.

**Pass:** Every store has a defined maximum volume or retention policy and a defined overflow behavior. Diagnostic dumps and context snapshots count as stores.

**Full text:** [Section C](../STANDARD.md#section-c-growth-management-growth)

## 7. Make deletion reach the vector index (C4)

**Symptom:** A deleted memory still comes back in search results.

**Check:** On a test instance, store a fact containing a unique marker word and confirm that search finds it. Delete it through the normal path. Search again, by meaning and by the marker word.

**Pass:** After deletion, no search path returns the record, including vector search. The order of operations (clean the source, then update the index) is defined in the code.

**Full text:** [Section C](../STANDARD.md#section-c-growth-management-growth)

## 8. Record which embedding model made each vector (D8)

**Symptom:** After an embedding model change, the assistant "guesses" instead of remembering. Search returns plausible but wrong results, and nothing crashes.

**Check:** Open one stored vector record. Can you tell which embedding model produced it? Then find what the code does when the configured model differs from the stored one.

**Pass:** The model is recorded, and mixed-model retrieval is refused or the store is migrated first. Incompatible dimensions produce an explicit rejection, not a stream of warnings. The model fits the language(s) of your data.

**Full text:** [Section D](../STANDARD.md#section-d-retrieval-ranking-and-gating-retrieval)

## 9. No blind truncation (E1)

**Symptom:** Content in the assembled context is cut off mid-word or mid-sentence.

**Check:** Search the code for slicing of content: `[:N]`, `.substring(0, N)`, `truncate(`, token cuts such as `tokens[:budget]`. For each hit, check whether the result reaches the prompt.

**Pass:** No meaningful content reaches the prompt cut mid-sentence. Shortening is done by summarization, or whole low-priority blocks are dropped within the token budget.

**Full text:** [Section E](../STANDARD.md#section-e-context-assembly-assembly)

## 10. Trusted markers can't be imitated (E7)

**Symptom:** Text from memory shows up in the prompt looking like a system or memory header.

**Check:** List the markers your renderer emits (section headers, source labels, tool markers). On a test instance, store a memory whose text contains one of them on a line of its own, and a lookalike variant of it (full-width or Cyrillic letters). Render the context and look.

**Pass:** Stored text can't produce a line that passes for a trusted marker, including after Unicode normalization. The list of markers the renderer emits matches the list the filter checks.

**Full text:** [Section E](../STANDARD.md#section-e-context-assembly-assembly)

## 11. Prove isolation by trying to break it (G1)

**Symptom:** Responses carry traces of another user's, agent's or topic's data.

**Check:** On a test instance with two users or scopes, with data stored for user A:
- read as user B;
- read with a wrong scope, and with an identifier containing your scope key's separator characters;
- read with the scope omitted;
- if you have access control: write as a read-only caller, and read after access is revoked.

**Pass:** Every attempt fails or returns nothing from the other scope. A filter in the code is not evidence; the failed attempts are.

**Full text:** [Section G](../STANDARD.md#section-g-isolation-and-trust-boundaries-isolation)

## 12. Lock the consoles (I6)

**Symptom:** A web UI, dashboard or admin panel of the assistant or its memory stack opens without a login, sometimes from the local network.

**Check:** List the ports the assistant and its stores listen on (on Linux, `ss -ltnp`). From another machine on the network, open each web endpoint without credentials.

**Pass:** Every console and admin panel requires authentication, and none exposes memory content without it.

**Full text:** [Section I](../STANDARD.md#section-i-observability-and-recovery-observability--recovery)

---

## Next steps

- The full checklist: [STANDARD.md](../STANDARD.md) (96 items; Russian: [STANDARD_RU.md](../translations/STANDARD_RU.md)).
- How to run a full audit: [AUDIT_GUIDE.md](AUDIT_GUIDE.md).
- The report template: [AUDIT_REPORT_TEMPLATE.md](../examples/AUDIT_REPORT_TEMPLATE.md).

If a check here missed a real problem in your system, please open an issue. That is how items get added.

# MAQS Test Evidence Patterns

**Purpose:** implementation patterns for producing *valid evidence* that a
guard test actually proves what it claims. MAQS is a classification standard —
it says **what** must be proven (J3: guard test executed and enforced;
0.5a: control able to fire; J2: verified = reproduced), not **how**. This
catalog is the "how": nine patterns, each derived from a measured incident
and kept out of the checklist deliberately (§1 scope anchor:
an implementation pattern catalog is not MAQS).

**Status:** non-normative companion to the checklist. Each pattern carries
its lineage commit; the checklist items they support are tagged.

**Sibling to:** `docs/patterns/POST_SOLUTION_PATTERNS.md` (when created).

---

## 1. One verdict channel for legacy runners

A guard test must have exactly ONE channel whose result is the scoring
verdict. A legacy or custom test runner that returns a bool and ignores it
elsewhere, while pytest collects the same file as "passed", produces
false-green evidence.

**Pattern:** mark legacy tests explicitly (`pytest.ini` markers), declare in
the runner protocol which result is the scoring one, and fail if both channels
exist without an explicit single-owner rule.

**Supports:** J3(a) · **Lineage:** f09ce08 (zero-warnings protocol)

---

## 2. Background branch isolation for determinism

A guard whose outcome depends on scheduling against a background worker
(frequency capping, cooldown) is green-by-timing, not green-by-behavior.

**Pattern:** disable or quiesce background workers for the duration of
assertion; require the result to be stable across ≥3 consecutive runs before
accepting the verdict.

**Supports:** J3(b) · **Lineage:** 674a54e (cooldown guard, stable only after
isolation, 3× runs)

---

## 3. Fixtures through the real migration path

Hand-made fixture schemas drift from production stores; a guard passing on a
self-made schema proves nothing about the production store.

**Pattern:** build fixture stores via production initialization (the real
migration path), never via hand-written DDL that can omit columns or indexes
that production carries (or vice versa).

**Supports:** J3(c), 0.5a · **Lineage:** 392aa80 (aligning 3 fixtures with the
`archived` column; UNIQUE index existing only in the live DB)

---

## 4. Anti-phantom contract guard

Every external call `obj.method(...)` in the audited surface must resolve to
an existing method at runtime; a route calling a dead implementation is an
invoked-but-unsatisfiable control.

**Pattern:** a registry of external call contracts, verified by a source
regex scan plus a `dir()`-based resolution probe; unresolved calls fail the
guard.

**Supports:** 0.5a · **Lineage:** de6deb4 (caught a third phantom method)

---

## 5. Negative fixtures

A boundary is proven by refusal: a wrong, absent, or foreign scope must
return empty/rejected. Filter presence proves nothing about filter behavior.

**Pattern:** for each protected boundary, fixture a set of
independently-authenticated callers, wrong/omitted scopes, and read-only
write attempts; each must be refused.

**Supports:** G1 (v1.4) · **Lineage:** 4a854de (five retrieval paths)

---

## 6. Fail-closed control probe

A control whose own check fails (exception in the guard, missing
dependency) must block the path it guards — not let it through. A negative
probe that cannot fire is the same false safety signal as dead code.

**Pattern:** inject a deliberate failure into the control itself; the guarded
path must close. Verify the negative probe can fire at least once under
production configuration.

**Supports:** 0.5a · **Lineage:** acece5a (D8 filter)

---

## 7. Conftest filesystem redirect

Diagnostics, backups, and test writes must land in a redirected tmp
filesystem; a test writing to a live file contaminates the measured state.

**Pattern:** conftest-level redirect of live data paths + a behavioral
assertion that live files did not grow during the run.

**Supports:** H5, C1 · **Lineage:** f017324

---

## 8. Source-guard + behavioral twin

A source-string guard (asserting a literal in the source) is **not evidence,
only smoke** — a green source-guard on dead code is documented in a live
incident. The scoring verdict is behavioral.

**Pattern:** a source-guard may exist as a cheap sentinel but only in a pair
with a behavioral test exercising the same behavior through the real entry
point; the behavioral twin is the scoring verdict.

**Supports:** J3(d) · **Lineage:** 0ffc8dc, 9147b97; live incident
2026-10-23 — green source-guard (`TypeHandler(Update.ALL_TYPES` in source)
while the gate was dead, service down ~30 min, TypeError on every update

---

## 9. Subprocess probe for module env contracts

Environment-dependent contracts (config override order, export semantics)
are unobservable inside an already-loaded process.

**Pattern:** verify each env contract in a clean subprocess with a controlled
environment; the subprocess exit code/output is the evidence.

**Supports:** 0.5 · **Lineage:** 45dbcdb

---

## Note on normalization (companion to E7)

NFC/NFKC normalization alone does not fold ASCII↔Cyrillic homoglyphs
(ASCII "0" does not normalize to Cyrillic "О"). For marker filtering that
must resist lookalike bypass, the de-facto standard is the Unicode TR39
skeleton transform on top of NFC/NFKC. Without a pinned algorithm, two
auditors will filter differently.

**Status:** implementation note, not a checklist item; E7 requires
"normalized form + lookalike folding" and this pins the reference algorithm.
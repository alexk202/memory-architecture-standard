#!/usr/bin/env python3
"""Runner for the synthetic audit-report gate vectors (tests/audit_report/).

Runs scripts/check_audit_report.py over every vector and asserts, per vector:
the exit code, the set of hard finding codes, and the set of soft finding codes.
Soft vectors are checked twice: default (soft reported, exit 0) and --strict
(soft fails, exit 1).

GREEN vectors must come out clean (no hard, no soft). RED vectors must fail
with exactly the designed finding codes — no more, no less.

Usage: python3 tests/audit_report/run_vectors.py
Exit 0 = all vectors behave as designed; exit 1 = a deviation (list printed).
Stdlib only, read-only.
"""

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
GATE = REPO / "scripts" / "check_audit_report.py"
VEC = Path(__file__).resolve().parent

STD = ["--standard-version", "v1.8.1"]

# (file, extra args, expected exit, expected hard codes, expected soft codes)
CASES = [
    ("green_all_yes.md",         STD, 0, set(), set()),
    ("green_mixed.md",           STD, 0, set(), set()),
    ("green_j3_crit_guard.md",   STD, 0, set(), set()),
    ("red_r1_missing.md",        STD, 1, {"R1"}, set()),
    ("red_r1_dup.md",            STD, 1, {"R1"}, set()),
    ("red_r1_unknown.md",        STD, 1, {"R1"}, set()),
    ("red_r1_empty_verdict.md",  STD, 1, {"R1"}, set()),
    ("red_r2_inflation.md",      STD, 1, {"R2"}, set()),
    ("red_r2_omission.md",       STD, 1, {"R2"}, set()),
    ("red_r3.md",                STD, 1, {"R3"}, set()),
    ("red_r4_wrong.md",          STD, 1, {"R4"}, set()),
    ("red_r4_zero_checked.md",   STD, 1, {"R4"}, set()),
    ("red_r4_all_three.md",      STD, 1, {"R4"}, set()),
    ("red_j3_inheritance.md",    STD, 1, {"R2", "R3", "R4"}, set()),
    ("red_s1.md",                STD, 0, set(), {"S1"}),
    ("red_s1.md",                STD + ["--strict"], 1, set(), {"S1"}),
    ("red_s2.md",                STD, 0, set(), {"S2"}),
    ("red_s2.md",                STD + ["--strict"], 1, set(), {"S2"}),
    ("red_s3.md",                STD, 0, set(), {"S3"}),
    ("red_s3.md",                STD + ["--strict"], 1, set(), {"S3"}),
    ("red_r5.md",                [],  1, {"R5"}, set()),
    # Russian-language vectors: fully Russian reports against the same
    # standard (mixed audit type). GREEN must stay clean; RED classes must
    # fire exactly as in the English vectors.
    ("ru_green_mixed.md",        STD, 0, set(), set()),
    ("ru_red_r2_inflation.md",   STD, 1, {"R2"}, set()),
    ("ru_red_r3_text_crit.md",   STD, 1, {"R3"}, set()),
    ("ru_red_r4_softened.md",    STD, 1, {"R4"}, set()),
]


def main() -> int:
    failures = 0
    for name, args, want_exit, want_hard, want_soft in CASES:
        proc = subprocess.run(
            [sys.executable, str(GATE), str(VEC / name), "--format", "json", *args],
            capture_output=True, text=True, cwd=str(REPO))
        try:
            res = json.loads(proc.stdout)
        except json.JSONDecodeError:
            print(f"FAIL {name} {args}: gate produced no JSON (rc={proc.returncode})\n{proc.stdout}\n{proc.stderr}")
            failures += 1
            continue
        got_hard = {c for c, _ in res["hard"]}
        got_soft = {c for c, _ in res["soft"]}
        problems = []
        if proc.returncode != want_exit:
            problems.append(f"exit {proc.returncode} != {want_exit}")
        if got_hard != want_hard:
            problems.append(f"hard {sorted(got_hard)} != {sorted(want_hard)}")
        if got_soft != want_soft:
            problems.append(f"soft {sorted(got_soft)} != {sorted(want_soft)}")
        if problems:
            print(f"FAIL {name} {args}: " + "; ".join(problems))
            for c, m in res["hard"]:
                print(f"        {c}: {m}")
            failures += 1
        else:
            tag = "GREEN" if want_exit == 0 and not want_soft else ("soft" if not want_hard else "RED")
            print(f"PASS {tag:5} {name} {(' ' + ' '.join(args)) if args else ''}")
    print(f"{len(CASES) - failures}/{len(CASES)} vector runs behave as designed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
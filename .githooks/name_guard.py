#!/usr/bin/env python3
"""Name-leak guard (owner rule: no personal names in public repo docs/code/commits
except the project author). Wired as git pre-commit + commit-msg via core.hooksPath.
Self-excludes: .githooks/ (this file holds the patterns), evals/datasets/ (benchmark
data), evals/results/ (run artifacts carry benchmark entity names -- NOT leaks per
the 2026-10-24 audit). Covers Cyrillic declensions AND Latin transliterations
(the 291f123 redaction missed the latter -- audit finding 1).
"""
import re
import subprocess
import sys

PAT = re.compile(
    r"Лумин|Люмик|Стасик|Клодик|Финик|Саш[аеиу]|Яш[аеиы]"
    r"|Lumin(?![A-Za-z])|Lumik|Klodik|Stasik|Yasha|Fenik|Finik|Sasha"
    r"|(^|[^A-Za-z])Prima([^A-Za-z]|$)",
    re.IGNORECASE,  # names leak lowercase too (canon README case)
)
SKIP_PREFIX = ("evals/datasets/", ".githooks/")
SKIP_SUBSTR = ("evals/results/",)


def hits_in(text):
    return sorted({text[:m.start()].count("\n") + 1 for m in PAT.finditer(text)})


def scan_all():
    """Full-repo mode (gate/CI): every tracked file, same skips. Returns hit list."""
    import subprocess
    out = subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.split()
    hits = []
    for f in out:
        if f.startswith(SKIP_PREFIX) or any(s in f for s in SKIP_SUBSTR):
            continue
        try:
            text = open(f, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        h = hits_in(text)
        if h:
            hits.append((f, h))
    return hits


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    fail = 0
    if mode == "scan-all":
        hits = scan_all()
        for f, h in hits:
            print(f"NAME LEAK in {f} (lines {h[:8]})")
        print(f"scan-all: {len(hits)} file(s) with leaks")
        return 1 if hits else 0
    if mode == "pre-commit":
        files = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True, text=True).stdout.split()
        for f in files:
            if f.startswith(SKIP_PREFIX) or any(s in f for s in SKIP_SUBSTR):
                continue
            try:
                text = open(f, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            h = hits_in(text)
            if h:
                print(f"NAME LEAK in {f} (lines {h[:8]}) -- fix or add to "
                      f"SKIP only by owner decision")
                fail = 1
    elif mode == "commit-msg":
        with open(sys.argv[2], encoding="utf-8", errors="ignore") as fh:
            text = fh.read()
        h = hits_in(text)
        if h:
            print(f"NAME LEAK in commit message (lines {h[:8]}); "
                  f"use roles (council/owner/agent) instead")
            fail = 1
    else:
        print("usage: name_guard.py pre-commit|commit-msg <msgfile>")
        fail = 2
    return fail


if __name__ == "__main__":
    sys.exit(main())

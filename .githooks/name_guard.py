#!/usr/bin/env python3
"""Name-leak guard (owner rule: no personal names in public repo docs/code/commits
except the project author). Wired as git pre-commit + commit-msg via core.hooksPath
and as the gate vector schemas/check_name_policy.py.

Repo binding (external-audit finding, 2026-10-24): the scan is bound to the
repository OF THIS SCRIPT (REPO_ROOT from __file__), never to the current
working directory -- a gate invoked from a foreign repo or a non-git folder
must scan THIS repo, not the caller's. Fail-closed: if git is unavailable,
errors, or reports no tracked files, the scan result is RED, never GREEN.

Self-excludes: .githooks/ (this file holds the patterns), evals/datasets/
(benchmark data), evals/results/ (run artifacts carry benchmark entity names
-- not leaks per the 2026-10-24 audit).
"""
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

PAT = re.compile(
    r"Лумин|Люмик|Стасик|Клодик|Финик|Саш[аеиу]|Яш[аеиы]"
    r"|Lumin(?![A-Za-z])|Lumik|Klodik|Stasik|Yasha|Fenik|Finik|Sasha"
    r"|(^|[^A-Za-z])Prima([^A-Za-z]|$)",
    re.IGNORECASE,  # names leak lowercase too (observed in the wild)
)
SKIP_PREFIX = ("evals/datasets/", ".githooks/")
SKIP_SUBSTR = ("evals/results/",)


def hits_in(text):
    return sorted({text[:m.start()].count("\n") + 1 for m in PAT.finditer(text)})


def _tracked(root):
    """git ls-files bound to `root`. Returns (files, error)."""
    try:
        proc = subprocess.run(["git", "-C", str(root), "ls-files"],
                              capture_output=True, text=True)
    except OSError as e:  # git binary missing / not executable
        return None, f"git unavailable ({e.__class__.__name__})"
    if proc.returncode != 0:
        return None, f"git ls-files failed in {root}: {proc.stderr.strip()[:120]}"
    files = proc.stdout.split()
    if not files:
        return None, f"no tracked files under {root} -- not a git repository?"
    return files, None


def scan_core(root):
    """Scan all tracked files of `root`. Returns (hits, error); exactly one
    is None. hits: list of (relpath, line_numbers)."""
    files, err = _tracked(root)
    if err:
        return None, err
    hits = []
    for f in files:
        if f.startswith(SKIP_PREFIX) or any(s in f for s in SKIP_SUBSTR):
            continue
        try:
            text = (root / f).read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        h = hits_in(text)
        if h:
            hits.append((f, h))
    return hits, None


def scan_all():
    """Full-repo mode (gate/CI): THIS script's repository, any cwd."""
    return scan_core(REPO_ROOT)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    fail = 0
    if mode == "scan-all":
        hits, err = scan_all()
        if err:
            print(f"NAME-POLICY SCAN FAILED: {err}")
            print("name policy: FAIL-CLOSED (cannot scan -> red, never green)")
            return 1
        for f, h in hits:
            print(f"NAME LEAK in {f} (lines {h[:8]})")
        print(f"scan-all: {len(hits)} file(s) with leaks")
        return 1 if hits else 0
    if mode == "pre-commit":
        try:
            proc = subprocess.run(
                ["git", "-C", str(REPO_ROOT), "diff", "--cached",
                 "--name-only", "--diff-filter=ACM"],
                capture_output=True, text=True)
        except OSError:
            print("NAME-POLICY SCAN FAILED: git unavailable")
            return 1
        if proc.returncode != 0:
            print(f"NAME-POLICY SCAN FAILED: git diff error: "
                  f"{proc.stderr.strip()[:120]}")
            return 1
        for f in proc.stdout.split():
            if f.startswith(SKIP_PREFIX) or any(s in f for s in SKIP_SUBSTR):
                continue
            try:
                text = (REPO_ROOT / f).read_text(encoding="utf-8", errors="ignore")
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
        print("usage: name_guard.py pre-commit|commit-msg <msgfile>|scan-all")
        fail = 2
    return fail


if __name__ == "__main__":
    sys.exit(main())

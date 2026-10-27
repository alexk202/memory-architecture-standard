#!/usr/bin/env python3
"""MAQS audit-report consistency gate.

Checks a filled MAQS audit report against a pinned version of STANDARD.md.
It does not judge whether a verdict is right; it checks that the report is
internally consistent and that criticality comes from the standard, not from
the auditor.

Standard resolution (first match wins):
  1. --standard PATH          read STANDARD.md from this file directly;
  2. --standard-version TAG   `git show TAG:STANDARD.md` in this repository;
  3. the report's "Standard version" field ("MAQS v1.8.1" -> tag v1.8.1).
  No flag and no field -> hard R5 (standard version not identified); the
  coverage/protocol/verdict checks are skipped (nothing to check against).

Hard checks (exit 1 on any failure):
  R1 coverage     every checklist item of STANDARD.md has exactly one verdict row;
                  no unknown item ids.
  R2 crit-list    the declared [CRIT] failure list equals the computed one
                  (verdict partial/no on an item marked [CRIT] in STANDARD.md).
                  J3 inherited criticality (v1.8.1): a failing J3 row naming a
                  [CRIT] guarded item is scored [CRIT] and must appear in the list.
  R3 protocol     the Audit Result Protocol counts equal the per-item verdicts,
                  computed by the same rule (so a J3 scored [CRIT] is counted in
                  its section's Failed-[CRIT] column and per-section codes
                  reconcile with the list, STANDARD 2.2 step 6).
  R4 verdict      exactly one of the three verdict boxes is checked ([x]); the
                  checked line must follow the verdict rules: any [CRIT] failure
                  (incl. inherited J3) -> DOES NOT PASS; only [IMP] ->
                  PASSES WITH CAVEATS; otherwise CONFORMS.
  R5 provenance   the report names the audited version (commit SHA, or an explicit
                  "no-SHA" statement with a reconstruction note) and identifies the
                  standard version (field, or an explicit --standard-version).

Soft checks (reported, exit code unaffected unless --strict):
  S1 evidence-status  a static audit should mark verdicts as static implementation
                      evidence / behavioral verification pending (glossary, v1.7+)
                      or carry the per-row evidence-status column of the template.
  S2 warnings         "Warnings: 0" in a static audit claims a clean run that
                      never happened; use "not collected".
  S3 section-claims   a section called CONFORMING/PASS must have no CRIT/IMP
                      failures.

Report format contract (examples/AUDIT_REPORT_TEMPLATE.md): per-item verdict rows
`| **<ID>** | <yes|partial|no|n/a> | <static|behavioral|pending> | <evidence> |
<guarded item (J3 only)> |`; the guarded item is read from the dedicated fifth
column only; the declared [CRIT] list lives under a "Critical Failures" /
"[CRIT] ..." heading.

Usage:
  python3 check_audit_report.py REPORT.md [--standard PATH]
      [--standard-version TAG] [--strict] [--format json]

Stdlib only, no network, read-only (the only subprocess is `git show`).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

VERDICTS = ("yes", "partial", "no", "n/a")
FAILING = {"partial", "no"}
SECTION_ORDER = ["0", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
VERDICT_LABELS = ("DOES NOT PASS", "PASSES WITH CAVEATS", "CONFORMS")

ITEM_RE = re.compile(r"^- \[[ xX]\] \*\*(?P<id>(?:\d+\.\d+[a-z]?)|(?:[A-J]\d+))\*\*(?P<rest>.*)$")
CRIT_RE = re.compile(r"\*\*\[(CRIT|IMP|REC)\]\*\*")
ROW_RE = re.compile(
    r"^\|\s*\*\*(?P<id>(?:\d+\.\d+[a-z]?)|(?:[A-J]\d+)|(?:SUPP-[A-Z]+-\d+))\*\*[^|]*\|\s*\*{0,2}(?P<v>yes|partial|no|n/a)\*{0,2}\s*\|",
    re.IGNORECASE,
)
PROTO_RE = re.compile(
    r"^\|\s*(?P<sec>0|[A-J])\.\s[^|]*\|\s*(?P<items>\d+)\s*\|\s*(?P<yes>\d+)\s*\|\s*(?P<partial>\d+)\s*\|"
    r"\s*(?P<no>\d+)\s*\|\s*(?P<na>\d+)\s*\|\s*(?P<crit>\d+)"
)
ID_TOKEN_RE = re.compile(r"\b((?:\d+\.\d+[a-z]?)|(?:[A-J]\d{1,2}))\b")
CHECKBOX_RE = re.compile(
    r"^[-*]\s*\[([ xX])\]\s*\*\*(?P<label>DOES NOT PASS|PASSES WITH CAVEATS|CONFORMS)\*\*",
    re.IGNORECASE | re.MULTILINE,
)


def section_of(item_id: str) -> str:
    return "0" if item_id[0].isdigit() else item_id[0]


def parse_standard(text: str) -> dict[str, str]:
    """item id -> criticality (CRIT/IMP/REC), first marker on the item's lines."""
    items: dict[str, str] = {}
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = ITEM_RE.match(line)
        if not m:
            continue
        crit = CRIT_RE.search(m.group("rest"))
        j = i + 1
        while crit is None and j < len(lines) and not ITEM_RE.match(lines[j]) and not lines[j].startswith("## "):
            crit = CRIT_RE.search(lines[j])
            j += 1
        items[m.group("id")] = crit.group(1) if crit else "?"
    return items


def resolve_standard(args, report_text: str):
    """Returns (standard_text|None, source_description|None, tag|None, hard_findings)."""
    hard: list[tuple[str, str]] = []
    if args.standard:
        return Path(args.standard).read_text(encoding="utf-8"), f"file {args.standard}", None, hard
    tag = args.standard_version
    if not tag:
        head = report_text[:3000]
        m = re.search(r"\*{0,2}Standard\s+version\*{0,2}\s*:\s*(.+)", head, re.IGNORECASE)
        if m:
            vm = re.search(r"v?(\d+(?:\.\d+)+)", m.group(1))
            if vm:
                tag = "v" + vm.group(1)
    if not tag:
        hard.append(("R5", "standard version not identified: no --standard-version/--standard "
                           "and no 'Standard version' field in the report header"))
        return None, None, None, hard
    proc = subprocess.run(["git", "-C", str(REPO_ROOT), "show", f"{tag}:STANDARD.md"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        hard.append(("R5", f"standard version '{tag}' not resolvable via git tags in this repository"))
        return None, f"git show {tag}:STANDARD.md", tag, hard
    return proc.stdout, f"git show {tag}:STANDARD.md", tag, hard


def block_after(text: str, heading_pattern: str) -> str:
    m = re.search(heading_pattern, text, re.IGNORECASE | re.MULTILINE)
    if not m:
        return ""
    rest = text[m.end():]
    nxt = re.search(r"^#{1,3} ", rest, re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def parse_report(text: str):
    verdicts: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for line in text.splitlines():
        m = ROW_RE.match(line.strip())
        if m:
            verdicts[m.group("id")].append((m.group("v").lower(), line.strip()))

    protocol = {}
    for line in text.splitlines():
        m = PROTO_RE.match(line.strip())
        if m:
            protocol[m.group("sec")] = {k: int(m.group(k)) for k in ("items", "yes", "partial", "no", "na", "crit")}

    # Declared [CRIT] failure list: table under a "Critical Failures" / "[CRIT] ..." heading.
    crit_block = block_after(text, r"^#{2,3}\s*(?:\[CRIT\]|Critical)[^\n]*$")
    declared_crit = set()
    for line in crit_block.splitlines():
        if line.startswith("|") and not set(line) <= set("|-: "):
            cells = [c.strip() for c in line.strip("|").split("|")]
            for c in cells[:2]:
                declared_crit.update(t for t in ID_TOKEN_RE.findall(c))

    # J3 guarded items: the dedicated fifth column of the J3 verdict row(s) only.
    guarded: set[str] = set()
    for rows in verdicts.get("J3", []):
        cells = [c.strip() for c in rows[1].split("|")]
        if len(cells) >= 6 and cells[5]:
            guarded.update(ID_TOKEN_RE.findall(cells[5]))

    # R4 reads the checked verdict line ([x]).
    checked = [m.group("label").upper() for m in CHECKBOX_RE.finditer(text) if m.group(1).lower() == "x"]

    section_claims = {}
    for m in re.finditer(r"\*\*(?P<sec>[0A-J]) verdict:\*\*\s*(?P<claim>[A-Z ]+)", text):
        section_claims[m.group("sec")] = m.group("claim").strip()
    m = re.search(r"Sections? ([0A-J](?:, [0A-J])*) (?:are|is) CONFORMING", text)
    if m:
        for s in m.group(1).split(", "):
            section_claims[s] = "CONFORMING"

    return verdicts, protocol, declared_crit, guarded, checked, section_claims


def _is_static_audit(head: str) -> bool:
    return bool(re.search(r"static (code )?(analysis|audit|review)", head, re.IGNORECASE)
                or re.search(r"audit\s+type\*{0,2}\s*:\s*\*{0,2}\s*static\b", head, re.IGNORECASE))


def _has_evidence_marking(text: str) -> bool:
    return bool(re.search(r"static implementation evidence|behavioral verification pending|\bevidence[- ]status\b",
                          text, re.IGNORECASE))


WARNINGS_ZERO_RE = re.compile(r"(?im)^\s*#*\s*\*{0,2}\s*warnings\*{0,2}\s*:\*{0,2}\s*0\b(?![-.\d])")


def check(report_text: str, standard_text: str) -> dict:
    std = parse_standard(standard_text)
    verdicts, protocol, declared_crit, guarded, checked, section_claims = parse_report(report_text)
    hard, soft = [], []
    v = {i: vs[0][0] for i, vs in verdicts.items() if i in std}

    # J3 inherited criticality (v1.8.1): a failing J3 with a [CRIT] guarded item.
    j3_failing = v.get("J3") in FAILING
    j3_inherited = j3_failing and any(std.get(g) == "CRIT" for g in guarded)

    # R1 coverage
    missing = [i for i in std if i not in verdicts]
    dup = [i for i, vs in verdicts.items() if len(vs) > 1]
    unknown = [i for i in verdicts if i not in std and not i.upper().startswith("SUPP-")]
    if missing:
        hard.append(("R1", f"items without a verdict row: {', '.join(missing)}"))
    if dup:
        hard.append(("R1", f"items with more than one verdict row: {', '.join(dup)}"))
    if unknown:
        hard.append(("R1", f"item ids not in STANDARD.md: {', '.join(unknown)}"))

    # R2 crit list
    computed_crit = {i for i, verdict in v.items() if verdict in FAILING and std[i] == "CRIT"}
    if j3_inherited:
        computed_crit.add("J3")
    over = sorted(declared_crit - computed_crit, key=_key)
    under = sorted(computed_crit - declared_crit, key=_key)
    for i in over:
        why = f"marked [{std.get(i, '?')}] in STANDARD.md" if std.get(i) != "CRIT" else f"verdict is '{v.get(i)}'"
        hard.append(("R2", f"{i} listed as [CRIT] failure but {why}"))
    if under:
        hard.append(("R2", "[CRIT] items with partial/no missing from the CRIT failure list: " + ", ".join(under)))

    # R3 protocol
    if not protocol:
        hard.append(("R3", "Audit Result Protocol table not found or not parseable"))
    for sec in SECTION_ORDER:
        ids = [i for i in std if section_of(i) == sec]
        if not ids:
            continue
        c = Counter(v.get(i) for i in ids)
        expect = {
            "items": len(ids), "yes": c["yes"], "partial": c["partial"], "no": c["no"], "na": c["n/a"],
            "crit": sum(1 for i in ids if i in computed_crit),
        }
        got = protocol.get(sec)
        if got is None:
            if protocol:
                hard.append(("R3", f"section {sec}: no protocol row"))
            continue
        diffs = [f"{k} {got[k]}->{expect[k]}" for k in expect if got[k] != expect[k]]
        if diffs:
            hard.append(("R3", f"section {sec}: declared vs computed: " + ", ".join(diffs)))

    # R4 overall verdict: exactly one checked box, and it must follow the rules.
    has_imp_fail = any(verdict in FAILING and std[i] == "IMP" for i, verdict in v.items())
    expected = "DOES NOT PASS" if computed_crit else ("PASSES WITH CAVEATS" if has_imp_fail else "CONFORMS")
    if not checked:
        hard.append(("R4", f"no checked verdict line (zero of the three verdict boxes checked); rules give '{expected}'"))
    elif len(checked) > 1:
        hard.append(("R4", f"{len(checked)} verdict lines checked ({', '.join(sorted(set(checked)))}); "
                           f"rules give '{expected}'"))
    elif checked[0] != expected:
        hard.append(("R4", f"overall verdict '{checked[0]}', rules give '{expected}'"))

    # R5 provenance: audited version (SHA or explicit no-SHA statement).
    head = report_text[:3000]
    has_sha = re.search(r"(commit|sha|revision)[^\n]{0,40}\b[0-9a-f]{7,40}\b", head, re.IGNORECASE)
    has_sha = has_sha or re.search(r"audited\s+version\*{0,2}\s*:[^\n]*\b[0-9a-f]{7,40}\b", head, re.IGNORECASE)
    declared_no_sha = re.search(r"no[-\s](commit\s+)?sha|without\s+\.git|sha\s+(not|un)", head, re.IGNORECASE)
    if not has_sha and not declared_no_sha:
        hard.append(("R5", "audited version not identified: no commit SHA and no explicit no-SHA statement in the header"))

    # S1 evidence status
    static = _is_static_audit(head)
    if static and not _has_evidence_marking(report_text):
        soft.append(("S1", "static audit without 'static implementation evidence' / 'behavioral verification pending' "
                           "marking (or the evidence-status column) on verdicts"))

    # S2 warnings
    if static and WARNINGS_ZERO_RE.search(report_text):
        soft.append(("S2", "'Warnings: 0' in a static audit; no run took place, use 'not collected'"))

    # S3 section claims
    for sec, claim in section_claims.items():
        if claim.startswith(("CONFORM", "PASS")) and "CAVEAT" not in claim:
            fails = [i for i, verdict in v.items() if section_of(i) == sec and verdict in FAILING and std[i] in ("CRIT", "IMP")]
            if fails:
                soft.append(("S3", f"section {sec} called {claim} but has CRIT/IMP failures: {', '.join(sorted(fails, key=_key))}"))

    return {
        "standard_items": len(std),
        "items_unparsed_criticality": [i for i, c in std.items() if c == "?"],
        "computed_crit_failures": sorted(computed_crit, key=_key),
        "expected_verdict": expected,
        "j3_guarded_items": sorted(guarded),
        "hard": hard,
        "soft": soft,
    }


def _key(item_id: str):
    sec = section_of(item_id)
    num = re.findall(r"\d+", item_id)
    return (SECTION_ORDER.index(sec) if sec in SECTION_ORDER else 99, [int(n) for n in num], item_id)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("report")
    ap.add_argument("--standard", default=None,
                    help="path to STANDARD.md (overrides --standard-version and the report field)")
    ap.add_argument("--standard-version", default=None, metavar="TAG",
                    help="standard tag to audit against, e.g. v1.8.1 (git show TAG:STANDARD.md); "
                         "without it the report's 'Standard version' field is used")
    ap.add_argument("--strict", action="store_true", help="soft findings also fail the gate")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args(argv)

    report_text = Path(args.report).read_text(encoding="utf-8")
    standard_text, source, tag, hard = resolve_standard(args, report_text)

    result = {
        "standard_source": source,
        "standard_version": tag,
        "hard": hard,
        "soft": [],
    }

    if standard_text is None:
        # Nothing to check the report against: provenance failed, skip coverage checks.
        # S1/S2 do not need the standard; S3 does.
        head = report_text[:3000]
        if _is_static_audit(head) and not _has_evidence_marking(report_text):
            result["soft"].append(("S1", "static audit without evidence-status marking on verdicts"))
        if _is_static_audit(head) and WARNINGS_ZERO_RE.search(report_text):
            result["soft"].append(("S2", "'Warnings: 0' in a static audit; use 'not collected'"))
        result.update({"standard_items": 0, "computed_crit_failures": [], "expected_verdict": None,
                       "j3_guarded_items": [], "skipped": "no standard resolved: R1-R4 and S3 skipped"})
    else:
        r = check(report_text, standard_text)
        result.update(r)

    red = bool(result["hard"]) or (args.strict and bool(result["soft"]))

    if args.format == "json":
        print(json.dumps({**result, "gate": "RED" if red else "GREEN"}, indent=2))
    else:
        if source:
            print(f"standard: {result['standard_version'] or ''} via {source}" if tag else f"standard: {source}")
        print(f"standard items: {result.get('standard_items', 0)}")
        if result.get("items_unparsed_criticality"):
            print("WARNING: criticality not parsed for: " + ", ".join(result["items_unparsed_criticality"]))
        if result.get("skipped"):
            print(f"  skipped: {result['skipped']}")
        print(f"computed [CRIT] failures ({len(result.get('computed_crit_failures', []))}): "
              + (", ".join(result.get("computed_crit_failures", [])) or "none"))
        if result.get("expected_verdict"):
            print(f"verdict by the rules: {result['expected_verdict']}")
        for code, msg in result["hard"]:
            print(f"  HARD {code}: {msg}")
        for code, msg in result["soft"]:
            print(f"  soft {code}: {msg}")
        print(f"GATE {'RED' if red else 'GREEN'}")
    return 1 if red else 0


if __name__ == "__main__":
    sys.exit(main())
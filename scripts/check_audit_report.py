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
                  no unknown item ids. Rows with an empty verdict cell (the
                  template's pre-filled rows) are reported under a separate
                  message ("a verdict row but an empty verdict cell"); the
                  empty template stays RED either way.
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
  R6 imp-list     the declared [IMP] failure list equals the computed one
                  (verdict partial/no on an item marked [IMP] in STANDARD.md);
                  a J3 that inherited [CRIT] is R2's business, not here. A
                  missing Important Failures table with [IMP] failures on
                  record is reported here as well.
  R7 deviation-items  every id in the Accepted Deviations table is a checklist
                  item with a partial/no verdict — there must be something
                  to accept.

Soft checks (reported, exit code unaffected unless --strict):
  S1 evidence-status  a static audit should mark verdicts as static implementation
                      evidence / behavioral verification pending (glossary, v1.7+)
                      or carry the per-row evidence-status column of the template.
  S2 warnings         "Warnings: 0" in a static audit claims a clean run that
                      never happened; use "not collected".
  S3 section-claims   a section called CONFORMING/PASS must have no CRIT/IMP
                      failures.
  S4 accepted-by   a deviation in the Accepted Deviations table is accepted by
                   the owner of the audited system, not by the auditor: the
                   "Accepted by" cell must be filled and must not name the
                   auditor; deviation rows without an "Accepted by" column
                   are reported as well.

Report format contract (examples/AUDIT_REPORT_TEMPLATE.md): per-item verdict rows
`| **<ID>** | <yes|partial|no|n/a> | <static|behavioral|pending> | <evidence> |
<guarded item (J3 only)> |`; the guarded item is read from the dedicated fifth
column only; the declared [CRIT] list lives under a "Critical Failures" /
"[CRIT] ..." heading, the declared [IMP] list under "Important Failures" /
"[IMP] ..." (RU: "## Провалы [ВАЖ]"), and accepted deviations under
"Accepted Deviations" / "## Принятые отступления" with the "Accepted by" /
"Кем принято" column.

Languages: English is canonical; Russian is an equal alias set, not a
translation layer. The standard (translations/STANDARD_RU.md: markers
[КРИТ]/[ВАЖ]/[РЕК]) and the report (verdicts да/частично/нет/н/п, labels
НЕ ПРОХОДИТ / ПРОХОДИТ С ОГОВОРКАМИ / СООТВЕТСТВУЕТ, headings
"## Вердикты по пунктам", "## Провалы [КРИТ]" / "## Провалы [ВАЖ]",
"## Принятые отступления" with the "Кем принято" deviation column, the
Russian protocol-table header, the "Версия стандарта" field, Russian
provenance wording) are parsed by the same rules; everything is normalized
to the English canonical forms before any check runs. The gate output
reports which language was recognized for the standard and for the report
("languages: report=ru, standard=ru").

Messages name the actual standard file (--standard path, or "STANDARD.md" for
a git-tag resolution) and the criticality marker in the standard's language:
"marked [ВАЖ] in translations/STANDARD_RU.md" when checked against the
Russian standard, "marked [IMP] in STANDARD.md" otherwise.

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

# Russian aliases (translations/STANDARD_RU.md) are equal, not secondary:
# criticality markers [КРИТ]/[ВАЖ]/[РЕК], verdicts да/частично/нет/н/п, the
# overall-verdict labels НЕ ПРОХОДИТ / ПРОХОДИТ С ОГОВОРКАМИ / СООТВЕТСТВУЕТ,
# the "## Вердикты по пунктам" and "## Провалы [КРИТ]" headings, the Russian
# protocol-table header and the "Версия стандарта" field. Everything is
# normalized to the English canonical form before any check runs.
CRIT_ALIAS = {"CRIT": "CRIT", "КРИТ": "CRIT", "IMP": "IMP", "ВАЖ": "IMP", "REC": "REC", "РЕК": "REC"}
VERDICT_ALIAS = {"да": "yes", "частично": "partial", "нет": "no", "н/п": "n/a"}
VERDICT_LABEL_ALIAS = {
    "НЕ ПРОХОДИТ": "DOES NOT PASS",
    "ПРОХОДИТ С ОГОВОРКАМИ": "PASSES WITH CAVEATS",
    "СООТВЕТСТВУЕТ": "CONFORMS",
}

ITEM_RE = re.compile(r"^- \[[ xX]\] \*\*(?P<id>(?:\d+\.\d+[a-z]?)|(?:[A-J]\d+))\*\*(?P<rest>.*)$")
CRIT_RE = re.compile(r"\*\*\[(CRIT|КРИТ|IMP|ВАЖ|REC|РЕК)\]\*\*")
ROW_RE = re.compile(
    r"^\|\s*\*\*(?P<id>(?:\d+\.\d+[a-z]?)|(?:[A-J]\d+)|(?:SUPP-[A-Z]+-\d+))\*\*[^|]*\|"
    r"\s*\*{0,2}(?P<v>yes|partial|no|n/a|да|частично|нет|н/п)\*{0,2}\s*\|",
    re.IGNORECASE,
)
PROTO_RE = re.compile(
    r"^\|\s*(?P<sec>0|[A-J])\.\s[^|]*\|\s*(?P<items>\d+)\s*\|\s*(?P<yes>\d+)\s*\|\s*(?P<partial>\d+)\s*\|"
    r"\s*(?P<no>\d+)\s*\|\s*(?P<na>\d+)\s*\|\s*(?P<crit>\d+)"
)
ID_TOKEN_RE = re.compile(r"\b((?:\d+\.\d+[a-z]?)|(?:[A-J]\d{1,2}))\b")
ROW_PRESENCE_RE = re.compile(r"^\|\s*\*\*(?P<id>(?:\d+\.\d+[a-z]?)|(?:[A-J]\d+)|(?:SUPP-[A-Z]+-\d+))\*\*")
CHECKBOX_RE = re.compile(
    r"^[-*]\s*\[([ xX])\]\s*\*\*(?P<label>DOES NOT PASS|PASSES WITH CAVEATS|CONFORMS"
    r"|НЕ ПРОХОДИТ|ПРОХОДИТ С ОГОВОРКАМИ|СООТВЕТСТВУЕТ)\*\*",
    re.IGNORECASE | re.MULTILINE,
)

# Headings of the template blocks, English and Russian forms both recognized.
IV_HEADING_RE = r"^#{1,3}\s*(?:Item\s+Verdicts|Вердикты\s+по\s+пунктам)\b"
CRIT_HEADING_RE = r"^#{2,3}\s*(?:\[CRIT\]|Critical|Провалы\s*\[(?:КРИТ)\])[^\n]*$"
IMP_HEADING_RE = r"^#{2,3}\s*(?:\[IMP\]|Important|Провалы\s*\[(?:ВАЖ)\])[^\n]*$"
DEV_HEADING_RE = r"^#{2,3}\s*(?:Accepted\s+Deviations|Принятые\s+отступления)[^\n]*$"
ACCEPTED_BY_RE = re.compile(r"accepted\s+by\b|кем\s+принято\b", re.IGNORECASE)
AUDITOR_RE = re.compile(r"\*{0,2}Auditor\*{0,2}:\*{0,2}\s*([^\n|]+)", re.IGNORECASE)

# Language detection (informational, reported in the gate output; both
# languages parse identically — this only says which one was recognized).
RU_STANDARD_RE = re.compile(r"\*\*\[(?:КРИТ|ВАЖ|РЕК)\]\*\*")
RU_REPORT_RE = re.compile(
    r"Вердикты\s+по\s+пунктам"
    r"|Провалы\s*\[КРИТ\]"
    r"|Провалы\s*\[ВАЖ\]"
    r"|Принятые\s+отступления"
    r"|^\|\s*Раздел\s*\|"
    r"|\[\s*[xX]\s*\]\s*\*\*(?:НЕ\s+ПРОХОДИТ|ПРОХОДИТ\s+С\s+ОГОВОРКАМИ|СООТВЕТСТВУЕТ)\*\*"
    r"|^\|\s*\*{0,2}[\w.a-z]+\*{0,2}\s*\|\s*\*{0,2}(?:да|частично|н/п)\*{0,2}\s*\|",
    re.IGNORECASE | re.MULTILINE,
)


def detect_standard_language(text: str) -> str:
    return "ru" if RU_STANDARD_RE.search(text) else "en"


def detect_report_language(text: str) -> str:
    return "ru" if RU_REPORT_RE.search(text) else "en"


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
        items[m.group("id")] = CRIT_ALIAS[crit.group(1)] if crit else "?"
    return items


def resolve_standard(args, report_text: str):
    """Returns (standard_text|None, source_description|None, tag|None, hard_findings)."""
    hard: list[tuple[str, str]] = []
    if args.standard:
        return Path(args.standard).read_text(encoding="utf-8"), f"file {args.standard}", None, hard
    tag = args.standard_version
    if not tag:
        head = report_text[:3000]
        m = re.search(r"\*{0,2}(?:Standard\s+version|Версия\s+стандарта)\*{0,2}\s*:\s*(.+)", head, re.IGNORECASE)
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


def table_rows(block: str) -> list[list[str]]:
    """Cell lists of the table rows in a heading block; separator rows skipped."""
    rows: list[list[str]] = []
    for line in block.splitlines():
        s = line.strip()
        if not s.startswith("|") or set(s) <= set("|-: "):
            continue
        rows.append([c.strip() for c in s.strip("|").split("|")])
    return rows


MARKER_PIECE_RE = re.compile(r"[\[(]\*{0,2}(?:CRIT|КРИТ|IMP|ВАЖ|REC|РЕК)\*{0,2}[\])]")


def _id_cell_tokens(cell: str) -> list[str] | None:
    """Item ids when the cell consists of item-id token(s) with optional
    criticality markers ('**A4**', 'D6 [REC]', 'A4, A5'), else None —
    free text never yields ids."""
    cleaned = cell.replace("*", "").replace(",", " ").strip()
    parts = cleaned.split()
    if not parts:
        return None
    for p in parts:
        if not (ID_TOKEN_RE.fullmatch(p) or MARKER_PIECE_RE.fullmatch(p)):
            return None
    ids = [p for p in parts if ID_TOKEN_RE.fullmatch(p)]
    return ids or None


def declared_ids(rows: list[list[str]], ncells: int = 2) -> set[str]:
    """Item ids from the first id-bearing cell of every table row (R2/R6
    style). A cell is id-bearing when it consists of item-id token(s) with
    optional criticality markers ('**A4**', 'D6 [REC]', 'A4, A5') — free
    text (Evidence in the second cell, descriptions) never yields ids, and
    a '#' numbering column in the first cell is skipped in favor of the
    next cell. Cells after the first id-bearing one are not read."""
    out: set[str] = set()
    for cells in rows:
        for c in cells[:ncells]:
            toks = _id_cell_tokens(c)
            if toks:
                out.update(toks)
                break
    return out


def parse_report(text: str):
    verdicts: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for line in text.splitlines():
        m = ROW_RE.match(line.strip())
        if m:
            val = VERDICT_ALIAS.get(m.group("v").lower(), m.group("v").lower())
            verdicts[m.group("id")].append((val, line.strip()))

    protocol = {}
    for line in text.splitlines():
        m = PROTO_RE.match(line.strip())
        if m:
            protocol[m.group("sec")] = {k: int(m.group(k)) for k in ("items", "yes", "partial", "no", "na", "crit")}

    # Declared [CRIT] failure list: table under a "Critical Failures" /
    # "[CRIT] ..." heading (Russian: "## Провалы [КРИТ]"); ids from the
    # first two cells of every table row.
    declared_crit = declared_ids(table_rows(block_after(text, CRIT_HEADING_RE)), 2)

    # J3 guarded items: the dedicated fifth column of the J3 verdict row(s) only.
    guarded: set[str] = set()
    for rows in verdicts.get("J3", []):
        cells = [c.strip() for c in rows[1].split("|")]
        if len(cells) >= 6 and cells[5]:
            guarded.update(ID_TOKEN_RE.findall(cells[5]))

    # R4 reads the checked verdict line ([x]); Russian labels are normalized
    # to the English canonical forms before comparison.
    checked = [VERDICT_LABEL_ALIAS.get(m.group("label").upper(), m.group("label").upper())
               for m in CHECKBOX_RE.finditer(text) if m.group(1).lower() == "x"]

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

# How criticality markers are shown in gate messages: in the language of the
# standard being checked against. English standard -> [CRIT]/[IMP]/[REC];
# Russian standard -> [КРИТ]/[ВАЖ]/[РЕК].
MARKERS_EN = {"CRIT": "CRIT", "IMP": "IMP", "REC": "REC", "?": "?"}
MARKERS_RU = {"CRIT": "КРИТ", "IMP": "ВАЖ", "REC": "РЕК", "?": "?"}


def check(report_text: str, standard_text: str, standard_ref: str = "STANDARD.md") -> dict:
    std = parse_standard(standard_text)
    # standard_ref: how the standard file is named in gate messages — the
    # --standard path when given, "STANDARD.md" for a git-tag resolution.
    markers = MARKERS_RU if detect_standard_language(standard_text) == "ru" else MARKERS_EN
    verdicts, protocol, declared_crit, guarded, checked, section_claims = parse_report(report_text)
    hard, soft = [], []
    v = {i: vs[0][0] for i, vs in verdicts.items() if i in std}

    # J3 inherited criticality (v1.8.1): a failing J3 with a [CRIT] guarded item.
    j3_failing = v.get("J3") in FAILING
    j3_inherited = j3_failing and any(std.get(g) == "CRIT" for g in guarded)

    # R1 coverage. Verdict rows are scanned globally (old-format reports carry
    # per-item rows in their own section tables); rows that merely name an item
    # with an empty verdict cell are recognized only inside the template's
    # "Item Verdicts" block, so Critical/Important table rows never mask a
    # missing verdict row. The two R1 messages are separate: "without a verdict
    # row" vs "a verdict row but an empty verdict cell" (the empty template
    # stays RED either way).
    iv_block = block_after(report_text, IV_HEADING_RE)
    present: set[str] = set()
    empty_verdict: set[str] = set()
    for line in iv_block.splitlines():
        m = ROW_PRESENCE_RE.match(line.strip())
        if m:
            present.add(m.group("id"))
            if not ROW_RE.match(line.strip()):
                empty_verdict.add(m.group("id"))
    missing = [i for i in std if i not in verdicts and i not in present]
    empty_verdict_list = sorted((i for i in empty_verdict if i in std), key=_key)
    dup = [i for i, vs in verdicts.items() if len(vs) > 1]
    unknown = [i for i in present | set(verdicts) if i not in std and not i.upper().startswith("SUPP-")]
    if missing:
        hard.append(("R1", f"items without a verdict row: {', '.join(missing)}"))
    if empty_verdict_list:
        hard.append(("R1", f"items with a verdict row but an empty verdict cell: {', '.join(empty_verdict_list)}"))
    if dup:
        hard.append(("R1", f"items with more than one verdict row: {', '.join(dup)}"))
    if unknown:
        hard.append(("R1", f"item ids not in {standard_ref}: {', '.join(unknown)}"))

    # R2 crit list
    computed_crit = {i for i, verdict in v.items() if verdict in FAILING and std[i] == "CRIT"}
    if j3_inherited:
        computed_crit.add("J3")
    over = sorted(declared_crit - computed_crit, key=_key)
    under = sorted(computed_crit - declared_crit, key=_key)
    for i in over:
        if std.get(i) != "CRIT":
            why = f"marked [{markers.get(std.get(i, '?'), std.get(i, '?'))}] in {standard_ref}"
        elif v.get(i) is None:
            why = "has no verdict row (see R1)"
        else:
            why = f"verdict is '{v.get(i)}'"
        hard.append(("R2", f"{i} listed as [CRIT] failure but {why}"))
    if under:
        hard.append(("R2", f"{markers['CRIT']} items with partial/no missing from the {markers['CRIT']} "
                           f"failure list: " + ", ".join(under)))

    # R6 imp list: the same reconciliation as R2 for [IMP] items. A J3 that
    # inherited [CRIT] is already in the R2 list, so it is excluded here.
    computed_imp = {i for i, verdict in v.items() if verdict in FAILING and std[i] == "IMP"}
    if j3_inherited:
        computed_imp.discard("J3")
    if re.search(IMP_HEADING_RE, report_text, re.IGNORECASE | re.MULTILINE):
        declared_imp = declared_ids(table_rows(block_after(report_text, IMP_HEADING_RE)), 2)
        over_imp = sorted(declared_imp - computed_imp, key=_key)
        under_imp = sorted(computed_imp - declared_imp, key=_key)
        for i in over_imp:
            if std.get(i) != "IMP":
                why = f"marked [{markers.get(std.get(i, '?'), std.get(i, '?'))}] in {standard_ref}"
            elif v.get(i) is None:
                why = "has no verdict row (see R1)"
            else:
                why = f"verdict is '{v.get(i)}'"
            hard.append(("R6", f"{i} listed as [IMP] failure but {why}"))
        if under_imp:
            hard.append(("R6", f"[{markers['IMP']}] items with partial/no missing from the "
                               f"[{markers['IMP']}] failure list: " + ", ".join(under_imp)))
    elif computed_imp:
        hard.append(("R6", "Important Failures table not found"))

    # Accepted Deviations table: read once for R7 (hard) and S4 (soft).
    dev_rows = table_rows(block_after(report_text, DEV_HEADING_RE))
    accepted_by_col = None
    if dev_rows and not ID_TOKEN_RE.search(dev_rows[0][0]):
        for idx, cell in enumerate(dev_rows[0]):
            if ACCEPTED_BY_RE.match(cell):
                accepted_by_col = idx
                break

    # R7 deviation items: every listed deviation must be a checklist item
    # with a partial/no verdict — there must be something to accept.
    for cells in dev_rows:
        for i in ID_TOKEN_RE.findall(cells[0]):
            if i not in std:
                hard.append(("R7", f"{i} in Accepted Deviations is not an item of {standard_ref}"))
                continue
            verdict = v.get(i)
            if verdict not in FAILING:
                shown = verdict if verdict is not None else "unknown"
                hard.append(("R7", f"{i} in Accepted Deviations has verdict '{shown}' — nothing to accept"))

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

    # R5 provenance: audited version (SHA or explicit no-SHA statement);
    # English and Russian header forms both recognized ("Audited version:"
    # / "Аудируемая версия:", commit SHA or "коммит <SHA>", "no-SHA" /
    # "без sha / без коммита / без .git").
    head = report_text[:3000]
    has_sha = re.search(r"(commit|sha|revision|коммит)[^\n]{0,40}\b[0-9a-f]{7,40}\b", head, re.IGNORECASE)
    has_sha = has_sha or re.search(r"(?:audited|аудируем\w*)\s+(?:version|верси\w*)\*{0,2}\s*:[^\n]*\b[0-9a-f]{7,40}\b",
                                   head, re.IGNORECASE)
    declared_no_sha = re.search(r"no[-\s](commit\s+)?sha|without\s+\.git|sha\s+(not|un)|без\s+(?:sha|коммита?|\.git)",
                                head, re.IGNORECASE)
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

    # S4 accepted-by (soft): a deviation is accepted by the owner of the
    # audited system, not by the auditor.
    dev_id_rows = [cells for cells in dev_rows if ID_TOKEN_RE.findall(cells[0])]
    if dev_id_rows and accepted_by_col is None:
        soft.append(("S4", "Accepted Deviations without an 'Accepted by' column"))
    elif accepted_by_col is not None:
        m_aud = AUDITOR_RE.search(head)
        auditor = m_aud.group(1).strip().casefold() if m_aud else None
        for cells in dev_id_rows:
            val = cells[accepted_by_col].strip() if accepted_by_col < len(cells) else ""
            for i in ID_TOKEN_RE.findall(cells[0]):
                if not val:
                    soft.append(("S4", f"{i} deviation has no 'Accepted by'"))
                elif auditor and val.casefold() == auditor:
                    soft.append(("S4", f"{i} deviation accepted by the auditor; acceptance "
                                       f"belongs to the owner of the audited system"))

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
        "standard_language": detect_standard_language(standard_text) if standard_text is not None else None,
        "report_language": detect_report_language(report_text),
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
        r = check(report_text, standard_text,
                  standard_ref=args.standard if args.standard else "STANDARD.md")
        result.update(r)

    red = bool(result["hard"]) or (args.strict and bool(result["soft"]))

    if args.format == "json":
        print(json.dumps({**result, "gate": "RED" if red else "GREEN"}, indent=2))
    else:
        if source:
            print(f"standard: {result['standard_version'] or ''} via {source}" if tag else f"standard: {source}")
        langs = f"languages: report={result['report_language']}"
        if result["standard_language"]:
            langs += f", standard={result['standard_language']}"
        print(langs)
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
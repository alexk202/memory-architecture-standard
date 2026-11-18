#!/usr/bin/env python3
"""Version and item-count consistency across the repository (hard gate).

Single source: the newest release heading in CHANGELOG.md -- "## [X.Y] -
YYYY-MM-DD". Every other place that states the standard's version, its
release date or its item count must agree with it, and the two checklist
files must carry the same number of items.

Why this exists: the version line in the standard's own header
("**Version:** X.Y (DATE)") went stale across two releases. The item
counts were covered by R8 and by per-release greps; the header version was
covered by nothing, and a grep for "v1.9" does not match "1.9".

Usage: python3 scripts/check_version_sync.py   (exit 1 on any mismatch)
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def find(rel, pattern, label, group=1):
    m = re.search(pattern, read(rel))
    if not m:
        return None, f"{label}: pattern not found in {rel}"
    return m.group(group), None


def main() -> int:
    problems = []

    # --- single source -----------------------------------------------
    m = re.search(r"^## \[(\d+\.\d+(?:\.\d+)?)\] - (\d{4}-\d{2}-\d{2})",
                  read("CHANGELOG.md"), re.M)
    if not m:
        print("VERSION SYNC FAILED: no release heading in CHANGELOG.md")
        return 1
    version, date = m.group(1), m.group(2)

    # --- item counts --------------------------------------------------
    en_items = read("STANDARD.md").count("- [ ] **")
    ru_items = read("translations/STANDARD_RU.md").count("- [ ] **")
    if en_items != ru_items:
        problems.append(f"item count: STANDARD.md {en_items} != RU mirror {ru_items}")
    items = str(en_items)

    # --- every stated version, date and count -------------------------
    checks = [
        ("STANDARD.md", r"\*\*Version:\*\* (\d+\.\d+(?:\.\d+)?) \((\d{4}-\d{2}-\d{2})\)",
         "standard header", (version, date)),
        ("translations/STANDARD_RU.md", r"\*\*Версия:\*\* (\d+\.\d+(?:\.\d+)?) \((\d{4}-\d{2}-\d{2})\)",
         "RU header", (version, date)),
        ("README.md", r"badge/version-(\d+\.\d+(?:\.\d+)?)-", "README badge", (version,)),
        ("README.md", r"badge/checklist-(\d+)_items", "README item badge", (items,)),
        ("README.md", r"A (\d+)-item", "README intro", (items,)),
        ("README.md", r"\| \| \*\*Total\*\* \| \*\*(\d+)\*\* \|", "README total", (items,)),
        ("docs/QUICK_CHECK.md", r"\*\*Standard:\*\* MAQS v(\d+\.\d+(?:\.\d+)?) · \d+ of (\d+) items",
         "QUICK_CHECK header", (version, items)),
        ("docs/QUICK_CHECK.md", r"\((\d+) items;", "QUICK_CHECK next steps", (items,)),
        ("examples/AUDIT_REPORT_TEMPLATE.md", r"\*\*Standard version:\*\* MAQS v(\d+\.\d+(?:\.\d+)?)",
         "template version field", (version,)),
        ("examples/AUDIT_REPORT_TEMPLATE.md", r"Generated using MAQS v(\d+\.\d+(?:\.\d+)?) Audit Report Template",
         "template footer", (version,)),
    ]
    for rel, pattern, label, expected in checks:
        m = re.search(pattern, read(rel))
        if not m:
            problems.append(f"{label}: pattern not found in {rel}")
            continue
        got = m.groups()
        if got != expected:
            problems.append(f"{label} ({rel}): {got} != expected {expected}")

    # --- template verdict rows ----------------------------------------
    rows = len(re.findall(r"^\| \*\*[0-9A-Z]", read("examples/AUDIT_REPORT_TEMPLATE.md"), re.M))
    if rows != en_items:
        problems.append(f"template verdict rows: {rows} != {en_items} items")

    print(f"single source: CHANGELOG {version} ({date}); items {items}")
    if problems:
        print("VERSION SYNC RED:")
        for p in problems:
            print("  -", p)
        return 1
    print("VERSION SYNC GREEN — version, date and item counts agree everywhere")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Pre-commit / pre-push privacy check for berkeley-callink-engage-finance.
Flags accidental real emails, chartstrings, CalLink request IDs, or non-sample spreadsheets/PDFs.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ALLOWED_XLSX = {Path("skills/budget-reconcile/examples/sample_budget.xlsx")}
BLOCKED_EXTENSIONS = {".xlsx", ".xls", ".pdf", ".docx", ".m4a", ".csv"}

PATTERNS = [
    ("University/personal email", re.compile(r"[a-zA-Z0-9._%+-]+@(?!example\.com\b)[a-zA-Z0-9.-]+\.(?:edu|com|org|net)\b")),
    ("Real UC chartstring", re.compile(r"\b4-\d{2}-\d{6}\b")),
    ("Real CalLink request ID (18xxxxx/19xxxxx)", re.compile(r"(?:CalLinks?\s*#?|requests/purchase/|finance/print/|req=)\s*1[89]\d{5}\b", re.IGNORECASE)),
]


def scan() -> int:
    issues: list[str] = []

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if ".git" in rel.parts or "__pycache__" in rel.parts:
            continue

        if path.suffix.lower() in BLOCKED_EXTENSIONS and rel not in ALLOWED_XLSX:
            issues.append(f"Blocked file type in public repo: {rel}")
            continue

        if path.suffix.lower() in {".xlsx", ".xls", ".png", ".jpg", ".jpeg", ".pdf"}:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for line_no, line in enumerate(text.splitlines(), 1):
            for label, pat in PATTERNS:
                m = pat.search(line)
                if m:
                    # Allow explicit documentation examples like <org_slug>, 4-XX-XXXXXX, or github.com/ChromeDevTools
                    snippet = m.group(0)
                    if "github.com" in line or "callink.berkeley.edu" in snippet or "berkeley.edu" == snippet:
                        continue
                    issues.append(f"{rel}:{line_no} [{label}] -> {snippet}")

    if issues:
        print("PRIVACY CHECK FAILED:")
        for item in issues:
            print(f"  [!] {item}")
        return 1

    print("[OK] Privacy check passed: no real club data, emails, chartstrings, or blocked files found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(scan())

#!/usr/bin/env python3
"""
Normalize CalLink Finance exports (CSV, TSV, or copy-pasted text tables)
into structured JSON or a Markdown summary table.
"""

import argparse
import csv
import io
import json
import re
import sys
from pathlib import Path
from typing import Any


AMOUNT_RE = re.compile(r"^\s*([+-]?)\s*\$?\s*([0-9][0-9,]*\.?\d*|\.\d+)\s*$")
PAREN_AMOUNT_RE = re.compile(r"^\s*\(\s*\$?\s*([0-9][0-9,]*\.?\d*|\.\d+)\s*\)\s*$")
CALLINKS_ID_RE = re.compile(r"(?:CalLinks?\s*#?|#)(\d{5,9})", re.IGNORECASE)


def parse_amount(raw: str | None) -> float | None:
    """Parse currency string such as '$1,234.56', '($500.00)', or '-45.00'."""
    if raw is None:
        return None
    text = str(raw).strip()
    if not text or text in {"-", "--", "N/A"}:
        return None

    m_paren = PAREN_AMOUNT_RE.match(text)
    if m_paren:
        return -float(m_paren.group(1).replace(",", ""))

    m_amt = AMOUNT_RE.match(text)
    if m_amt:
        sign = -1.0 if m_amt.group(1) == "-" else 1.0
        return sign * float(m_amt.group(2).replace(",", ""))

    return None


def normalize_header(header: str) -> str:
    """Map varying CalLink / pasted column headers to canonical keys."""
    h = re.sub(r"[^a-z0-9]+", " ", header.strip().lower()).strip()
    mapping = {
        "date": "date",
        "transaction date": "date",
        "posted date": "date",
        "submitted": "date",
        "request": "ref",
        "request #": "ref",
        "id": "ref",
        "ref": "ref",
        "transaction id": "ref",
        "callinks": "ref",
        "payee": "vendor",
        "vendor": "vendor",
        "vendor payee": "vendor",
        "title": "description",
        "subject": "description",
        "description": "description",
        "memo": "description",
        "status": "status",
        "stage": "status",
        "type": "type",
        "category": "category",
        "amount": "amount",
        "net amount": "amount",
        "total": "amount",
        "credit": "money_in",
        "money in": "money_in",
        "deposit": "money_in",
        "debit": "money_out",
        "money out": "money_out",
        "expense": "money_out",
    }
    return mapping.get(h, h.replace(" ", "_"))


def detect_delimiter(sample: str) -> str | None:
    """Return csv delimiter if input looks delimited, else None."""
    lines = [ln for ln in sample.splitlines() if ln.strip()]
    if not lines:
        return None
    first = lines[0]
    if "\t" in first:
        return "\t"
    if "," in first:
        return ","
    return None


def parse_delimited(text: str, delimiter: str) -> list[dict[str, Any]]:
    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    if not reader.fieldnames:
        return []

    canon_fields = [normalize_header(f) for f in reader.fieldnames]
    rows: list[dict[str, Any]] = []

    for raw_row in reader:
        if not any(v and str(v).strip() for v in raw_row.values()):
            continue
        item: dict[str, Any] = {}
        for orig_k, canon_k in zip(reader.fieldnames, canon_fields):
            val = (raw_row.get(orig_k) or "").strip()
            if canon_k in {"amount", "money_in", "money_out"}:
                parsed = parse_amount(val)
                item[canon_k] = parsed if parsed is not None else val
            else:
                item[canon_k] = val

        # Derive money_in / money_out if only a signed amount column is present
        if "amount" in item and isinstance(item["amount"], (int, float)):
            amt = float(item["amount"])
            item.setdefault("money_in", round(amt, 2) if amt > 0 else 0.0)
            item.setdefault("money_out", round(abs(amt), 2) if amt < 0 else 0.0)
        elif "money_in" in item or "money_out" in item:
            m_in = float(item.get("money_in") or 0.0) if isinstance(item.get("money_in"), (int, float)) else 0.0
            m_out = float(item.get("money_out") or 0.0) if isinstance(item.get("money_out"), (int, float)) else 0.0
            item["money_in"] = round(m_in, 2)
            item["money_out"] = round(m_out, 2)
            item["amount"] = round(m_in - m_out, 2)

        # Extract CalLinks # if embedded in description or title
        if not item.get("ref"):
            combined = f"{item.get('description', '')} {item.get('vendor', '')}"
            m = CALLINKS_ID_RE.search(combined)
            if m:
                item["ref"] = f"CalLinks #{m.group(1)}"

        rows.append(item)

    return rows


def parse_freeform_lines(text: str) -> list[dict[str, Any]]:
    """Best-effort parser for pipe-separated or whitespace-separated pasted lines."""
    rows: list[dict[str, Any]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or set(line) <= {"-", "=", "|", " ", ":"}:
            continue
        if "|" in line:
            parts = [p.strip() for p in line.strip("|").split("|")]
        else:
            parts = re.split(r"\s{2,}", line)
        if len(parts) < 2:
            continue
        amounts = [parse_amount(p) for p in parts]
        numeric = [a for a in amounts if a is not None]
        m = CALLINKS_ID_RE.search(line)
        rows.append({
            "raw_columns": parts,
            "ref": f"CalLinks #{m.group(1)}" if m else "",
            "amount": numeric[-1] if numeric else None,
        })
    return rows


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total_in = sum(
        float(r["money_in"])
        for r in rows
        if isinstance(r.get("money_in"), (int, float))
    )
    total_out = sum(
        float(r["money_out"])
        for r in rows
        if isinstance(r.get("money_out"), (int, float))
    )
    return {
        "row_count": len(rows),
        "total_money_in": round(total_in, 2),
        "total_money_out": round(total_out, 2),
        "net_change": round(total_in - total_out, 2),
        "rows": rows,
    }


def to_markdown(summary: dict[str, Any]) -> str:
    rows = summary["rows"]
    lines = [
        f"**Parsed Rows:** {summary['row_count']} | "
        f"**Money In:** ${summary['total_money_in']:,.2f} | "
        f"**Money Out:** ${summary['total_money_out']:,.2f} | "
        f"**Net:** ${summary['net_change']:,.2f}",
        "",
        "| Date | Ref # | Vendor / Description | Status | In ($) | Out ($) |",
        "| :--- | :--- | :--- | :--- | ---: | ---: |",
    ]
    for r in rows:
        if "raw_columns" in r:
            desc = " / ".join(r["raw_columns"])
            amt = r.get("amount")
            amt_str = f"{amt:,.2f}" if isinstance(amt, (int, float)) else "-"
            lines.append(f"| - | {r.get('ref', '-')} | {desc} | - | - | {amt_str} |")
            continue
        dt = r.get("date", "-") or "-"
        ref = r.get("ref", "-") or "-"
        vendor = r.get("vendor", "")
        desc = r.get("description", "")
        label = " - ".join(p for p in (vendor, desc) if p) or "-"
        status = r.get("status", r.get("type", "-")) or "-"
        m_in = r.get("money_in", 0.0)
        m_out = r.get("money_out", 0.0)
        in_str = f"{m_in:,.2f}" if isinstance(m_in, (int, float)) else "-"
        out_str = f"{m_out:,.2f}" if isinstance(m_out, (int, float)) else "-"
        lines.append(f"| {dt} | {ref} | {label} | {status} | {in_str} | {out_str} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize CalLink Finance exports.")
    parser.add_argument("input_file", nargs="?", help="Path to CSV/TSV/text export (or omit to read stdin)")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    if args.input_file:
        text = Path(args.input_file).read_text(encoding="utf-8-sig")
    else:
        text = sys.stdin.read()

    delimiter = detect_delimiter(text)
    rows = parse_delimited(text, delimiter) if delimiter else parse_freeform_lines(text)
    summary = summarize(rows)

    if args.format == "json":
        print(json.dumps(summary, indent=2))
    else:
        print(to_markdown(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

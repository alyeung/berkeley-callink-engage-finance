#!/usr/bin/env python3
"""
Generic Budget & Ledger Audit Harness
Validates Ledger categories and Status values against Spending Dashboard formulas,
verifies the Bank Reconciliation tie-out, detects duplicate IDs/refs, and prints
a Budget vs. Actuals report.
"""

import argparse
import sys
from pathlib import Path
import openpyxl


DEFAULT_WORKBOOK = Path(__file__).resolve().parent.parent / "examples" / "sample_budget.xlsx"
VALID_STATUSES = {"Cleared", "Encumbered", "Unapproved", "Placeholder"}


def audit_workbook(path: Path) -> int:
    wb = openpyxl.load_workbook(path, data_only=False)
    ws_led = wb["Ledger"]
    ws_bva = wb["Spending Dashboard"]
    ws_bs = wb["Budget Summary"]
    ws_gala = wb["Gala Assumptions"]

    valid_categories = set()
    budget_rows = []
    gala_tickets = float(ws_gala["C3"].value or 0) * float(ws_gala["D3"].value or 0)

    r = 4
    while r <= ws_bs.max_row:
        name = ws_bs.cell(r, 1).value
        if not name or str(name).startswith("Operating Subtotal") or str(name).startswith("TOTAL"):
            r += 1
            continue
        is_sub = str(name).lstrip().startswith("↳")
        cat_key = str(name).replace("↳", "").replace("(Sub-item)", "").strip() if is_sub else str(name).strip()
        valid_categories.add(cat_key)

        rev_raw = ws_bs.cell(r, 3).value
        rev = gala_tickets if isinstance(rev_raw, str) and "Gala Assumptions" in rev_raw else float(rev_raw or 0.0)
        spo = float(ws_bs.cell(r, 4).value or 0.0)
        ga = float(ws_bs.cell(r, 5).value or 0.0)
        gross = float(ws_bs.cell(r, 8).value or 0.0)
        approved_budget = -(rev + spo + ga + gross)

        budget_rows.append({
            "bs_row": r,
            "name": str(name),
            "cat_key": cat_key,
            "approved_budget": approved_budget,
            "is_subitem": is_sub,
            "is_passthrough": "Pass-Through" in str(name),
        })
        r += 1

    errors = []
    warnings = []
    txns = []
    seen_ids = set()
    seen_refs = {}

    row_idx = 5
    while row_idx <= ws_led.max_row:
        rec_id = ws_led.cell(row_idx, 1).value
        if not rec_id or str(rec_id).startswith("TOTAL"):
            break
        dt = str(ws_led.cell(row_idx, 2).value or "")
        cat = str(ws_led.cell(row_idx, 3).value or "").strip()
        desc = str(ws_led.cell(row_idx, 5).value or "")
        vendor = str(ws_led.cell(row_idx, 6).value or "")
        m_in = float(ws_led.cell(row_idx, 9).value or 0.0)
        m_out = float(ws_led.cell(row_idx, 10).value or 0.0)
        status = str(ws_led.cell(row_idx, 12).value or "").strip()
        pmt_ref = str(ws_led.cell(row_idx, 13).value or "").strip()

        if rec_id in seen_ids:
            errors.append(f"Row {row_idx}: Duplicate Receipt # '{rec_id}'")
        seen_ids.add(rec_id)

        if status not in VALID_STATUSES:
            errors.append(f"Row {row_idx} ({rec_id}): Invalid Status '{status}' (expected one of {sorted(VALID_STATUSES)})")

        if pmt_ref.startswith("CalLinks #"):
            if pmt_ref in seen_refs:
                warnings.append(f"Row {row_idx} ({rec_id}): Duplicate ref '{pmt_ref}' (also on {seen_refs[pmt_ref]})")
            seen_refs[pmt_ref] = rec_id

        if cat not in valid_categories:
            errors.append(f"Row {row_idx} ({rec_id}): Unknown Budget Category '{cat}'")

        txns.append({
            "rec_id": rec_id,
            "date": dt,
            "category": cat,
            "description": desc,
            "vendor": vendor,
            "in": m_in,
            "out": m_out,
            "net_spend": m_out - m_in,
            "status": status,
            "pmt_ref": pmt_ref,
        })
        row_idx += 1

    # Bank reconciliation tie-out
    opening_cash = float(ws_bva["C21"].value or 0.0)
    misc_bal = float(ws_bva["B5"].value or 0.0)
    grso_bal = float(ws_bva["G5"].value or 0.0)
    cleared_in = sum(t["in"] for t in txns if t["status"] == "Cleared")
    cleared_out = sum(t["out"] for t in txns if t["status"] == "Cleared")
    encumbered_out = sum(t["out"] for t in txns if t["status"] == "Encumbered")
    expected_cash = opening_cash + cleared_in - cleared_out
    bank_variance = round((misc_bal + grso_bal) - expected_cash, 2)

    print("=" * 116)
    print(f"BUDGET & LEDGER AUDIT REPORT ({path.name})")
    print(
        f"MISC Balance: ${misc_bal:,.2f} | Encumbered: -${encumbered_out:,.2f} | "
        f"Available: ${misc_bal - encumbered_out:,.2f} | GRSO: ${grso_bal:,.2f} | Bank Rec Variance: ${bank_variance:,.2f}"
    )
    print("=" * 116)

    tot_in = sum(t["in"] for t in txns)
    tot_out = sum(t["out"] for t in txns)
    tot_net = tot_out - tot_in
    print(f"Ledger Entries: {len(txns)} | Money In: ${tot_in:,.2f} | Money Out: ${tot_out:,.2f} | Net Spend: ${tot_net:,.2f}\n")

    print(f"{'Line Item':<38} {'Approved':>12} {'Expenses':>12} {'Inflows':>12} {'Net Spent':>12} {'Remaining':>12} {'Status':<16}")
    print("-" * 116)

    dash_net = 0.0
    for b in budget_rows:
        if b["name"] == "Social Events":
            matched = [t for t in txns if ("Social" in t["category"] or "Gala" in t["category"])]
        elif b["is_subitem"]:
            matched = [t for t in txns if "Gala" in t["category"]]
        else:
            matched = [t for t in txns if t["category"] == b["cat_key"]]

        g_out = sum(t["out"] for t in matched)
        g_in = sum(t["in"] for t in matched)
        net = g_out - g_in
        rem = b["approved_budget"] - net
        if not b["is_subitem"]:
            dash_net += net

        unused = (g_out == 0 and g_in == 0)
        if b["is_passthrough"]:
            status = "Not Started" if unused else ("Reimbursed" if rem >= 0 else "Pending Reimb.")
        else:
            status = "Not Started" if unused else ("On Track" if rem >= 0 else "Over Budget")
        print(f"{b['name']:<38} {b['approved_budget']:>12,.2f} {g_out:>12,.2f} {g_in:>12,.2f} {net:>12,.2f} {rem:>12,.2f} {status:<16}")

    variance = round(tot_net - dash_net, 2)
    print("-" * 116)
    print(f"Dashboard Net Spend: ${dash_net:,.2f} | Ledger Net Spend: ${tot_net:,.2f} | Unmapped Variance: ${variance:,.2f}")

    if abs(variance) > 0.005:
        errors.append(f"Unmapped ledger variance detected: ${variance:,.2f}")
    if abs(bank_variance) > 0.005:
        errors.append(f"Bank reconciliation variance detected: ${bank_variance:,.2f}")
    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print(f"  [!] {w}")
    if errors:
        print("\nAUDIT FAILED:")
        for e in errors:
            print(f"  [X] {e}")
        return 1

    print("\n[OK] AUDIT PASSED: All categories & statuses valid, zero unmapped or bank rec variance.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit budget workbook against ledger formulas.")
    parser.add_argument("workbook", nargs="?", type=Path, default=DEFAULT_WORKBOOK)
    args = parser.parse_args()
    sys.exit(audit_workbook(args.workbook))

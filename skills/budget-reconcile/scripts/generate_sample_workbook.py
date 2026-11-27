#!/usr/bin/env python3
"""
Generate an anonymized sample Student Organization Budget & Expense Tracker
(`sample_budget.xlsx`) with Cover, Spending Dashboard (including built-in Bank Rec),
Budget Summary, Ledger (with Cleared/Encumbered/Unapproved/Placeholder Status),
and Gala Assumptions tabs.
"""

from pathlib import Path
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation


DEFAULT_OUT = Path(__file__).resolve().parent.parent / "examples" / "sample_budget.xlsx"


def build_sample_workbook(output_path: Path = DEFAULT_OUT) -> None:
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    # Palette & Styles
    navy = "1B365D"
    accent = "2B547E"
    tbl_hdr_bg = "D9E1F2"
    zebra_bg = "F8FAFC"
    highlight_bg = "FFFBEB"
    border_col = "CBD5E1"

    f_title = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    f_sub = Font(name="Calibri", size=10, italic=True, color="E2E8F0")
    f_sec = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    f_thdr = Font(name="Calibri", size=10, bold=True, color="1E293B")
    f_bold = Font(name="Calibri", size=10, bold=True, color="0F172A")
    f_data = Font(name="Calibri", size=10, color="1E293B")

    fill_navy = PatternFill("solid", fgColor=navy)
    fill_accent = PatternFill("solid", fgColor=accent)
    fill_thdr = PatternFill("solid", fgColor=tbl_hdr_bg)
    fill_zebra = PatternFill("solid", fgColor=zebra_bg)
    fill_hi = PatternFill("solid", fgColor=highlight_bg)

    thin = Side(border_style="thin", color=border_col)
    thick = Side(border_style="medium", color="0F172A")
    b_thin = Border(left=thin, right=thin, top=thin, bottom=thin)
    b_tot = Border(left=thin, right=thin, top=thin, bottom=thick)

    fmt_curr = "$#,##0.00;($#,##0.00);\"-\""
    fmt_int = "#,##0"

    opening_cash = 10000.00
    misc_balance = 12200.00
    grso_balance = 1200.00

    # Generic Line Items:
    # (Name, Owner, Ticket Rev, Sponsor Grant, GA/Gov Grant, Gross Budget, Notes)
    line_items = [
        ("Cohort Allocations", "VP of Student Life", 0, 0, 0, -2500, "Equal allocations across member cohorts"),
        ("Social Events", "VP of Social", "='Gala Assumptions'!E3", 0, 1500, -20000, "Total Social budget: Spring Gala (-$3,000 net) + campus mixers (-$500 net)"),
        ("  ↳ Spring Gala (Sub-item)", "VP of Social", "='Gala Assumptions'!E3", 0, 1000, -19000, "Included in Social Events above (200 @ $75; $19,000 max spend; $1,000 GA grant)"),
        ("Signature Events", "VP of Events", 0, 0, 1000, -2000, "Annual welcome celebration"),
        ("Professional & Career", "VP of Career", 0, 0, 500, -1500, "Panels, workshops, and networking"),
        ("Academics & Case Competitions", "VP of Academics", 0, 0, 500, -1500, "Case competition travel and speaker series"),
        ("Community & DEI", "VP of Community", 0, 0, 500, -1000, "Affinity group co-sponsorships"),
        ("Operations & Admin", "VP Finance & President", 0, 0, 0, -1000, "Board logistics, software, and supplies"),
    ]

    # Sample Ledger Rows:
    # (Rec#, Date, Category, Event, Desc, Vendor, Owner, Approver, In, Out, Status, Ref, Notes)
    # Math tie-out: Opening $10,000 + Cleared In ($5,350) - Cleared Out ($1,950) = $13,400 ($12,200 MISC + $1,200 GRSO)
    sample_txns = [
        ("REC-001", "2026-08-18", "Signature Events", "Welcome Mixer", "Catering & Snacks", "Local Caterer", "VP of Events", "Treasurer", 0.00, 1200.00, "Cleared", "CalLinks #1001001", "Paid via CalLinks"),
        ("REC-002", "2026-08-25", "Signature Events", "Welcome Mixer", "Student Government Grant Received", "Student Government", "VP of Events", "Treasurer", 1000.00, 0.00, "Cleared", "GA GRSO (200001)", "Summer grant allocation"),
        ("REC-003", "2026-09-12", "Social Events", "Fall Mixer", "Fall Kickoff Mixer", "Neighborhood Cafe", "VP of Social", "Treasurer", 0.00, 350.00, "Cleared", "CalLinks #1001042", "Paid via CalLinks"),
        ("REC-004", "2026-09-20", "Spring Gala", "Spring Gala", "Gala Venue Deposit", "Civic Ballroom", "VP of Social", "Treasurer", 0.00, 2500.00, "Encumbered", "CalLinks #1001088", "Approved; waiting for check/ACH payout"),
        ("REC-005", "2026-10-05", "Spring Gala", "Spring Gala", "Gala Ticket Sales (Stripe Net)", "Stripe (Tickets)", "VP of Social", "Treasurer", 4350.00, 0.00, "Cleared", "Stripe Net Payouts", "60 tickets cleared in MISC ($4,500 gross less ~$150 fees)"),
        ("REC-006", "2026-10-12", "Campus Sponsor Grant (Pass-Through)", "Sponsor Dinner", "Department Welcome Dinner", "Campus Dining", "Campus Sponsor", "Treasurer", 0.00, 400.00, "Cleared", "CalLinks #1001105", "Paid; awaiting campus sponsor reimbursement"),
    ]

    # ==========================================
    # 1. Cover
    # ==========================================
    ws_cov = wb.create_sheet("Cover")
    ws_cov.views.sheetView[0].showGridLines = False
    ws_cov.merge_cells("A1:F1")
    ws_cov["A1"] = "Example Student Association | Budget & Expense Tracker"
    ws_cov["A1"].font = f_title
    ws_cov["A1"].fill = fill_navy
    ws_cov["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws_cov.merge_cells("A2:F2")
    ws_cov["A2"] = "Academic Year 2026–2027 (Anonymized Template)"
    ws_cov["A2"].font = f_sub
    ws_cov["A2"].fill = fill_navy
    ws_cov["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws_cov.row_dimensions[1].height = 28
    ws_cov.row_dimensions[2].height = 20

    meta = [
        ("Organization:", "Example Student Association"),
        ("Account Slug / ID:", "<org_slug> / <account_id>"),
        ("Opening Bank Balance:", "$10,000.00 (Start-of-year CalLinks cash)"),
        ("Budgeted Net Spend:", "-$8,500.00 (Planned draw from reserves)"),
        ("Last Updated:", "Sample Template"),
    ]
    for i, (k, v) in enumerate(meta, start=4):
        ws_cov.row_dimensions[i].height = 20
        ws_cov.cell(i, 2, k).font = f_bold
        ws_cov.cell(i, 3, v).font = f_data

    ws_cov.merge_cells("B10:F10")
    ws_cov["B10"] = "TABS IN THIS WORKBOOK"
    ws_cov["B10"].font = f_sec
    ws_cov["B10"].fill = fill_accent
    ws_cov["B10"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws_cov.row_dimensions[10].height = 22

    toc = [
        ("Spending Dashboard", "Budget vs. actual spending, cash balances, and automatic bank reconciliation."),
        ("Budget Summary", "Approved annual budget by event and portfolio owner."),
        ("Ledger", "Itemized log of receipts, ticket sales, grants, and Status (Cleared / Encumbered / Unapproved / Placeholder)."),
        ("Gala Assumptions", "Ticket pricing model and Gala budget vs. actuals."),
    ]
    for i, (tab, desc) in enumerate(toc, start=11):
        ws_cov.row_dimensions[i].height = 20
        c1 = ws_cov.cell(i, 2, tab)
        c1.font = f_bold
        c1.border = b_thin
        ws_cov.merge_cells(f"C{i}:F{i}")
        c2 = ws_cov.cell(i, 3, desc)
        c2.font = f_data
        for cc in range(3, 7):
            ws_cov.cell(i, cc).border = b_thin

    for col, w in [("A", 4), ("B", 26), ("C", 24), ("D", 20), ("E", 20), ("F", 24)]:
        ws_cov.column_dimensions[col].width = w

    # ==========================================
    # 2. Budget Summary
    # ==========================================
    ws_bs = wb.create_sheet("Budget Summary")
    ws_bs.merge_cells("A1:I1")
    ws_bs["A1"] = "Annual Budget Summary (AY 2026–2027)"
    ws_bs["A1"].font = f_title
    ws_bs["A1"].fill = fill_navy
    ws_bs["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws_bs.row_dimensions[1].height = 26

    bs_headers = [
        "Line Item", "Owner", "Ticket Revenue", "Campus Sponsor",
        "Gov / GA Grants", "Planned Spend (97%)", "Buffer (3%)", "Total Planned Spend", "Net Cost to Org"
    ]
    ws_bs.row_dimensions[3].height = 24
    for c_i, h in enumerate(bs_headers, 1):
        c = ws_bs.cell(3, c_i, h)
        c.font = f_thdr
        c.fill = fill_thdr
        c.border = b_thin
        c.alignment = Alignment(horizontal="center" if c_i >= 3 else "left", vertical="center", wrap_text=True)

    for idx, (name, owner, tix, spo, ga, gross, _note) in enumerate(line_items, start=4):
        ws_bs.row_dimensions[idx].height = 20
        c_nm = ws_bs.cell(idx, 1, name)
        c_nm.font = f_bold if idx in (4, 5) else (Font(name="Calibri", size=10, italic=True, color="475569") if idx == 6 else f_data)
        if idx == 6:
            c_nm.alignment = Alignment(horizontal="left", indent=2)
        ws_bs.cell(idx, 2, owner).font = f_data

        for c_i, val in [(3, tix), (4, spo), (5, ga), (8, gross)]:
            cell = ws_bs.cell(idx, c_i, val)
            cell.number_format = fmt_curr
            cell.alignment = Alignment(horizontal="right")

        ws_bs.cell(idx, 6, f"=H{idx}*0.97").number_format = fmt_curr
        ws_bs.cell(idx, 7, f"=H{idx}*0.03").number_format = fmt_curr
        c_net = ws_bs.cell(idx, 9, f"=SUM(C{idx}:E{idx}, H{idx})")
        c_net.number_format = fmt_curr
        c_net.font = f_bold
        for c_i in range(1, 10):
            ws_bs.cell(idx, c_i).border = b_thin

    ws_bs.row_dimensions[12].height = 22
    ws_bs.cell(12, 1, "Operating Subtotal").font = f_bold
    ws_bs.cell(12, 2, "All Portfolios").font = f_bold
    for c_i in range(3, 10):
        col = get_column_letter(c_i)
        cell = ws_bs.cell(12, c_i, f"=SUM({col}4:{col}5, {col}7:{col}11)")
        cell.font = f_bold
        cell.number_format = fmt_curr
        cell.alignment = Alignment(horizontal="right")
    for c_i in range(1, 10):
        ws_bs.cell(12, c_i).fill = fill_thdr
        ws_bs.cell(12, c_i).border = b_tot

    ws_bs.row_dimensions[13].height = 20
    ws_bs.cell(13, 1, "Campus Sponsor Grant (Pass-Through)").font = f_bold
    ws_bs.cell(13, 2, "Campus Sponsor").font = f_data
    for c_i, val in [(3, 0), (4, 3000), (5, 0), (6, 0), (7, 0), (8, -3000), (9, "=SUM(C13:E13, H13)")]:
        cell = ws_bs.cell(13, c_i, val)
        cell.number_format = fmt_curr
        cell.alignment = Alignment(horizontal="right")
    for c_i in range(1, 10):
        ws_bs.cell(13, c_i).border = b_thin

    ws_bs.row_dimensions[14].height = 24
    ws_bs.cell(14, 1, "TOTAL BUDGET (Net Reserve Spend)").font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    ws_bs.cell(14, 2, "Total from Bank").font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    for c_i in range(3, 10):
        col = get_column_letter(c_i)
        cell = ws_bs.cell(14, c_i, f"={col}12+{col}13")
        cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        cell.number_format = fmt_curr
        cell.alignment = Alignment(horizontal="right")
    for c_i in range(1, 10):
        ws_bs.cell(14, c_i).fill = fill_navy
        ws_bs.cell(14, c_i).border = b_tot

    for col, w in [("A", 36), ("B", 22), ("C", 16), ("D", 16), ("E", 16), ("F", 18), ("G", 14), ("H", 18), ("I", 18)]:
        ws_bs.column_dimensions[col].width = w

    # ==========================================
    # 3. Spending Dashboard (8-Column Executive View + Bank Rec)
    # ==========================================
    ws_bva = wb.create_sheet("Spending Dashboard")
    ws_bva.merge_cells("A1:H1")
    ws_bva["A1"] = "Spending Dashboard"
    ws_bva["A1"].font = f_title
    ws_bva["A1"].fill = fill_navy
    ws_bva["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws_bva.merge_cells("A2:H2")
    ws_bva["A2"] = "Approved budgets vs. actual spending, current CalLinks cash, and bank reconciliation."
    ws_bva["A2"].font = f_sub
    ws_bva["A2"].fill = fill_navy
    ws_bva["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws_bva.row_dimensions[1].height = 26
    ws_bva.row_dimensions[2].height = 18

    kpis = [
        ("CalLinks Account", "4-XX-XXXXXX (MISC)", None),
        ("Account Balance", misc_balance, fmt_curr),
        ("Pending Payments (Encumbered)", "=-SUMIFS(Ledger!J:J, Ledger!L:L, \"Encumbered\")", fmt_curr),
        ("Available Cash", "=B5+C5", fmt_curr),
        ("Campus Grant Receivable", "=F17", fmt_curr),
        ("Cash After Receivables", "=D5+E5", fmt_curr),
        ("GA Grant Account (GRSO)", grso_balance, fmt_curr),
        ("Total Available Cash", "=F5+G5", fmt_curr),
    ]
    ws_bva.row_dimensions[4].height = 24
    for c_i, (lbl, val, nfmt) in enumerate(kpis, 1):
        c_lbl = ws_bva.cell(4, c_i, lbl)
        c_lbl.font = Font(name="Calibri", size=9, bold=True, color="57606A")
        c_lbl.alignment = Alignment(horizontal="left", vertical="bottom", wrap_text=True)
        c_val = ws_bva.cell(5, c_i, val)
        c_val.font = Font(name="Calibri", size=12, bold=True, color="B91C1C" if c_i == 3 else ("15803D" if c_i == 5 else navy))
        if nfmt:
            c_val.number_format = nfmt

    ws_bva.merge_cells("A6:H6")
    ws_bva["A6"] = "Sample snapshot: $12,200.00 MISC balance minus $2,500.00 pending payments = $9,700.00 available (+ $400.00 sponsor receivable + $1,200.00 GA grant account)."
    ws_bva["A6"].font = Font(name="Calibri", size=9, italic=True, color="57606A")

    bva_headers = [
        "Line Item", "Owner", "Approved Budget (Net)", "Expenses (Out)",
        "Revenue & Grants (In)", "Net Spent", "Remaining", "Status"
    ]
    ws_bva.row_dimensions[7].height = 24
    for c_i, h in enumerate(bva_headers, 1):
        c = ws_bva.cell(7, c_i, h)
        c.font = f_thdr
        c.fill = fill_thdr
        c.border = b_thin
        c.alignment = Alignment(horizontal="center" if c_i >= 3 else "left", vertical="center")

    for idx, (name, _, _, _, _, _, _) in enumerate(line_items, start=8):
        bs_row = idx - 4
        ws_bva.row_dimensions[idx].height = 20
        c_nm = ws_bva.cell(idx, 1, name)
        c_nm.font = f_bold if idx in (8, 9) else (Font(name="Calibri", size=10, italic=True, color="475569") if idx == 10 else f_data)
        if idx == 10:
            c_nm.alignment = Alignment(horizontal="left", indent=2)
        ws_bva.cell(idx, 2, f"='Budget Summary'!B{bs_row}").font = f_data
        ws_bva.cell(idx, 3, f"=-'Budget Summary'!I{bs_row}").number_format = fmt_curr

        if idx == 9:
            ws_bva.cell(idx, 4, "=SUMIFS(Ledger!J:J, Ledger!C:C, \"*Social*\")+SUMIFS(Ledger!J:J, Ledger!C:C, \"*Gala*\")")
            ws_bva.cell(idx, 5, "=SUMIFS(Ledger!I:I, Ledger!C:C, \"*Social*\")+SUMIFS(Ledger!I:I, Ledger!C:C, \"*Gala*\")")
        elif idx == 10:
            ws_bva.cell(idx, 4, "=SUMIFS(Ledger!J:J, Ledger!C:C, \"*Gala*\")")
            ws_bva.cell(idx, 5, "=SUMIFS(Ledger!I:I, Ledger!C:C, \"*Gala*\")")
        else:
            ws_bva.cell(idx, 4, f"=SUMIFS(Ledger!J:J, Ledger!C:C, A{idx})")
            ws_bva.cell(idx, 5, f"=SUMIFS(Ledger!I:I, Ledger!C:C, A{idx})")

        ws_bva.cell(idx, 4).number_format = fmt_curr
        ws_bva.cell(idx, 5).number_format = fmt_curr
        ws_bva.cell(idx, 6, f"=D{idx}-E{idx}").number_format = fmt_curr
        c_rem = ws_bva.cell(idx, 7, f"=C{idx}-F{idx}")
        c_rem.number_format = fmt_curr
        c_rem.font = f_bold
        c_rem.fill = fill_hi
        c_st = ws_bva.cell(idx, 8, f'=IF(AND(D{idx}=0, E{idx}=0), "Not Started", IF(G{idx}>=0, "On Track", "Over Budget"))')
        c_st.alignment = Alignment(horizontal="center")
        for c_i in range(1, 9):
            ws_bva.cell(idx, c_i).border = b_thin
            if idx % 2 == 0 and c_i != 7:
                ws_bva.cell(idx, c_i).fill = fill_zebra

    # Row 16: Operating Subtotal
    ws_bva.row_dimensions[16].height = 22
    ws_bva.cell(16, 1, "Operating Subtotal").font = f_bold
    ws_bva.cell(16, 2, "All Portfolios").font = f_bold
    for c_i in range(3, 8):
        col = get_column_letter(c_i)
        cell = ws_bva.cell(16, c_i, f"=SUM({col}8:{col}9, {col}11:{col}15)")
        cell.font = f_bold
        cell.number_format = fmt_curr
    for c_i in range(1, 9):
        ws_bva.cell(16, c_i).fill = fill_thdr
        ws_bva.cell(16, c_i).border = b_tot

    # Row 17: Campus Sponsor Grant
    ws_bva.row_dimensions[17].height = 20
    ws_bva.cell(17, 1, "Campus Sponsor Grant (Pass-Through)").font = f_bold
    ws_bva.cell(17, 2, "='Budget Summary'!B13").font = f_data
    ws_bva.cell(17, 3, "=-'Budget Summary'!I13").number_format = fmt_curr
    ws_bva.cell(17, 4, "=SUMIFS(Ledger!J:J, Ledger!C:C, A17)").number_format = fmt_curr
    ws_bva.cell(17, 5, "=SUMIFS(Ledger!I:I, Ledger!C:C, A17)").number_format = fmt_curr
    ws_bva.cell(17, 6, "=D17-E17").number_format = fmt_curr
    c_r17 = ws_bva.cell(17, 7, "=C17-F17")
    c_r17.number_format = fmt_curr
    c_r17.font = f_bold
    c_r17.fill = fill_hi
    c_s17 = ws_bva.cell(17, 8, '=IF(AND(D17=0, E17=0), "Not Started", IF(G17>=0, "Reimbursed", "Pending Reimbursement"))')
    c_s17.alignment = Alignment(horizontal="center")
    for c_i in range(1, 9):
        ws_bva.cell(17, c_i).border = b_thin

    # Row 18: Total Budget
    ws_bva.row_dimensions[18].height = 24
    ws_bva.cell(18, 1, "TOTAL BUDGET (Net Bank Spend)").font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    ws_bva.cell(18, 2, "Total Money from Bank").font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    for c_i in range(3, 8):
        col = get_column_letter(c_i)
        cell = ws_bva.cell(18, c_i, f"={col}16+{col}17")
        cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        cell.number_format = fmt_curr
    for c_i in range(1, 9):
        ws_bva.cell(18, c_i).fill = fill_navy
        ws_bva.cell(18, c_i).border = b_tot

    # Rows 20-26: Built-In Bank Reconciliation Tie-Out
    ws_bva.merge_cells("A20:D20")
    ws_bva["A20"] = "BANK RECONCILIATION (CASH TIE-OUT)"
    ws_bva["A20"].font = f_sec
    ws_bva["A20"].fill = fill_accent
    ws_bva["A20"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws_bva.row_dimensions[20].height = 22

    rec_rows = [
        ("Opening Cash (Start of Year)", opening_cash, "Entered from prior-year closing balance", False),
        ("Plus: Cleared Inflows (Status = Cleared)", "=SUMIFS(Ledger!I:I, Ledger!L:L, \"Cleared\")", "Ticket payouts & grants deposited into CalLinks", False),
        ("Less: Cleared Expenses (Status = Cleared)", "=-SUMIFS(Ledger!J:J, Ledger!L:L, \"Cleared\")", "Payments that have already left CalLinks", False),
        ("Expected Combined Bank Balance (MISC + GRSO)", "=SUM(C21:C23)", "Should equal MISC Balance (B5) + GRSO Balance (G5)", True),
        ("Actual CalLinks Balance (MISC + GRSO)", "=B5+G5", "Live total from CalLinks Accounts page", False),
        ("Bank Reconciliation Variance", "=C25-C24", "Must be $0.00 (any gap means a missing cleared row)", True),
    ]
    for offset, (lbl, val, note, is_tot) in enumerate(rec_rows, start=21):
        ws_bva.row_dimensions[offset].height = 20
        ws_bva.merge_cells(f"A{offset}:B{offset}")
        c_l = ws_bva.cell(offset, 1, lbl)
        c_l.font = f_bold if is_tot else f_data
        c_v = ws_bva.cell(offset, 3, val)
        c_v.number_format = fmt_curr
        c_v.font = f_bold if is_tot else f_data
        c_n = ws_bva.cell(offset, 4, note)
        c_n.font = Font(name="Calibri", size=9, italic=True, color="57606A")
        for c_i in range(1, 5):
            ws_bva.cell(offset, c_i).border = b_tot if is_tot else b_thin
            if is_tot:
                ws_bva.cell(offset, c_i).fill = fill_hi if offset == 26 else fill_thdr

    for col, w in [("A", 36), ("B", 22), ("C", 24), ("D", 22), ("E", 22), ("F", 18), ("G", 20), ("H", 24)]:
        ws_bva.column_dimensions[col].width = w

    # ==========================================
    # 4. Ledger (with Status column L)
    # ==========================================
    ws_led = wb.create_sheet("Ledger")
    ws_led.merge_cells("A1:N1")
    ws_led["A1"] = "Transaction Ledger (AY 2026–2027)"
    ws_led["A1"].font = f_title
    ws_led["A1"].fill = fill_navy
    ws_led["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws_led.row_dimensions[1].height = 26

    led_headers = [
        "Receipt #", "Date", "Budget Category", "Event / Format", "Item Description",
        "Vendor / Payee", "Portfolio Owner", "Approved By", "Money In (Tickets/Grants)",
        "Money Out (Expenses)", "Net Amount", "Status", "CalLinks # / Method", "Notes"
    ]
    ws_led.row_dimensions[4].height = 24
    for c_i, h in enumerate(led_headers, 1):
        c = ws_led.cell(4, c_i, h)
        c.font = f_thdr
        c.fill = fill_thdr
        c.border = b_thin
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    dv_status = DataValidation(type="list", formula1='"Cleared,Encumbered,Unapproved,Placeholder"', allow_blank=False)
    ws_led.add_data_validation(dv_status)

    for idx, row_t in enumerate(sample_txns, start=5):
        ws_led.row_dimensions[idx].height = 20
        for c_i, val in enumerate(row_t[:10], 1):
            cell = ws_led.cell(idx, c_i, val)
            cell.font = f_data
            if c_i in (9, 10):
                cell.number_format = fmt_curr
                cell.alignment = Alignment(horizontal="right")
        c_net = ws_led.cell(idx, 11, f"=I{idx}-J{idx}")
        c_net.number_format = fmt_curr
        c_net.alignment = Alignment(horizontal="right")
        c_st = ws_led.cell(idx, 12, row_t[10])
        c_st.font = f_bold
        c_st.alignment = Alignment(horizontal="center")
        dv_status.add(c_st)
        ws_led.cell(idx, 13, row_t[11]).font = f_data
        ws_led.cell(idx, 14, row_t[12]).font = f_data
        for c_i in range(1, 15):
            ws_led.cell(idx, c_i).border = b_thin

    tot_r = 5 + len(sample_txns)
    ws_led.row_dimensions[tot_r].height = 22
    ws_led.cell(tot_r, 1, "TOTAL TRANSACTIONS LOGGED").font = f_bold
    for c_i in (9, 10, 11):
        col = get_column_letter(c_i)
        c = ws_led.cell(tot_r, c_i, f"=SUM({col}5:{col}{tot_r-1})")
        c.font = f_bold
        c.number_format = fmt_curr
    for c_i in range(1, 15):
        ws_led.cell(tot_r, c_i).fill = fill_thdr
        ws_led.cell(tot_r, c_i).border = b_tot

    for col, w in [("A", 12), ("B", 12), ("C", 34), ("D", 16), ("E", 32), ("F", 22), ("G", 18), ("H", 14), ("I", 18), ("J", 18), ("K", 16), ("L", 14), ("M", 20), ("N", 34)]:
        ws_led.column_dimensions[col].width = w

    # ==========================================
    # 5. Gala Assumptions
    # ==========================================
    ws_gala = wb.create_sheet("Gala Assumptions")
    for c_i, h in enumerate(["Event", "Expected Attendees", "Ticket Price ($)", "Total Ticket Sales ($)"], 2):
        c = ws_gala.cell(2, c_i, h)
        c.font = f_thdr
        c.fill = fill_thdr
        c.border = b_thin
        c.alignment = Alignment(horizontal="center")

    ws_gala.cell(3, 2, "Spring Gala").font = f_bold
    ws_gala.cell(3, 3, 200).number_format = fmt_int
    ws_gala.cell(3, 4, 75).number_format = fmt_curr
    c_e3 = ws_gala.cell(3, 5, "=C3*D3")
    c_e3.font = f_bold
    c_e3.number_format = fmt_curr
    c_e3.fill = fill_hi
    for c_i in range(2, 6):
        ws_gala.cell(3, c_i).border = b_thin

    ws_gala.merge_cells("B5:E5")
    ws_gala["B5"] = "SPRING GALA — BUDGET VS. ACTUALS"
    ws_gala["B5"].font = f_sec
    ws_gala["B5"].fill = fill_accent
    ws_gala["B5"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws_gala.row_dimensions[5].height = 22

    for c_i, h in enumerate(["Category", "Budget", "Actual & Committed", "Variance"], 2):
        c = ws_gala.cell(6, c_i, h)
        c.font = f_thdr
        c.fill = fill_thdr
        c.border = b_thin
        c.alignment = Alignment(horizontal="center" if c_i > 2 else "left")

    gala_rows = [
        ("Ticket Sales (net of Stripe fees)", "='Budget Summary'!C6", "=SUMIFS(Ledger!I:I, Ledger!C:C, \"*Gala*\", Ledger!F:F, \"*Stripe*\")", "=D7-C7", False),
        ("Student Government Grant", "='Budget Summary'!E6", "=SUMIFS(Ledger!I:I, Ledger!C:C, \"*Gala*\", Ledger!F:F, \"*Government*\")", "=D8-C8", False),
        ("Total Revenue & Grants", "=SUM(C7:C8)", "=SUM(D7:D8)", "=D9-C9", True),
        ("Expenses Logged", "='Budget Summary'!H6", "=-SUMIFS(Ledger!J:J, Ledger!C:C, \"*Gala*\")", "=D10-C10", False),
        ("Net Cost to Org", "=C9+C10", "=D9+D10", "=D11-C11", True),
    ]
    for offset, (lbl, bud, act, var, is_tot) in enumerate(gala_rows, start=7):
        ws_gala.row_dimensions[offset].height = 20
        ws_gala.cell(offset, 2, lbl).font = f_bold if is_tot else f_data
        for c_i, v in [(3, bud), (4, act), (5, var)]:
            c = ws_gala.cell(offset, c_i, v)
            c.number_format = fmt_curr
            c.font = f_bold if is_tot else f_data
        for c_i in range(2, 6):
            ws_gala.cell(offset, c_i).border = b_tot if is_tot else b_thin
            if is_tot:
                ws_gala.cell(offset, c_i).fill = fill_thdr

    for col, w in [("A", 4), ("B", 38), ("C", 20), ("D", 22), ("E", 22)]:
        ws_gala.column_dimensions[col].width = w

    wb._sheets = [wb["Cover"], wb["Spending Dashboard"], wb["Budget Summary"], wb["Ledger"], wb["Gala Assumptions"]]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)
    print(f"Generated sample workbook: {output_path}")


if __name__ == "__main__":
    build_sample_workbook()

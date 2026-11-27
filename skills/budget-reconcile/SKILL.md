---
name: budget-reconcile
description: >-
  Use this skill when the user asks to categorize student organization transactions,
  reconcile CalLink or bank exports against a Budget vs. Actuals spreadsheet, preview
  portfolio impact, or update and audit a local budget workbook.
---

# Student Org Budget Reconciliation Skill

Follow this 4-step interactive workflow whenever reconciling transactions, grants, ticket payouts, or contracts into a local Budget vs. Actuals (BvA) workbook.

---

## Step 1: Audit Current Workbook & Identify Delta

1. **Inspect Existing Ledger:**
   - Run the audit script (e.g., `python3 ./scripts/audit_ledger.py path/to/workbook.xlsx`, tested against [examples/sample_budget.xlsx](./examples/sample_budget.xlsx)) or inspect the ledger tab to capture:
     - Existing transaction IDs (`REC-xxx`), payment references (`CalLinks #...`), and amounts.
     - Current approved net budgets and spent-so-far totals per category.
     - Recorded top-line bank/account KPIs (`Account Balance`, `Encumbered`, `Available Cash`).
2. **Compare Against Incoming Data:**
   - If live CalLink data is needed, invoke `callink-finance` first to extract and verify the current snapshot.
   - Match incoming transactions against existing rows by `Request #`, vendor, date, and amount.
   - Flag:
     - **New Transactions:** Not yet logged locally.
     - **Status / Amount Changes:** Previously pending/encumbered items that cleared, changed amount, or had line items removed.
     - **Inter-Account / Grant Activity:** Separate restricted grant account inflows/replenishments from operating reimbursements so grants aren't double-counted.

---

## Step 2: Confirm Categories (Human-in-the-Loop)

Before modifying any spreadsheet or script:
1. Load the workspace's official category list (e.g., from the Budget Summary tab, audit script, or [examples/sample_categories.json](./examples/sample_categories.json) as a template).
2. Present ambiguous or judgment-call items to the user one step at a time with a recommended category and ask them to confirm:
   - Which budget category each item belongs to.
   - Whether unapproved/pending commitments or placeholders should be logged now or held until approved.
   - Whether any campus/sponsor reimbursements are receivable (`Pending Reimbursement`).

---

## Step 3: Preview Proposed Workbook Changes

Show the user:
1. **Proposed Ledger Rows** (`Receipt # | Date | Category | Description | Vendor | In ($) | Out ($) | Status (Cleared / Encumbered / Unapproved / Placeholder) | Ref`).
2. **Before → After Dashboard Impact** for every affected category:
   - `Approved Budget (Net)`
   - `Expenses (Out)` and `Revenue & Grants (In)`
   - `Net Spent` (Before → After)
   - `Remaining` (Before → After) and `Status` (`Not Started`, `On Track`, `Over Budget`, `Pending Reimbursement`).
3. Wait for explicit user approval before editing files. *(If the `.xlsx` file is open in Excel with a `~$` lock file, remind the user to close it first.)*

---

## Step 4: Apply, Rebuild & Verify

After user approval:
1. **Update Source Script / Workbook:**
   - Add/update ledger rows (including exact `Status`: `Cleared`, `Encumbered`, `Unapproved`, or `Placeholder`) and refresh top-line cash KPIs (`Account Balance`, `Pending Payments / Encumbered`, `Available Cash`, `Grant Receivables`).
   - Update version history / `Last Updated` metadata.
2. **Regenerate & Audit:**
   - Run the workbook generator (see [scripts/generate_sample_workbook.py](./scripts/generate_sample_workbook.py) for a clean template) and [scripts/audit_ledger.py](./scripts/audit_ledger.py).
   - Verify **zero unmapped variance** (`Dashboard Net Spend == Ledger Net Spend`) and **zero bank reconciliation variance** (`Opening Cash + Cleared Inflows - Cleared Expenses == Actual Bank Balance`).
3. **Sync Docs:**
   - Update the workspace `README.md` (if present) with the latest balances and version summary.

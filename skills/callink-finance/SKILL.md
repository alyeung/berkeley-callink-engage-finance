---
name: callink-finance
description: >-
  Use this skill when the user wants to inspect, extract, parse, or reconcile UC Berkeley
  CalLink (or Anthology Engage) Finance data — account balances, encumbrances, transactions,
  purchase requests, or grant accounts — using an authenticated browser session or uploaded
  screenshots, CSVs, PDFs, or pasted tables.
---

# CalLink / Anthology Engage Finance Skill

Use this workflow to extract and verify financial data from **UC Berkeley CalLink** (`callink.berkeley.edu`, powered by Anthology / CampusLabs Engage) without storing credentials or hardcoding organization details.

---

## 1. Acquire CalLink Finance Data (Auth-Safe)

CalLink is gated by **campus SSO + Duo 2FA**. Never attempt to bypass authentication or store credentials.

### Path A: Live Authenticated Browser Session (Preferred)
1. Determine the target organization slug and account ID:
   - Check the current workspace (`README.md`, `.agents/skills/`, or local scripts) for the org's CalLink URL or account IDs, or ask the user.
   - Standard Anthology Engage routes:
     - **Accounts Summary:** `https://callink.berkeley.edu/actionCenter/organization/<org_slug>/finance?tab=Accounts`
     - **Account Transactions:** `https://callink.berkeley.edu/actionCenter/organization/<org_slug>/Finance/Account/<account_id>?tab=Transactions`
     - **Account Requests (Encumbrances):** `https://callink.berkeley.edu/actionCenter/organization/<org_slug>/Finance/Account/<account_id>?tab=Requests`
     - **Purchase Requests List:** `https://callink.berkeley.edu/finance/<org_slug>/requests/purchase`
     - **Printable Request Detail (Server-Rendered):** `https://callink.berkeley.edu/actionCenter/organization/<org_slug>/finance/print/<internal_id>`
2. Check whether a browser tool (`chrome-devtools` MCP or `/browser`) is connected to an authenticated `callink.berkeley.edu` tab:
   - If not authenticated (or redirected to SSO), instruct the user to sign in manually in their browser and confirm once ready.
   - Stop and wait before reading pages.
3. Once authenticated, capture:
   - **All Accounts (`finance?tab=Accounts`):** Check both the main operating/miscellaneous account (e.g., `MISC`) and any separate student-government/grant accounts (e.g., `GA GRSO`).
   - **Account Header KPIs:** `Balance`, `Encumbered Funds`, and `Available Funds`.
   - **Paginated Transactions:** Walk `accounttransactions/<account_id>?Column=Id&Direction=Descending&page=N` back to the start of the fiscal/academic year so paginated rows (e.g., individual Stripe ticket payouts or checks) are not missed.
   - **Purchase Requests & Printable Details:** Check `PurchaseRequests` for `Unapproved` vs. `Approved` items. Note that `/finance/<org_slug>/requests/purchase/<internal_id>` is a client-rendered SPA, whereas `/finance/print/<internal_id>` provides server-rendered payee, category, account, and approval dates.

### Path B: Offline File / Paste Fallback
If the user provides a screenshot, PDF, CSV export, or raw copy-pasted table from CalLink:
- For screenshots/PDFs: extract every visible KPI and row (`Date`, `Ref / #`, `Vendor / Payee`, `Description`, `Status / Type`, `Amount`).
- For CSV, TSV, or pasted text tables: run the normalizer script:
  ```bash
  python3 ./scripts/parse_callink_export.py <input_file> --format markdown
  ```
  (Use the installed skill path if running globally, and pass `--format json` for machine-readable output.)

See [references/callink_navigation.md](./references/callink_navigation.md) for Engage URL patterns, encumbrance semantics, and common pitfalls.

---

## 2. Normalize & Audit the Extracted Snapshot

Before reporting numbers or updating any downstream ledger, verify the math:
1. **KPI Check:** Verify `Available Funds == Balance - Encumbered Funds`.
2. **Encumbrance Tie-Out:** Sum all approved Purchase Requests on the account that have not yet posted as `Payment` transactions in the `Transactions` tab, and verify they equal `Encumbered Funds`. Flag any `Unapproved` requests separately (not yet encumbered).
3. **Separate Grant Pools:** If the org has a separate grant account (e.g., `GRSO`), track its deposits and payouts separately from `MISC` so inter-account splits and grant replenishments are not double-counted.
4. **Classify Flows:** Separate `Money Out` (vendor payments, reimbursements, POs) from `Money In` (ticket processor payouts such as Stripe net of fees, campus/government grants, departmental reimbursements).

---

## 3. Handoff or Generic Diff

- **If a workspace-specific reconciliation skill exists** (e.g., in `.agents/skills/`), pass the verified CalLink snapshot and delta to that skill for category confirmation and workbook updates.
- **Otherwise:** Diff the extracted CalLink rows against any local CSV/XLSX/Markdown ledger by `Request #`, vendor, date, and amount, then present:
  1. Live cash position (`Balance`, `Encumbered`, `Available Funds` per account)
  2. New transactions (not yet logged locally)
  3. Status or amount changes (`Encumbered` → `Paid`, partial adjustments)
  4. Items logged locally that are missing from CalLink

---

## 4. Verification

After parsing or reconciling:
- Verify no pagination pages were truncated.
- Confirm that starting balance minus net activity plus/minus timing items reconciles to live `Available Funds` with `$0.00` unexplained variance.

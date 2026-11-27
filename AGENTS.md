# Workspace Guardrails & Style Guide

Follow these rules whenever working in this repository or using these skills.

## 1. Login & Security
* **Never bypass login or ask for secrets:** Never ask for, save, or log CalNet passwords, Duo 2FA codes, cookies, or session tokens.
* **User-authenticated access only:** Only read CalLink from a browser tab the user has already logged into themselves, or parse screenshots, CSVs, and PDFs they share in chat.

## 2. Spreadsheet & Budget Safety
* **Confirm before editing:** Never modify a budget spreadsheet or generator script silently. Always walk through new/changed items, confirm categories, and preview the before/after impact first.
* **Check for open Excel files:** If a `~$*.xlsx` lock file exists, ask the user to close Excel before regenerating the workbook.
* **Verify every change:** After editing any spreadsheet or script, run `audit_ledger.py` and confirm `$0.00` unmapped discrepancy.

## 3. Public Repo Privacy
* **Keep real club data in a private repo:** Never write real organization names, CalLink slugs, account IDs, chartstrings, student/vendor names, emails, or real `.xlsx`/`.pdf` files into this public template repo.
* **Run the privacy check before committing:**
  ```bash
  python3 scripts/check_privacy.py
  ```

## 4. Communication & Wording
* **Write like a human finance lead, not an AI:** Keep replies short, direct, and easy to scan.
* **Skip unexplained jargon:** Use plain English alongside (or instead of) accounting/CalLink terms:
  * Say **"money held for approved requests that haven't paid out yet"** (not just *"encumbered"*).
  * Say **"expenses minus ticket sales and grants"** (not just *"net outflow"*).
  * Say **"budget vs. actual spending"** (not *"BvA variance"*).
* **Be concrete:** Always show exact dollar amounts and clearly separate cash already in the bank from pending approvals or estimates.

---
name: callink-purchase-request
description: >-
  Use this skill when the user wants to prepare, validate, or fill out a Purchase
  Request (especially a Student Reimbursement) in UC Berkeley CalLink / Anthology
  Engage using a logged-in Chrome tab or a copy-paste checklist, pausing before
  final submission.
---

# CalLink / Anthology Engage Purchase Request Skill

Use this workflow to validate reimbursement packets and pre-fill the **Create Purchase Request** form on **UC Berkeley CalLink** (`callink.berkeley.edu`, powered by Anthology / CampusLabs Engage) without storing credentials or submitting without human sign-off.

> **Safety Rule:** Never click **Submit Request** (`#saveButton`) automatically. Always fill the form up to the final review step, verify attachments and fields, and let the user click **Submit Request** themselves.

---

## Step 1: Collect & Verify the Reimbursement Packet

Before opening or filling the CalLink form, verify every required payee and receipt detail:

1. **Payee Details (Must match the person who paid, NOT the submitting officer):**
   - `First Name` and `Last Name`
   - Physical US mailing address (`Street`, optional `Street Continued`, `City`, `State/Province`, `ZIP/Postal Code` — international mailing addresses are not supported)
   - Campus `Unique ID (UID)` from the campus directory or CalCentral.
     - **SID vs. UID Catch:** Reject 10-digit Student IDs (typically starting with `303` or `304`) and never accept an SSN. Campus Directory UIDs are typically shorter (e.g., 6–7 digits). If a payee submits a `303...` or `304...` number, flag it and ask for their Directory UID before filling the form.
   - Campus `.edu` email address (payment notifications go here) and phone number
2. **Consolidated PDF (`1` file per expense item, strictly `< 4 MB`):**
   - **Itemized merchant receipt:** Vendor name, transaction date, line items, total, and `$0.00` remaining balance (Amazon receipts must show shipped status; hotel folios must show zero balance; rideshares must show traveler name).
   - **Proof of payment:** Credit card or bank statement screenshot showing payee name, last 4 digits of card/account, date, vendor, and amount.
   - **Disallowed payment methods:** Cash, Venmo, Zelle, PayPal, or SNAP/EBT cannot be reimbursed.
   - **Disallowed reimbursement items:** Individual contracted services (DJs, photographers, speakers, caterers) must be paid directly via vendor/contract workflow, not reimbursed out-of-pocket.
   - **Size Check & Lossless Compression:** If the PDF is `>= 4 MB`, shrink it losslessly with `pypdf` (`compress_content_streams()` + object deduplication) so vector text stays crisp and size drops under `4 MB`. Ensure any locally saved reimbursement PDF containing student PII is git-ignored before saving inside a repository.
3. **Expenditure & Direct Deposit Details:**
   - Preferred payout method (`Direct Deposit - Answer Question 6.`, `Mail to Payee`, `Hold for Pickup...`, etc.)
   - If `Direct Deposit`: confirm **Q6** (`Payee has already successfully completed...` vs. `Payee hasn't completed... within 3 business days`).

If anything is missing or fails a check, stop and ask the user before filling CalLink.

---

## Step 2: Confirm Account, Compliance & Form Preview

1. **Confirm Funding Account:**
   - Check live `Available Funds` (via `callink-finance`) before choosing an account.
   - **Never select the `SUMMARY` account.**
   - If splitting one receipt across two accounts (e.g., supplies from a grant account and food from general reserves), prepare **two separate Purchase Requests** (`1 of 2` and `2 of 2` in `Subject`), upload an annotated receipt showing the split, and explain the split in **Question 5 (Special Instructions)** and **Additional Misc. Information**.
2. **Check Grant / Campus Compliance Rules (if charging a restricted grant account):**
   - Verify event submission deadline (e.g., 30 days post-event and semester cutoffs).
   - Verify per-attendee food caps, tip caps (20% max without written justification), and banned items (alcohol, single-use bottled water, non-compostable utensils, branded merch, UC staff/faculty gifts).
   - Capture `Event Details` (event date(s), location(s), estimated attendee count).
3. **Handling `> 6` Orders / Receipts:**
   - The CalLink form accepts up to **6 items per submission**. Offer the user two paths when >6 orders come from one purchase batch:
     - **Option A (1 consolidated PR):** Enter `Item #1` as the consolidated batch (e.g., `Orders #A-#B`), attach a single `< 4 MB` PDF containing a summary table (p. 1) + all itemized receipts + card statement, and summarize the contents in **`Description`**.
     - **Option B (Multiple PRs: `1 of N` … `N of N` in `Subject`):** Split across separate requests (up to 6 items per request).
4. **Top-to-Bottom Review Before Filling:**
   - Present the full proposed values in the **exact top-to-bottom order of the CalLink form** (`Request Details` → `Payee Information` → `Questions 1–6` → `Event Details` → `Item #1`), and let the user edit wording or confirm **`Item #1: Type of Expense`** (`Contracted Services/Performer`, `Copies/Printing`, `Food`, `Stipend`, `Supplies`, `Travel`, `Other`) and **Q6 Direct Deposit** status before writing to the tab.
   - **Keep Q5 & Misc. Info Clean:** Put routine consolidated-PDF explanations in **`Description`**. Leave **`Q5 (Special Instructions)`** and **`Item #1–#6 Additional Misc. Information`** **blank** unless there is an amount discrepancy, multi-account split, payee/receipt name mismatch, or a mileage rate (Travel).

---

## Step 3: Fill Out the CalLink Form (Auth-Safe)

Target URL:
`https://callink.berkeley.edu/actionCenter/organization/<org_slug>/Finance/CreatePurchaseRequest`

See [references/purchase_request_form.md](./references/purchase_request_form.md) for exact field labels, DOM IDs/selectors, dropdown options, and item fields (`Item #1`–`Item #6`).

### Path A: Live Authenticated Chrome Tab (Preferred)
1. Check via `chrome-devtools` MCP (`list_pages`) whether an authenticated `CreatePurchaseRequest` tab is open.
   - If redirected to SSO (`auth.berkeley.edu`), ask the user to log in manually and confirm when ready.
2. Take a fresh snapshot (`take_snapshot`) and fill fields in order using `fill_form`:
   - **Request Details:** `Subject`, `Description`, `Requested Amount`, `Categories` (`Reimbursement`), and `Account` (click `#accountSelectButton`, then click the target `a.account-picker[id="<account_id>"]` inside `#AccountGrid` — never `SUMMARY`).
   - **Payee Information:** `First Name`, `Last Name`, `Street`, `Street Continued (Optional)`, `City`, `State/Province`, `ZIP/Postal Code`.
   - **Questions 1–6 & Event Details:**
     - **Q1:** Select `YES` + enter `UID`, and check the UID certification box `#49448409` (or `No` if non-UC affiliate).
     - **Q2 & Q3:** Payee email and phone number.
     - **Q4:** `Expenditure Action` (e.g., `Direct Deposit - Answer Question 6.`).
     - **Q5:** `Special Instructions` (leave blank unless discrepancy, split, or payee mismatch).
     - **Q6:** `Direct Deposit` status (required if Q4 = Direct Deposit).
     - **Event Details:** Date(s), location(s), estimated attendees/recipients.
   - **Expense Items (`Item #1`–`Item #6`):** Date of Expense, Type of Expense, Vendor name, Location (`City, State`), Invoice Number (if any), Total of Expense, Additional Misc. Information (blank unless mileage rate or split), and click `Upload File` (`#fileUploadQuestion-...`) to attach the single `< 4 MB` PDF for that item.
     - *Note:* If browser MCP blocks automated file-picker uploads outside its workspace roots, open the `Upload File` modal (or tell the user) and provide the exact local file path to pick via `Choose File` → `OK`.
     - *Note:* Do not use Items #2–#6 to upload extra pages for Item #1; combine all pages for one expense into one PDF.

### Path B: Offline Copy-Paste Checklist
If no live browser tab is connected, output a clean field-by-field table matching [references/purchase_request_form.md](./references/purchase_request_form.md) with exact copy-paste values and file attachments ready for the user.

---

## Step 4: Pre-Submit Review & Post-Submit Handoff

1. **Stop Before Submit:** Re-read the filled form values in the DOM (`evaluate_script` / `take_snapshot`, confirming `TemporaryFileName` is populated) and present a concise verification summary:
   - Account selected, Category (`Reimbursement`), `Subject`, `Requested Amount`
   - Payee Name, Mailing Address, UID, Email, Payout Method & Q6 status
   - Attached PDF filename and item totals
2. **Ask the User to Click `Submit Request`:** Remind them that Purchase Requests cannot be edited after submission.
3. **Stage 1 → Stage 2 Reminder:**
   - Submitting places the request in **Stage 1 (Unapproved)**.
   - An authorized **ASUC/GA Agent who is NOT the payee** must review the attachments and advance the request to **Stage 2** (leaving a stage comment if any ASUC Finance corrections are needed).
4. **Budget Tracking Handoff:**
   - If a workspace budget reconciliation skill is present (e.g., `budget-reconcile` or `.agents/skills/reconcile-budget`), offer to log or update the submitted request as `Unapproved` once the user shares the Purchase Request `#`.

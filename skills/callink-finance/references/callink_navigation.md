# CalLink / Anthology Engage Finance Reference

## 1. Standard URL Routes

Replace `<org_slug>` with your organization's CalLink slug (e.g., `my-org`) and `<account_id>` with the numeric account ID from the Finance Accounts tab:

- **Accounts Overview:** `https://callink.berkeley.edu/actionCenter/organization/<org_slug>/finance?tab=Accounts`
- **Account Transactions:** `https://callink.berkeley.edu/actionCenter/organization/<org_slug>/Finance/Account/<account_id>?tab=Transactions`
- **Paginated Transactions Endpoint:** `https://callink.berkeley.edu/actioncenter/organization/<org_slug>/finance/accounttransactions/<account_id>?Column=Id&Direction=Descending&page=<n>`
- **Account Requests (Encumbered / Approved):** `https://callink.berkeley.edu/actionCenter/organization/<org_slug>/Finance/Account/<account_id>?tab=Requests&page=<n>`
- **Purchase Requests List:** `https://callink.berkeley.edu/finance/<org_slug>/requests/purchase`
- **Printable Purchase Request Detail:** `https://callink.berkeley.edu/actionCenter/organization/<org_slug>/finance/print/<internal_id>`

---

## 2. Core Finance Concepts

| Term | Meaning in CalLink / Engage | Reconciliation Note |
| :--- | :--- | :--- |
| **Account Balance** | Posted cash balance in the university chartstring (e.g., `4-XX-XXXXXX-00000-MISC-XXXX`) | Has not yet deducted open encumbrances |
| **Encumbered Funds** | Approved Purchase Requests / POs reserving funds prior to check/ACH/wire payout | Reduces `Available Funds` immediately on approval |
| **Available Funds** | `Account Balance - Encumbered Funds` | True spendable cash remaining in that account |
| **Unapproved Request** | Submitted request still in review (Stage 1/2) | Does **not** reduce `Available Funds` until approved |
| **Grant / GRSO Account** | Restricted student-government allocation pool (separate from `MISC`) | Track inflows/replenishments and payouts separately so transfers/splits aren't double-counted |

---

## 3. Common Pitfalls

1. **Pagination:** Account transactions default to 15 rows per page. Always page backward to the start of your fiscal year when summing ticket payouts (e.g., Stripe batches) or checking cleared payments.
2. **Client-Side SPA vs. Printable HTML:** `/finance/<org_slug>/requests/purchase/<internal_id>` loads as a React SPA, whereas `/actionCenter/organization/<org_slug>/finance/print/<internal_id>` returns server-rendered details (payee, category, chartstring account, approval timestamp, and payout schedule).
3. **Encumbrance Double-Counting:** When an approved request finally clears as a `Payment` in `Transactions`, its encumbrance drops off and `Balance` decreases. Never subtract both the encumbrance and the cleared payment for the same item.
4. **Processor Fees on Ticket Revenue:** Imported Stripe/ticket deposits reflect net payouts after processing fees (~3%), not gross ticket face value.
5. **SSO / Duo 2FA Timeouts:** If a session expires and redirects to `auth.berkeley.edu`, pause and ask the user to re-authenticate in their browser.

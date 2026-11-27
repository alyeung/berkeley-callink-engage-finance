# Berkeley CalLink & Engage Finance Skills

Plain-English AI instructions (`SKILL.md`) and spreadsheet tools for checking UC Berkeley CalLink balances, tracking ticket sales and grants, and keeping a club budget up to date.

Works with Claude Code, Codex, Cursor, Gemini CLI, Antigravity, or standalone Python.

### Why Clubs Use This
* **No more double-counting:** Separates cash already in the bank from money held for approved requests that haven't paid out yet (`Encumbered`) and unapproved drafts.
* **Tracks both accounts cleanly:** Keeps your main club account (`MISC`) and student-government grant pool (`GRSO`) straight so grant replenishments aren't counted twice.
* **Clear budget vs. actuals:** Shows **Expenses (Out)**, **Ticket Sales & Grants (In)**, and **Net Cost** side by side with a built-in **`$0.00` bank tie-out**.

---

## Install & Try in 60 Seconds

Choose whichever option is easiest for you:

* **One-line CLI install** *(for Claude Code, Codex, Cursor, Gemini CLI, Antigravity via [`skills.sh`](https://skills.sh))*:
  ```bash
  npx skills add alyeung/berkeley-callink-engage-finance
  ```
* **No terminal (Download ZIP):** Click **Code → Download ZIP** on [github.com/alyeung/berkeley-callink-engage-finance](https://github.com/alyeung/berkeley-callink-engage-finance), unzip it, and open the folder in your AI assistant (or copy `skills/` into your club repo's `.agents/skills/`).
* **Git clone:**
  ```bash
  git clone https://github.com/alyeung/berkeley-callink-engage-finance.git
  cp -r berkeley-callink-engage-finance/skills/* /path/to/your-private-budget-repo/.agents/skills/
  ```

### First Prompt (No Browser Setup Needed)
Take a screenshot or CSV export of your CalLink Account page (and Purchase Requests page), drop it into chat, and ask in plain English:
* *"How much money do we actually have left after pending payments, and how much came in from tickets and grants?"*
* *"Compare these CalLink rows to our Excel budget, suggest categories, and show me what changes before updating anything."*
* *"Check `skills/budget-reconcile/examples/sample_budget.xlsx` and walk me through adding a $250 mixer expense."*

You don't need exact wording — the assistant asks you to confirm categories and previews the before/after numbers before changing any file.

---

## What's Inside (Two Focused Skills)

| Folder | What It Does |
| :--- | :--- |
| [`skills/callink-finance`](skills/callink-finance/SKILL.md) | Extracts balances, pending payments, ticket sales, grants, and recent expenses from a CalLink screenshot, CSV, or live browser tab. Works even if you track budgets in Google Sheets or Notion. |
| [`skills/budget-reconcile`](skills/budget-reconcile/SKILL.md) | Matches CalLink activity to your Excel budget, tracks each row's status (`Cleared`, `Encumbered`, `Unapproved`, `Placeholder`), and runs a `$0.00` discrepancy check. Includes [sample_budget.xlsx](skills/budget-reconcile/examples/sample_budget.xlsx). |

### What the Output Looks Like (`sample_budget.xlsx`)

| Line Item | Approved (Net) | Expenses (Out) | Revenue & Grants (In) | Net Spent | Remaining | Status |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| **Social Events** | `$3,500.00` | `$2,850.00` | `$4,350.00` | `-$1,500.00` | `$5,000.00` | On Track |
| &nbsp;&nbsp;↳ *Spring Gala* | *`$3,000.00`* | *`$2,500.00`* | *`$4,350.00`* | *`-$1,850.00`* | *`$4,850.00`* | *On Track* |
| **Signature Events** | `$1,000.00` | `$1,200.00` | `$1,000.00` | `$200.00` | `$800.00` | On Track |
| **Campus Sponsor Grant** | `$0.00` | `$400.00` | `$0.00` | `$400.00` | `-$400.00` | Pending Reimb. |

---

## Login & Security (Duo 2FA)

CalLink sits behind UC Berkeley CalNet SSO and Duo two-factor authentication. These skills:
* **Never** ask for or save your password or login cookies.
* Only read a CalLink tab after **you** sign in yourself, or read screenshots/CSVs you share directly in chat.

---

## Optional: Read Your Open Chrome Tab Live

If you'd rather have your assistant read CalLink directly from Chrome instead of taking screenshots:

1. Add [`chrome-devtools-mcp`](https://github.com/ChromeDevTools/chrome-devtools-mcp) to your tool's MCP config (`.mcp.json`, `~/.claude.json`, or `~/.gemini/config/mcp_config.json`):
   ```json
   {
     "mcpServers": {
       "chrome-devtools": {
         "command": "npx",
         "args": ["-y", "chrome-devtools-mcp@latest", "--autoConnect"]
       }
     }
   }
   ```
2. In Chrome (144+), open `chrome://inspect/#remote-debugging` and check **Enable remote debugging**.
3. Log into CalLink in Chrome, refresh MCP servers in your tool, and ask your question.

---

## Standalone Python Scripts (No AI Needed)

*(The Excel generator/audit scripts require `openpyxl`: `pip install openpyxl`. `parse_callink_export.py` uses Python's standard library only.)*

```bash
# Turn a CalLink CSV/TSV export into a clean summary table
python3 skills/callink-finance/scripts/parse_callink_export.py export.csv --format markdown

# Build and audit the sample Excel budget (checks categories, statuses, and bank tie-out)
python3 skills/budget-reconcile/scripts/generate_sample_workbook.py
python3 skills/budget-reconcile/scripts/audit_ledger.py
```

---

## Keep Your Club's Real Data Private

Keep your real spreadsheets, contracts, org name, and account numbers in a **private** repository. Mention your CalLink URL or account number in your private repo's `README.md` so the skill knows which account to check.

This repo includes [AGENTS.md](AGENTS.md) guardrails (login safety, step-by-step confirmation, plain-language wording) and a privacy check script to run before pushing:

```bash
python3 scripts/check_privacy.py
```

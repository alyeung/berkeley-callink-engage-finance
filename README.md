# Berkeley CalLink & Engage Finance Skills

Plain-English AI instructions (`SKILL.md`) and spreadsheet helpers for checking UC Berkeley CalLink balances, tracking ticket sales and grants, and keeping a club budget up to date.

Works with any AI coding assistant that supports `SKILL.md` (Claude Code, Codex, Cursor, Gemini CLI, Antigravity), or standalone with Python.

---

## Start Here (60 Seconds, Zero Setup)

You do **not** need Node.js, Chrome debugging, or terminal scripts to try this:

1. **Get the skills from GitHub:**
   * **Easiest (no Git):** Click **Code → Download ZIP** on [github.com/alyeung/berkeley-callink-engage-finance](https://github.com/alyeung/berkeley-callink-engage-finance), unzip it, and either open that folder in your AI assistant or copy its `skills/` folder into your club budget folder's `.agents/skills/`.
   * **Or via terminal (`git clone`):**
     ```bash
     git clone https://github.com/alyeung/berkeley-callink-engage-finance.git
     cp -r berkeley-callink-engage-finance/skills/* /path/to/your-private-budget-repo/.agents/skills/
     ```
2. **Take a screenshot or export a CSV** from your CalLink Account page (and Purchase Requests page).
3. **Drop it into chat** and ask in plain English:
   * *"Here's a screenshot from CalLink. How much money do we actually have left after pending payments, and how much came in from tickets and grants?"*
   * *"Compare these CalLink rows to our Excel budget, suggest categories, and show me what changes before updating anything."*

The assistant handles the rest — and always asks you to confirm categories and preview the impact before touching your spreadsheet.

---

## What's Inside

| Folder | What It Does |
| :--- | :--- |
| [`skills/callink-finance`](skills/callink-finance/SKILL.md) | Reads your CalLink accounts (bank balance, money held for approved requests that haven't paid out yet, ticket sales, grants, and recent expenses) from a screenshot, CSV, or open Chrome tab. |
| [`skills/budget-reconcile`](skills/budget-reconcile/SKILL.md) | Compares new CalLink activity against your Excel budget, tracks each row's status (`Cleared`, `Encumbered`, `Unapproved`, `Placeholder`), includes a built-in bank tie-out (`$0.00` variance check), and comes with [sample_budget.xlsx](skills/budget-reconcile/examples/sample_budget.xlsx). |

They are split into two skills so any club can use `callink-finance` by itself (even if they use Google Sheets or Notion) or pair both together with Excel.

---

## Example Questions You Can Ask

You don't need exact wording:
* *"Check our CalLink balance, pending payments, ticket sales, and grants."*
* *"Pull new CalLink activity since last month and help me update our budget."*
* *"Audit `skills/budget-reconcile/examples/sample_budget.xlsx` and walk me through adding a $250 mixer expense."*

---

## Login & Security (Duo 2FA)

CalLink sits behind UC Berkeley CalNet login and Duo two-factor authentication. These skills:
* **Never** ask for or save your password or login cookies.
* Only read a CalLink tab after **you** sign in yourself, or read screenshots/CSVs you share directly in chat.

---

## Optional: Let Your AI Read Your Open Chrome Tab Live

If you'd rather have your assistant read CalLink directly from Chrome instead of taking screenshots:

1. Add [`chrome-devtools-mcp`](https://github.com/ChromeDevTools/chrome-devtools-mcp) to your tool's MCP config (for example `.mcp.json`, `~/.claude.json`, or `~/.gemini/config/mcp_config.json`):
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

### Global Shortcut Setup (Optional)
If you want `callink-finance` available in every project (not just one repo):
```bash
# Antigravity / Gemini
ln -s /path/to/berkeley-callink-engage-finance/skills/callink-finance ~/.gemini/config/skills/callink-finance
# Claude Code
ln -s /path/to/berkeley-callink-engage-finance/skills/callink-finance ~/.claude/skills/callink-finance
```

---

## Running the Python Scripts Directly (No AI Needed)

```bash
# Turn a CalLink CSV/TSV export into a clean summary table
python3 skills/callink-finance/scripts/parse_callink_export.py export.csv --format markdown

# Build and check the sample Excel budget (checks categories, statuses, and bank tie-out)
python3 skills/budget-reconcile/scripts/generate_sample_workbook.py
python3 skills/budget-reconcile/scripts/audit_ledger.py
```

---

## Keep Your Club's Real Data Private

Keep your real spreadsheets, contracts, org name, and account numbers in a **private** repository. Just mention your CalLink URL or account number in your private repo's `README.md` so the skill knows which account to check.

This repo includes [AGENTS.md](AGENTS.md) guardrails (login safety, confirm before editing, plain-language communication) and a privacy check script to run before pushing:

```bash
python3 scripts/check_privacy.py
```

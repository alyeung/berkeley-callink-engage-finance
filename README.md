# Berkeley CalLink & Engage Finance Skills

Tools and AI instructions (`SKILL.md`) for checking UC Berkeley CalLink balances, tracking ticket sales and grants, and updating a club budget spreadsheet.

Works with any AI coding assistant that supports `SKILL.md` or browser MCP (Claude Code, Codex, Cursor, Gemini CLI, Antigravity), or on its own using the Python scripts included.

---

## What's Inside

| Folder | What It Does |
| :--- | :--- |
| [`skills/callink-finance`](skills/callink-finance/SKILL.md) | Reads your CalLink accounts (including bank balance, money held for approved requests that haven't paid out yet, ticket sales, grants, and recent expenses) from an open browser tab, screenshot, or CSV export. |
| [`skills/budget-reconcile`](skills/budget-reconcile/SKILL.md) | Compares new CalLink activity against your Excel budget, asks you which category each item belongs to, updates the spreadsheet, and checks that all totals match. Includes a sample workbook ([sample_budget.xlsx](skills/budget-reconcile/examples/sample_budget.xlsx)). |

They are split into two skills so any club can use `callink-finance` by itself (even if they track their budget in Google Sheets or Notion) or use both together with Excel.

---

## Security & Login (Duo 2FA)

CalLink is behind UC Berkeley CalNet login and Duo two-factor authentication. These skills:
* **Never** ask for or save your password or login cookies.
* Only read a CalLink tab after **you** sign in yourself, or read screenshots/CSVs you share directly in chat.

---

## How to Use

You don't need exact wording — just ask in plain English. Once the skills are installed, your AI assistant knows when to use them.

### Step by Step
1. **Log into CalLink** in Chrome (or save a screenshot or CSV export of your account page).
2. **Ask your AI assistant** what you want to check or update.
3. **Review and confirm:** Before changing any file, the assistant shows you what's new, asks you to confirm categories (and whether to log pending requests), and previews how your budget totals will change.
4. **Verify:** After updating your spreadsheet, it runs `audit_ledger.py` to make sure every transaction maps to a valid category and the totals match.

### Things You Can Ask (Just Examples)
* *"Check our CalLink account. How much money do we actually have left after pending payments, and how much have we brought in from ticket sales and grants?"*
* *"Pull new CalLink transactions, ticket payouts, and grants since last month and help me update our budget spreadsheet."*
* *"Here's a screenshot / CSV from CalLink — clean it up and show me what's not in our budget yet."*
* *"Check `skills/budget-reconcile/examples/sample_budget.xlsx` and walk me through adding a $250 mixer expense."*

---

## Setup

### 1. Add the Skills to Your AI Tool
Copy `skills/*` into your project's `.agents/skills/` folder (works in most tools), or link them globally:

```bash
# Project folder (works across Antigravity, Codex, Cursor, etc.)
cp -r skills/* /path/to/your-private-budget-repo/.agents/skills/

# Global shortcut (if you want them available in all projects)
ln -s /path/to/berkeley-callink-engage-finance/skills/callink-finance ~/.claude/skills/callink-finance
ln -s /path/to/berkeley-callink-engage-finance/skills/callink-finance ~/.gemini/config/skills/callink-finance
```

### 2. Let Your AI Read Your Open Chrome Tab (Optional)
If you want your assistant to read CalLink directly from your browser after you sign in:
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

*(Prefer not to connect Chrome? Just drop a screenshot or CSV export into chat instead.)*

---

## Running the Python Scripts Directly (No AI Needed)

```bash
# Turn a CalLink CSV/TSV export into a clean summary table
python3 skills/callink-finance/scripts/parse_callink_export.py export.csv --format markdown

# Build and check the sample Excel budget
python3 skills/budget-reconcile/scripts/generate_sample_workbook.py
python3 skills/budget-reconcile/scripts/audit_ledger.py
```

---

## Keep Your Club's Real Data Private

Keep your real spreadsheets, contracts, org name, and account numbers in a **private** repository. Just mention your CalLink URL or account number in your private repo's `README.md` so the skill knows which account to check.

This repo includes [AGENTS.md](AGENTS.md) guardrails (login safety, confirm before editing, plain-language communication) and a privacy check script you can run before pushing:

```bash
python3 scripts/check_privacy.py
```

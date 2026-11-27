# Berkeley CalLink & Anthology Engage Finance Skills

Open-standard **Agent Skills** (`SKILL.md`) and Python helpers for extracting, auditing, and reconciling student organization finances on **UC Berkeley CalLink** (and other **Anthology / CampusLabs Engage** campuses).

Works with any agent supporting `SKILL.md` and/or MCP (Claude Code, Codex, Cursor, Gemini CLI, Antigravity, etc.), or standalone via the included Python scripts.

---

## Included Skills

| Skill | Purpose | Use When |
| :--- | :--- | :--- |
| [`skills/callink-finance`](skills/callink-finance/SKILL.md) | **Extract & Normalize** | Reading live CalLink balances, encumbrances, paginated transactions, Purchase Requests, or parsing CSV/TSV/screenshot exports. |
| [`skills/budget-reconcile`](skills/budget-reconcile/SKILL.md) | **Categorize & Reconcile** | Diffing CalLink activity against a Budget-vs-Actuals workbook (includes an anonymized [sample_budget.xlsx](skills/budget-reconcile/examples/sample_budget.xlsx), generator, and audit script). |

Keeping them separate lets any organization use `callink-finance` standalone (regardless of where they track their budget) or pair both skills together.

---

## Auth & Security Model

CalLink sits behind **UC Berkeley CalNet SSO + Duo 2FA**. These skills:
* **Never** store passwords, cookies, or tokens.
* **Never** attempt to bypass authentication.
* Read from a browser session **you** already signed into (or from screenshots, PDFs, or CSV exports you share in chat).

---

## Quick Start

### 1. Install the Skills
Copy or symlink `skills/*` into your preferred agent's skills directory (project-local `.agents/skills/` works across most tools):

```bash
# Project-local (works in any repo across Antigravity, Codex, Cursor, etc.)
cp -r skills/* /path/to/your-private-budget-repo/.agents/skills/

# Global examples (choose your client):
# Claude Code:
ln -s /path/to/berkeley-callink-engage-finance/skills/callink-finance ~/.claude/skills/callink-finance
# Antigravity / Gemini:
ln -s /path/to/berkeley-callink-engage-finance/skills/callink-finance ~/.gemini/config/skills/callink-finance
```

### 2. Enable Live Chrome Reading (Optional, via MCP)
To let your AI client read CalLink tabs you already logged into via Chrome:
1. Add [`chrome-devtools-mcp`](https://github.com/ChromeDevTools/chrome-devtools-mcp) with `--autoConnect` to your client's MCP config (e.g., `.mcp.json`, `~/.claude.json`, or `~/.gemini/config/mcp_config.json`):
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
3. Sign into CalLink in Chrome, reload MCP servers in your client, and ask it to pull and reconcile your CalLink account.

*(No browser MCP? Drop a screenshot, CSV, or copy-pasted table from CalLink into chat and `parse_callink_export.py` will normalize it offline.)*

---

## Standalone Python Scripts (No AI Client Required)

```bash
# Normalize a CalLink CSV/TSV export into Markdown or JSON
python3 skills/callink-finance/scripts/parse_callink_export.py export.csv --format markdown

# Generate and audit the anonymized sample workbook
python3 skills/budget-reconcile/scripts/generate_sample_workbook.py
python3 skills/budget-reconcile/scripts/audit_ledger.py
```

---

## Keeping Org Data Private

Keep your actual workbooks, signed contracts, org slugs, account IDs, and board categories in a **private** repository. Point `callink-finance` at your org dynamically by noting your CalLink URL or account ID in your private repo's `README.md` or `.agents/skills/`.

# Berkeley CalLink & Anthology Engage Finance Skills

AI agent skills for extracting, auditing, and reconciling student organization finances on **UC Berkeley CalLink** (and other **Anthology / CampusLabs Engage** campuses).

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
* Read from a browser session **you** already signed into (or from screenshots, PDFs, or CSV exports you drop into chat).

---

## Quick Start

### 1. Install the Skills
Copy (or symlink) one or both skill folders into your Antigravity global skills directory (`~/.gemini/config/skills/`) or a project's `.agents/skills/` directory:

```bash
# Option A: Symlink globally (recommended if contributing back to this repo)
ln -s /path/to/berkeley-callink-engage-finance/skills/callink-finance ~/.gemini/config/skills/callink-finance
ln -s /path/to/berkeley-callink-engage-finance/skills/budget-reconcile ~/.gemini/config/skills/budget-reconcile

# Option B: Copy into a private org budget repo
cp -r skills/* /path/to/your-private-budget-repo/.agents/skills/
```

### 2. Enable Live Chrome Reading (Optional, Recommended)
To let the agent read CalLink tabs you already logged into via Chrome:
1. Add `chrome-devtools-mcp` with `--autoConnect` to `~/.gemini/config/mcp_config.json`:
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
3. Sign into CalLink in Chrome, refresh MCP servers in Antigravity, and run `/callink-finance`.

*(No browser MCP? Drop a screenshot, CSV, or copy-pasted table from CalLink into chat and `parse_callink_export.py` will normalize it offline.)*

---

## Keeping Org Data Private

Keep your actual workbooks, signed contracts, org slugs, account IDs, and board categories in a **private** repository. Point `callink-finance` at your org dynamically by noting your CalLink URL or account ID in your private repo's `README.md` or `.agents/skills/`.

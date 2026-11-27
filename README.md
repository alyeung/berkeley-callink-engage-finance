# Berkeley CalLink & Engage Finance Skills

Track spending for impact, prevent reconciliation mistakes, and account for every dollar in minutes. The UC Berkeley Haas Evening and Weekend MBA Association VP of Finance uses this system to manage annual budgets, grants, and event P&L.

Works with Claude Code, Codex, Cursor, Gemini CLI, Antigravity, or standalone Python.

## Quick Start

```bash
npx skills add alyeung/berkeley-callink-engage-finance
```

*(Prefer manual install? Download the ZIP or `git clone` into your private repo's `.agents/skills/` folder.)*

Drop a CalLink Account or Purchase Requests screenshot (or a student's reimbursement email + PDF) into chat and ask:
* *"How much cash is actually left after pending payments, and what came in from tickets and grants?"*
* *"Check this reimbursement packet, shrink the PDF under 4 MB if needed, and pre-fill my CalLink Purchase Request before I submit."*
* *"Compare these CalLink rows to our Excel budget, suggest categories, and preview changes before editing."*
* *"Walk me through adding a $250 mixer expense to `skills/budget-reconcile/examples/sample_budget.xlsx`."*

## Sample Output ([`sample_budget.xlsx`](skills/budget-reconcile/examples/sample_budget.xlsx))

Separates **Expenses (Out)**, **Revenue & Grants (In)**, and **Net Spent** while reconciling `MISC`, `GRSO` grants, `Encumbered` holds, and a `$0.00` bank tie-out:

| Line Item | Approved (Net) | Expenses (Out) | Revenue & Grants (In) | Net Spent | Remaining | Status |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| **Social Events** | `$3,500.00` | `$2,850.00` | `$4,350.00` | `-$1,500.00` | `$5,000.00` | On Track |
| &nbsp;&nbsp;↳ *Spring Gala* | *`$3,000.00`* | *`$2,500.00`* | *`$4,350.00`* | *`-$1,850.00`* | *`$4,850.00`* | *On Track* |
| **Signature Events** | `$1,000.00` | `$1,200.00` | `$1,000.00` | `$200.00` | `$800.00` | On Track |
| **Campus Sponsor Grant** | `$0.00` | `$400.00` | `$0.00` | `$400.00` | `-$400.00` | Pending Reimb. |

## What's Inside

| Skill | Purpose |
| :--- | :--- |
| [`skills/callink-finance`](skills/callink-finance/SKILL.md) | Reads CalLink balances, holds, ticket sales, grants, and recent expenses from screenshots, CSVs, or a live Chrome tab. |
| [`skills/callink-purchase-request`](skills/callink-purchase-request/SKILL.md) | Validates student reimbursement packets and pre-fills the CalLink Create Purchase Request form, pausing before Submit. |
| [`skills/budget-reconcile`](skills/budget-reconcile/SKILL.md) | Maps CalLink activity to Excel categories, tracks `Cleared`/`Encumbered`/`Unapproved` status, and runs a `$0.00` variance check. |

## Security & Privacy

* **You handle CalNet + Duo 2FA:** Skills never ask for or store passwords or cookies, and only read a browser tab after you log in (or screenshots/CSVs you share).
* **Keep real numbers private:** Store real spreadsheets, contracts, and account numbers in a **private** repo (see [AGENTS.md](AGENTS.md)), and run `python3 scripts/check_privacy.py` before pushing public changes.

<details>
<summary>Optional: Live Chrome tab setup &amp; standalone Python scripts</summary>

**Live Chrome tab (`chrome-devtools-mcp`):** Add to `.mcp.json`, `~/.claude.json`, or `~/.gemini/config/mcp_config.json`, enable **Remote debugging** in Chrome `144+` at `chrome://inspect/#remote-debugging`, and log into CalLink before asking questions:

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

**Standalone Python (`openpyxl` required for Excel scripts):**

```bash
python3 skills/callink-finance/scripts/parse_callink_export.py export.csv --format markdown
python3 skills/budget-reconcile/scripts/generate_sample_workbook.py
python3 skills/budget-reconcile/scripts/audit_ledger.py
```

</details>

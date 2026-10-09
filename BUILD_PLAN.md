# Robo_CFO Build Plan

Robo_CFO is a bespoke AI finance agent from Lazarre Consulting Group. It runs a small
business's finance department: **bookkeeper, tax/EA and CFO**. It watches the books every
day, forecasts cash, texts the owner what matters, and never moves money without approval.

- **First client:** a solo-owner therapy practice, about $2M a year in revenue, with no CFO.
  Self-pay only: clients pay by card through Stripe or by wire. No insurance billing.
- **Product goal:** a reusable Robo_CFO core, configured for each new client.
- **Developer:** Clavel Lazarre, MBA, EA.
- **Language:** Python.

**Build order rule:** compliance before client data, books before forecasts, view-only
before anything that moves money.

---

## Who uses it

| Person | What they do with it |
|---|---|
| Owner (client) | Receives texts, asks questions by text, approves payments, sets limits |
| Backup approver (e.g., office manager) | Approves routine payments while the owner is out |
| Clavel, as CFO | Reviews forecasts, alerts and briefings; tunes rules |
| Clavel, as EA | Reviews tax estimates; reviews, signs and e-files returns; answers notices |
| Bookkeeping reviewer (Clavel or staff) | Clears uncertain transactions; signs off on month-end close |

## What it does

**Bookkeeper:** categorizes and records transactions, reconciles bank accounts, records
Stripe payouts and client wires, captures bills and receipts, books
payroll, closes the month (P&L, balance sheet, cash flow), tracks contractors for 1099s.

**Tax (EA-reviewed):** tax calendar and reminders, quarterly estimates and weekly
set-asides, S corp owner-pay planning, year-end close and tax package, draft returns for
EA review and filing, IRS and state notice intake.

**CFO:** daily cash check, 13-week cash outlook, payroll readiness, payroll tracking,
client payment tracking, seasonal outlook, owner time-off protection, ask-anything by
text, monthly one-page summary.

## What it never does

- Never moves money without the owner's (or backup approver's) approval, within set limits.
- Never files a tax return. The agent prepares; the EA reviews, signs and e-files.
- Never sends client names or session details by text. Client names are masked in texts and reports.
- Never holds client funds. Payments go from the client's own accounts.
- Does not charge clients or contact them. It only sees money as it comes in.
- Does not replace the payroll provider's payroll tax filings. It checks they were made.

---

## Architecture

| Part | Purpose | Python tools (proposed) |
|---|---|---|
| Web API and app | Approvals, settings, review queues, reports | FastAPI, Jinja2 or HTMX for simple pages |
| Database | Clients, transactions, forecasts, rules, alerts, approvals | PostgreSQL, SQLAlchemy 2, Alembic |
| Audit log | Every read, write, alert and approval, with who and when | Append-only Postgres table |
| Ledger | The books of record | Client's **QuickBooks Online** via the QuickBooks Online Accounting API |
| Bank data | Balances and transactions | Plaid (`plaid-python`) |
| Payroll data | Pay runs, employees, contractors | Finch (`finch-api`) or Gusto API |
| Client payments | Card payments, fees, refunds, disputes and payouts | Stripe API (`stripe`), read-only restricted key |
| Client wires | Incoming wires | Bank transactions via Plaid, matched to the client or invoice |
| AI agents | Bookkeeping, tax and CFO agents; plain-English texts; Q&A | Claude Agent SDK for Python, latest Claude models |
| Forecasting | 13-week cash flow, Stripe payout timing, seasonality | pandas, plain Python |
| Rules and alerts | Thresholds and checks per client | Rules stored as data, evaluated in Python |
| Messaging | Two-way texts | Twilio (`twilio`), A2P 10DLC registered |
| Scheduler | Daily syncs, weekly forecast, reminders | APScheduler to start; a task queue later if needed |
| Secrets | API keys and OAuth tokens | Cloud secrets manager, encrypted at rest |
| Hosting | Runs everything | A reputable cloud provider (e.g., AWS), encrypted at rest and in transit |
| Tests | Accounting math, forecast, rules | pytest, sandbox data only |

---

## Phase 0: Before any client data (weeks 1–2)

| # | Item | Notes |
|---|---|---|
| 1 | Start Twilio A2P 10DLC registration | Carrier approval can take 1–3 weeks |
| 2 | Service agreement, text-message consent, IRC §7216 consent | Confirm 7216 consent covers AI and third-party providers |
| 3 | Written Information Security Plan (WISP) | FTC Safeguards Rule / IRS Pub 4557; also covers client-confidentiality practices |
| 4 | Confirm EFIN | New applications can take up to ~45 days |
| 5 | E&O and cyber insurance | Covering software-driven advice and tax preparation |
| 6 | Developer sandboxes | Intuit Developer (QuickBooks Online), Plaid, Stripe (test mode), Finch or Gusto, Anthropic API, Twilio |
| 7 | Hosting account set up with encryption, backups and MFA | Before any client data arrives |

## Phase 1: Foundation and bookkeeper (weeks 2–6)

| # | Item | Done when |
|---|---|---|
| 8 | Project skeleton: repo layout, Postgres schema, secrets, login, audit log | Every read and write is logged |
| 9 | QuickBooks Online connection (OAuth 2.0): read accounts, transactions, bills, invoices, payroll entries; write categorizations and journal entries | Agent reads and writes in the QuickBooks sandbox |
| 10 | Bank transactions via Plaid; settle the bank-feed decision (see Open decisions) | No duplicate entries in QuickBooks |
| 11 | Categorization agent: rules plus Claude, with a confidence score per transaction | 90%+ auto-categorized on test data; the rest queued |
| 12 | Review queue: approve or fix flagged items; corrections become rules | A week's exceptions cleared in minutes |
| 13 | Client payment import: Stripe charges, fees, refunds and disputes booked as gross revenue less fees; each Stripe payout matched to its bank deposit; wires matched to clients | Every deposit in QuickBooks ties to a Stripe payout or an identified wire |
| 14 | Payroll import into payroll journal entries | Payroll books itself every pay run |
| 15 | Month-end close: reconciliation helper, checklist, P&L, balance sheet, cash flow | One clean month closed in the sandbox |

## Phase 2: CFO, view only (proposal stage 1, weeks 6–9)

| # | Item | Done when |
|---|---|---|
| 16 | 13-week cash forecast engine: payroll and tax dates, recurring bills, Stripe payout schedule, expected wires | Back-tested forecast is within an agreed margin |
| 17 | Rules and alerts engine: safety floor, payroll coverage, deadlines, unusual spending | Each rule produces a test alert |
| 18 | Outbound texts and scheduler: daily cash check, Monday outlook, payroll readiness | Texts arrive on time; no client names |
| 19 | CFO review dashboard: Clavel approves every briefing in month 1 | Nothing reaches the owner unreviewed |
| 20 | Monthly one-page summary | Generated from the closed books |

## Phase 3: Plan ahead and two-way texting (proposal stage 2, weeks 9–12)

| # | Item |
|---|---|
| 21 | Two-way texting and "ask anything": Claude answers using read-only tools over the books and forecast |
| 22 | Tax module: tax calendar, quarterly estimates, weekly set-asides, S corp owner-pay planning |
| 23 | Client payment tracking: declined cards, disputes and chargebacks, refunds, unpaid balances, missing payouts or wires |
| 24 | Seasonal model from 2–3 years of history |
| 25 | Owner time-off module: reserves, `LEAVE` and `EMERGENCY` commands, backup approver, automatic check-in |

## Phase 4: Year-end tax work (before tax season)

| # | Item |
|---|---|
| 26 | 1099 contractor tracking through the year |
| 27 | Year-end close and tax-ready package: trial balance, adjusting entries, workpapers exported for the EA's tax software |
| 28 | Draft return support: agent prepares; EA reviews, signs and e-files in their own tax software |
| 29 | IRS and state notice intake: upload, summarize, draft a response for EA review |

## Phase 5: Act with approval (proposal stage 3)

| # | Item |
|---|---|
| 30 | Secure approval app: MFA or passkeys, per-payment and daily limits, backup approver |
| 31 | Bill pay execution through the client's own bank or QuickBooks bill pay |
| 32 | Tax payment preparation (EFTPS and state systems): owner approves; paid from the client's own account |

## Phase 6: Make it a product (after client #1 is stable)

| # | Item |
|---|---|
| 33 | Multi-client support: one dashboard, data separated per client |
| 34 | Onboarding checklist and configuration templates (e.g., "therapy practice" defaults) |
| 35 | Monitoring: failed syncs, missed texts, error alerts to Clavel |

---

## Open decisions

1. **Bank feed vs. Plaid.** The QuickBooks Online API is not known to expose bank-feed
   "For Review" items (verify against the current API before building item 10). Options:
   - (a) Plaid brings transactions in, the agent writes entries to QuickBooks, and the
     QuickBooks bank feed is turned off for those accounts. Most automation.
   - (b) QuickBooks keeps its bank feed; the agent works on transactions after they are
     accepted. Simpler, less automation.
2. **Payroll source:** Finch (works across providers) or the client's payroll provider API directly.
3. **Wire matching:** how to identify which client sent each wire (memo, amount, invoice number).
4. **Hosting provider** and region.

## Privacy note

The practice is self-pay and does not bill insurance electronically, so it is most likely not
a HIPAA covered entity, and Robo_CFO would not be a business associate. Confirm with a
health care attorney. Client confidentiality still applies: mask client names, keep session
details out of the system, and follow the WISP. If the practice ever bills insurance
electronically, revisit HIPAA.

## First week

Start items 1, 4 and 6 in parallel. Then scaffold item 8, the project skeleton, in this repo.

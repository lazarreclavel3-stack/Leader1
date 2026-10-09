# Leader1
new leads on stuff happening

## jobfeed: entry-level blue-collar jobs for Skynet

`jobfeed` pulls postings from several job APIs and normalizes them into one schema.
It keeps entry-level blue-collar roles (warehouse, driving, trades, manufacturing,
facilities, kitchen, automotive) and drops anything senior, supervisory or white-collar.
It removes duplicates across sources, then writes the feed to a file or pushes it to Skynet.

It uses only the Python 3.10+ standard library, so there's nothing to install.

### Sources

| Source | Why it matters for blue-collar | Key |
|---|---|---|
| `careeronestop` | US DOL National Labor Exchange: state job banks, lots of hourly and trades jobs | free registration |
| `usajobs` | Federal jobs, including Wage Grade (WG) trades and labor | free |
| `adzuna` | Large aggregator with good warehouse, driving and trade coverage | free tier |
| `jooble` | Large aggregator | free on request |
| `greenhouse` / `lever` | Direct employer boards (e.g. `doordashusa`), with no keyword search; the classifier filters them | none |

Copy `.env.example` to `.env`, fill in the keys you have, and export them. Sources without
keys are skipped.

### Usage

```bash
set -a; . ./.env; set +a
python3 -m jobfeed --list-sources                      # what's configured
python3 -m jobfeed --location "Dallas, TX" --radius 30 --days 7 --out jobs.json
python3 -m jobfeed --keywords "forklift,cdl driver" --pages 3 --out jobs.ndjson
python3 -m jobfeed --location 75201 --push             # POST to Skynet
```

### Feeding Skynet

With `--push`, jobs are sent in batches of 200 to `SKYNET_INGEST_URL`:

```
POST $SKYNET_INGEST_URL
Authorization: Bearer $SKYNET_API_KEY
{"source": "leader1-jobfeed", "jobs": [ <job>, ... ]}
```

Each job looks like this:

```json
{
  "id": "adzuna:4821", "source": "adzuna", "source_id": "4821",
  "title": "Forklift Operator", "company": "Acme", "location": "Dallas, TX",
  "url": "https://...", "description": "...", "posted_at": "2026-10-02T00:00:00Z",
  "salary_min": 18.0, "salary_max": 22.0, "salary_period": "hour",
  "employment_type": "full_time", "category": "warehouse_logistics",
  "entry_level_score": 0.8, "tags": ["hourly", "signal:paid training"]
}
```

If Skynet would rather pull than receive pushes, run the CLI on a schedule (cron)
with `--out` and serve the file.

### Tuning

- Category and exclusion keyword lists are in `jobfeed/classify.py`.
- `entry_level_score` starts at 0.6 for a matching title. Each entry-level signal
  ("no experience", "paid training", "apprentice", ...) adds 0.1. Requiring 2+ or 3+
  years of experience subtracts 0.2 or 0.4. `--min-score` sets the cutoff (default 0.5).

### Tests

```bash
python3 -m unittest
```

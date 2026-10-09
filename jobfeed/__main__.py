"""CLI: python -m jobfeed --location "Dallas, TX" --out jobs.json [--push]"""
from __future__ import annotations

import argparse
import json
import sys

from . import skynet
from .models import SearchQuery
from .pipeline import DEFAULT_KEYWORDS, collect
from .sources import ALL_SOURCES


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="jobfeed", description=__doc__)
    p.add_argument("--sources", default="all", help=f"comma list of {','.join(ALL_SOURCES)} or 'all'")
    p.add_argument("--keywords", help="comma list of search terms (default: built-in blue-collar list)")
    p.add_argument("--location", help='e.g. "Dallas, TX" or a ZIP code (default: nationwide)')
    p.add_argument("--radius", type=int, default=25, help="miles")
    p.add_argument("--days", type=int, default=7, help="only postings from the last N days")
    p.add_argument("--pages", type=int, default=1, help="pages per keyword per source")
    p.add_argument("--min-score", type=float, default=0.5, help="entry-level score cutoff 0-1")
    p.add_argument("--out", default="-", help="output file (.json or .ndjson), '-' for stdout")
    p.add_argument("--push", action="store_true", help="POST results to SKYNET_INGEST_URL")
    p.add_argument("--list-sources", action="store_true", help="show which sources have credentials")
    args = p.parse_args(argv)

    if args.list_sources:
        for name, src in ALL_SOURCES.items():
            status = "ready" if src.configured() else f"needs {', '.join(src.env_vars)}"
            print(f"{name:15} {status}")
        return 0

    names = list(ALL_SOURCES) if args.sources == "all" else args.sources.split(",")
    unknown = [n for n in names if n not in ALL_SOURCES]
    if unknown:
        p.error(f"unknown source(s): {', '.join(unknown)}")
    sources = [ALL_SOURCES[n] for n in names if ALL_SOURCES[n].configured()]
    if not sources:
        print("no configured sources; run with --list-sources", file=sys.stderr)
        return 1

    query = SearchQuery(
        keywords=args.keywords.split(",") if args.keywords else DEFAULT_KEYWORDS,
        location=args.location,
        radius_miles=args.radius,
        days=args.days,
        max_pages=args.pages,
    )
    jobs = collect(sources, query, min_score=args.min_score)
    rows = [j.to_dict() for j in jobs]

    if args.out.endswith(".ndjson"):
        text = "".join(json.dumps(r) + "\n" for r in rows)
    else:
        text = json.dumps(rows, indent=2) + "\n"
    if args.out == "-":
        sys.stdout.write(text)
    else:
        with open(args.out, "w") as f:
            f.write(text)

    if args.push:
        print(f"pushed {skynet.push(jobs)} jobs to Skynet", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

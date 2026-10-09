from __future__ import annotations

import re
import sys
from collections.abc import Iterable

from .classify import classify
from .models import Job, SearchQuery
from .sources.base import Source

DEFAULT_KEYWORDS = [
    "warehouse associate", "forklift operator", "general laborer", "material handler",
    "delivery driver", "CDL driver", "production worker", "assembler", "machine operator",
    "janitor", "maintenance technician", "construction laborer", "welder", "apprentice",
    "landscaping", "line cook", "dishwasher", "lube technician",
]

_NORM_RE = re.compile(r"[^a-z0-9]+")


def _norm(text: str | None) -> str:
    return _NORM_RE.sub(" ", (text or "").lower()).strip()


def dedupe(jobs: Iterable[Job]) -> list[Job]:
    """Drop repeats of the same posting across sources, keeping the richest copy."""
    by_key: dict[tuple, Job] = {}
    seen_urls: dict[str, tuple] = {}
    for job in jobs:
        key = (_norm(job.title), _norm(job.company), _norm(job.location))
        key = seen_urls.get(job.url, key) if job.url else key
        existing = by_key.get(key)
        if existing is None:
            by_key[key] = job
        else:
            for attr in ("salary_min", "salary_max", "salary_period", "description",
                         "employment_type", "posted_at"):
                if not getattr(existing, attr) and getattr(job, attr):
                    setattr(existing, attr, getattr(job, attr))
        if job.url:
            seen_urls[job.url] = key
    return list(by_key.values())


def collect(sources: Iterable[Source], query: SearchQuery, min_score: float = 0.5) -> list[Job]:
    raw: list[Job] = []
    for source in sources:
        try:
            got = list(source.fetch(query))
        except Exception as e:  # one bad source must not sink the whole run
            print(f"[{source.name}] failed: {e}", file=sys.stderr)
            continue
        print(f"[{source.name}] fetched {len(got)} postings", file=sys.stderr)
        raw.extend(got)

    kept = [j for j in (classify(j) for j in raw) if j.entry_level_score >= min_score]
    jobs = dedupe(kept)
    jobs.sort(key=lambda j: j.posted_at or "", reverse=True)
    print(f"kept {len(jobs)} entry-level blue-collar jobs from {len(raw)} postings", file=sys.stderr)
    return jobs

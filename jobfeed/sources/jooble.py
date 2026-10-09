"""Jooble job search API. Free key on request: https://jooble.org/api/about"""
from __future__ import annotations

import os
import re

from ..http import request_json
from ..models import Job, SearchQuery
from .base import Source, strip_html, to_float

URL = "https://jooble.org/api/{key}"
_MONEY_RE = re.compile(r"\$?\s*(\d[\d,]*(?:\.\d+)?)\s*(k)?", re.IGNORECASE)


def parse_salary(text: str | None):
    """Turn strings like '$18 - $22 per hour' or '$45k' into (min, max, period)."""
    if not text:
        return None, None, None
    amounts = [float(n.replace(",", "")) * (1000 if k else 1) for n, k in _MONEY_RE.findall(text)]
    if not amounts:
        return None, None, None
    lower = text.lower()
    if "hour" in lower or "/hr" in lower:
        period = "hour"
    elif "year" in lower or "annum" in lower or "/yr" in lower:
        period = "year"
    else:
        period = "hour" if max(amounts) < 200 else "year"
    return min(amounts), max(amounts), period


def parse(payload: dict) -> list[Job]:
    jobs = []
    for r in payload.get("jobs") or []:
        lo, hi, period = parse_salary(r.get("salary"))
        jobs.append(Job(
            source="jooble",
            source_id=str(r.get("id")),
            title=strip_html(r.get("title")),
            url=r.get("link", ""),
            company=r.get("company") or None,
            location=r.get("location") or None,
            description=strip_html(r.get("snippet")),
            posted_at=r.get("updated"),
            salary_min=lo,
            salary_max=hi,
            salary_period=period,
            employment_type=r.get("type") or None,
        ))
    return jobs


class Jooble(Source):
    name = "jooble"
    env_vars = ("JOOBLE_API_KEY",)

    def fetch(self, query: SearchQuery):
        url = URL.format(key=os.environ["JOOBLE_API_KEY"])
        for kw in query.keywords:
            for page in range(1, query.max_pages + 1):
                body = {"keywords": kw, "page": str(page), "ResultOnPage": str(query.page_size)}
                if query.location:
                    body["location"] = query.location
                payload = request_json(url, method="POST", body=body)
                jobs = parse(payload or {})
                yield from jobs
                if len(jobs) < query.page_size:
                    break

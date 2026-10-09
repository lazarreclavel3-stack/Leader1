"""Public applicant-tracking-system boards (no API key needed).

These boards have no keyword search, so every posting is pulled and the
classifier keeps the blue-collar ones. Point them at employers that hire
hourly workers, e.g. GREENHOUSE_BOARDS="acme-logistics,another-co".
"""
from __future__ import annotations

import datetime as dt
import os
import sys
import urllib.error

from ..http import request_json
from ..models import Job, SearchQuery
from .base import Source, strip_html, to_float

GREENHOUSE_URL = "https://boards-api.greenhouse.io/v1/boards/{board}/jobs"
LEVER_URL = "https://api.lever.co/v0/postings/{company}"
LEVER_PERIODS = {"per-hour-wage": "hour", "per-year-salary": "year"}


def _env_list(var: str) -> list[str]:
    return [s.strip() for s in os.environ.get(var, "").split(",") if s.strip()]


def parse_greenhouse(payload: dict, board: str) -> list[Job]:
    return [
        Job(
            source="greenhouse",
            source_id=f"{board}:{r.get('id')}",
            title=r.get("title", ""),
            url=r.get("absolute_url", ""),
            company=r.get("company_name") or board,
            location=(r.get("location") or {}).get("name"),
            description=strip_html(r.get("content")),
            posted_at=r.get("updated_at"),
        )
        for r in payload.get("jobs") or []
    ]


def parse_lever(payload: list, company: str) -> list[Job]:
    jobs = []
    for r in payload or []:
        cats = r.get("categories") or {}
        pay = r.get("salaryRange") or {}
        created = r.get("createdAt")
        jobs.append(Job(
            source="lever",
            source_id=f"{company}:{r.get('id')}",
            title=r.get("text", ""),
            url=r.get("hostedUrl", ""),
            company=company,
            location=cats.get("location"),
            description=r.get("descriptionPlain") or "",
            posted_at=(dt.datetime.fromtimestamp(created / 1000, dt.timezone.utc).isoformat()
                       if created else None),
            salary_min=to_float(pay.get("min")),
            salary_max=to_float(pay.get("max")),
            salary_period=LEVER_PERIODS.get(pay.get("interval")),
            employment_type=cats.get("commitment"),
        ))
    return jobs


class Greenhouse(Source):
    name = "greenhouse"
    env_vars = ("GREENHOUSE_BOARDS",)

    def fetch(self, query: SearchQuery):
        for board in _env_list("GREENHOUSE_BOARDS"):
            try:
                payload = request_json(GREENHOUSE_URL.format(board=board), params={"content": "true"})
            except urllib.error.HTTPError as e:
                print(f"[greenhouse] board {board!r} skipped: {e}", file=sys.stderr)
                continue
            yield from parse_greenhouse(payload or {}, board)


class Lever(Source):
    name = "lever"
    env_vars = ("LEVER_COMPANIES",)

    def fetch(self, query: SearchQuery):
        for company in _env_list("LEVER_COMPANIES"):
            try:
                payload = request_json(LEVER_URL.format(company=company), params={"mode": "json"})
            except urllib.error.HTTPError as e:
                print(f"[lever] company {company!r} skipped: {e}", file=sys.stderr)
                continue
            yield from parse_lever(payload or [], company)

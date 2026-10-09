"""USAJOBS (federal jobs, including Wage Grade trades). Free key: https://developer.usajobs.gov/"""
from __future__ import annotations

import os

from ..http import request_json
from ..models import Job, SearchQuery
from .base import Source, strip_html, to_float

URL = "https://data.usajobs.gov/api/search"
RATE_PERIODS = {"PH": "hour", "PA": "year"}


def parse(payload: dict) -> list[Job]:
    items = (payload.get("SearchResult") or {}).get("SearchResultItems") or []
    jobs = []
    for item in items:
        d = item.get("MatchedObjectDescriptor") or {}
        pay = (d.get("PositionRemuneration") or [{}])[0]
        schedule = (d.get("PositionSchedule") or [{}])[0]
        details = ((d.get("UserArea") or {}).get("Details")) or {}
        jobs.append(Job(
            source="usajobs",
            source_id=str(item.get("MatchedObjectId") or d.get("PositionID")),
            title=d.get("PositionTitle", ""),
            url=d.get("PositionURI") or (d.get("ApplyURI") or [""])[0],
            company=d.get("OrganizationName"),
            location=d.get("PositionLocationDisplay"),
            description=strip_html(details.get("JobSummary") or d.get("QualificationSummary")),
            posted_at=d.get("PublicationStartDate"),
            salary_min=to_float(pay.get("MinimumRange")),
            salary_max=to_float(pay.get("MaximumRange")),
            salary_period=RATE_PERIODS.get(pay.get("RateIntervalCode")),
            employment_type=schedule.get("Name"),
        ))
    return jobs


class USAJobs(Source):
    name = "usajobs"
    env_vars = ("USAJOBS_API_KEY", "USAJOBS_EMAIL")

    def fetch(self, query: SearchQuery):
        headers = {
            "Host": "data.usajobs.gov",
            "User-Agent": os.environ["USAJOBS_EMAIL"],
            "Authorization-Key": os.environ["USAJOBS_API_KEY"],
        }
        for kw in query.keywords:
            for page in range(1, query.max_pages + 1):
                payload = request_json(URL, headers=headers, params={
                    "Keyword": kw,
                    "LocationName": query.location,
                    "Radius": query.radius_miles if query.location else None,
                    "DatePosted": min(query.days, 60),
                    "ResultsPerPage": query.page_size,
                    "Page": page,
                })
                jobs = parse(payload or {})
                yield from jobs
                if len(jobs) < query.page_size:
                    break

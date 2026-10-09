"""CareerOneStop (US Dept. of Labor / National Labor Exchange) job search.

Free registration: https://www.careeronestop.org/Developers/WebAPI/registration.aspx
Strong coverage of hourly, trades and state job-bank postings.
"""
from __future__ import annotations

import os
import urllib.parse

from ..http import request_json
from ..models import Job, SearchQuery
from .base import Source

URL = ("https://api.careeronestop.org/v1/jobsearch/{user}/{kw}/{loc}/{radius}"
       "/0/0/{start}/{size}/{days}")


def parse(payload: dict) -> list[Job]:
    return [
        Job(
            source="careeronestop",
            source_id=str(r.get("JvId")),
            title=r.get("JobTitle", ""),
            url=r.get("URL", ""),
            company=r.get("Company") or None,
            location=r.get("Location") or None,
            posted_at=r.get("DatePosted"),
        )
        for r in payload.get("Jobs") or []
    ]


class CareerOneStop(Source):
    name = "careeronestop"
    env_vars = ("CAREERONESTOP_USER_ID", "CAREERONESTOP_TOKEN")

    def fetch(self, query: SearchQuery):
        headers = {"Authorization": f"Bearer {os.environ['CAREERONESTOP_TOKEN']}"}
        q = urllib.parse.quote
        for kw in query.keywords:
            for page in range(query.max_pages):
                url = URL.format(
                    user=q(os.environ["CAREERONESTOP_USER_ID"]),
                    kw=q(kw),
                    loc=q(query.location or "US"),
                    radius=query.radius_miles,
                    start=page * query.page_size,
                    size=query.page_size,
                    days=min(query.days, 30),
                )
                jobs = parse(request_json(url, headers=headers) or {})
                yield from jobs
                if len(jobs) < query.page_size:
                    break

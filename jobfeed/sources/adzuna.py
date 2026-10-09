"""Adzuna job search API. Free key: https://developer.adzuna.com/"""
from __future__ import annotations

import os

from ..http import request_json
from ..models import Job, SearchQuery
from .base import Source, strip_html, to_float

URL = "https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"


def parse(payload: dict) -> list[Job]:
    jobs = []
    for r in payload.get("results") or []:
        has_salary = r.get("salary_min") is not None or r.get("salary_max") is not None
        job = Job(
            source="adzuna",
            source_id=str(r.get("id")),
            title=strip_html(r.get("title")),
            url=r.get("redirect_url", ""),
            company=(r.get("company") or {}).get("display_name"),
            location=(r.get("location") or {}).get("display_name"),
            description=strip_html(r.get("description")),
            posted_at=r.get("created"),
            salary_min=to_float(r.get("salary_min")),
            salary_max=to_float(r.get("salary_max")),
            # Adzuna reports salaries annualised.
            salary_period="year" if has_salary else None,
            employment_type=r.get("contract_time"),
        )
        if str(r.get("salary_is_predicted")) == "1":
            job.tags.append("salary_predicted")
        jobs.append(job)
    return jobs


class Adzuna(Source):
    name = "adzuna"
    env_vars = ("ADZUNA_APP_ID", "ADZUNA_APP_KEY")

    def fetch(self, query: SearchQuery):
        country = os.environ.get("ADZUNA_COUNTRY", "us")
        for kw in query.keywords:
            for page in range(1, query.max_pages + 1):
                payload = request_json(URL.format(country=country, page=page), params={
                    "app_id": os.environ["ADZUNA_APP_ID"],
                    "app_key": os.environ["ADZUNA_APP_KEY"],
                    "what": kw,
                    "where": query.location,
                    "distance": round(query.radius_miles * 1.609) if query.location else None,
                    "max_days_old": query.days,
                    "results_per_page": query.page_size,
                })
                jobs = parse(payload or {})
                yield from jobs
                if len(jobs) < query.page_size:
                    break

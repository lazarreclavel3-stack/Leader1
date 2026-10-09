"""Push the normalised job feed into Skynet.

Skynet's ingest contract is configured, not hard-coded:
  SKYNET_INGEST_URL  endpoint that accepts POST {"source": "leader1-jobfeed", "jobs": [...]}
  SKYNET_API_KEY     optional bearer token
"""
from __future__ import annotations

import os

from .http import request_json
from .models import Job


def push(jobs: list[Job], batch_size: int = 200) -> int:
    url = os.environ.get("SKYNET_INGEST_URL")
    if not url:
        raise RuntimeError("SKYNET_INGEST_URL is not set")
    headers = {}
    if os.environ.get("SKYNET_API_KEY"):
        headers["Authorization"] = f"Bearer {os.environ['SKYNET_API_KEY']}"
    for i in range(0, len(jobs), batch_size):
        batch = [j.to_dict() for j in jobs[i:i + batch_size]]
        request_json(url, method="POST", headers=headers,
                     body={"source": "leader1-jobfeed", "jobs": batch})
    return len(jobs)

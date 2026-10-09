from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = "leader1-jobfeed/0.1"
RETRY_STATUSES = {429, 500, 502, 503, 504}


def request_json(url, *, method="GET", params=None, headers=None, body=None, retries=3, timeout=30):
    """Send a JSON HTTP request with simple exponential-backoff retries."""
    if params:
        clean = {k: v for k, v in params.items() if v is not None and v != ""}
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(clean, doseq=True)
    data = json.dumps(body).encode() if body is not None else None
    hdrs = {"Accept": "application/json", "User-Agent": USER_AGENT}
    if data is not None:
        hdrs["Content-Type"] = "application/json"
    hdrs.update(headers or {})

    for attempt in range(retries):
        req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                return json.loads(raw) if raw else None
        except urllib.error.HTTPError as e:
            if e.code in RETRY_STATUSES and attempt < retries - 1:
                time.sleep(2**attempt)
                continue
            raise
        except urllib.error.URLError:
            if attempt < retries - 1:
                time.sleep(2**attempt)
                continue
            raise

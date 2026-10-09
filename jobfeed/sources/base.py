from __future__ import annotations

import html
import os
import re
from collections.abc import Iterator

from ..models import Job, SearchQuery

_TAG_RE = re.compile(r"<[^>]+>")


def strip_html(text: str | None) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", _TAG_RE.sub(" ", html.unescape(text))).strip()


def to_float(value) -> float | None:
    try:
        return float(str(value).replace(",", "").replace("$", ""))
    except (TypeError, ValueError):
        return None


class Source:
    """A job source. Subclasses implement fetch() and keep parsing in pure functions."""

    name: str = ""
    env_vars: tuple[str, ...] = ()

    def configured(self) -> bool:
        return all(os.environ.get(v) for v in self.env_vars)

    def fetch(self, query: SearchQuery) -> Iterator[Job]:
        raise NotImplementedError

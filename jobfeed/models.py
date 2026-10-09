from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class SearchQuery:
    keywords: list[str]
    location: str | None = None
    radius_miles: int = 25
    days: int = 7
    max_pages: int = 1
    page_size: int = 50


@dataclass
class Job:
    source: str
    source_id: str
    title: str
    url: str
    company: str | None = None
    location: str | None = None
    description: str = ""
    posted_at: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    salary_period: str | None = None  # "hour" | "year" | None
    employment_type: str | None = None
    # Filled in by the classifier.
    category: str | None = None
    entry_level_score: float = 0.0
    tags: list[str] = field(default_factory=list)

    @property
    def id(self) -> str:
        return f"{self.source}:{self.source_id}"

    def to_dict(self) -> dict:
        return {"id": self.id, **asdict(self)}

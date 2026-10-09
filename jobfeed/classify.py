"""Decide whether a posting is an entry-level blue-collar job, and score it."""
from __future__ import annotations

import re

from .models import Job

CATEGORIES: dict[str, list[str]] = {
    "warehouse_logistics": [
        "warehouse", "picker", "packer", "pick and pack", "forklift", "material handler",
        "materials handler", "loader", "unloader", "package handler", "order selector",
        "stocker", "shipping", "receiving", "dock worker", "fulfillment associate",
        "inventory associate", "mover",
    ],
    "driving_delivery": [
        "cdl", "truck driver", "delivery driver", "driver helper", "courier", "route driver",
        "box truck", "van driver", "shuttle driver", "bus driver", "yard driver", "driver",
    ],
    "construction_trades": [
        "laborer", "general labor", "construction", "carpenter", "electrician", "plumber",
        "hvac", "roofer", "painter", "mason", "welder", "welding", "pipefitter", "drywall",
        "concrete", "framer", "insulation", "flagger", "apprentice", "trade helper",
        "electrical helper", "plumbing helper",
    ],
    "manufacturing": [
        "production worker", "production associate", "assembler", "assembly", "machine operator",
        "machinist", "cnc operator", "fabricator", "fabrication", "line worker", "packaging",
        "press operator", "sanitation worker", "manufacturing associate", "factory",
    ],
    "maintenance_facilities": [
        "maintenance", "janitor", "janitorial", "custodian", "custodial", "housekeeper",
        "housekeeping", "cleaner", "cleaning", "groundskeeper", "landscaper", "landscaping",
        "lawn care", "handyman", "porter", "pest control",
    ],
    "food_production_kitchen": [
        "line cook", "prep cook", "cook", "dishwasher", "kitchen", "food prep", "butcher",
        "meat cutter", "baker",
    ],
    "automotive": [
        "lube tech", "lube technician", "tire tech", "tire technician", "auto technician",
        "mechanic", "car wash", "detailer", "auto body",
    ],
}

# Titles that indicate a role is supervisory, senior, or white-collar.
EXCLUDE_TITLE = [
    "senior", "sr", "manager", "director", "supervisor", "superintendent", "lead", "principal",
    "engineer", "architect", "analyst", "estimator", "foreman", "head of", "vp", "president",
    "coordinator", "planner", "recruiter", "sales", "account executive", "iii", "iv",
]

ENTRY_SIGNALS = [
    "entry level", "entry-level", "no experience", "will train", "paid training",
    "on-the-job training", "on the job training", "trainee", "apprentice", "helper",
    "no degree", "high school diploma", "ged", "immediate start", "start immediately",
    "hiring immediately", "weekly pay", "daily pay", "same day pay",
]


def _compile(words):
    return re.compile(r"\b(?:" + "|".join(re.escape(w) for w in words) + r")\b", re.IGNORECASE)


_CATEGORY_RES = {cat: _compile(words) for cat, words in CATEGORIES.items()}
_EXCLUDE_RE = _compile(EXCLUDE_TITLE)
_ENTRY_RE = _compile(ENTRY_SIGNALS)
_YEARS_RE = re.compile(r"\b(\d{1,2})\s*\+?\s*(?:-\s*\d+\s*)?years?\b[^.]{0,40}\bexperience", re.IGNORECASE)


def categorize(title: str) -> str | None:
    for cat, rx in _CATEGORY_RES.items():
        if rx.search(title):
            return cat
    return None


def classify(job: Job) -> Job:
    """Set category, entry_level_score and tags on the job (in place) and return it.

    A score of 0 means "not an entry-level blue-collar job".
    """
    title = job.title or ""
    job.category = categorize(title)
    if job.category is None or _EXCLUDE_RE.search(title):
        job.entry_level_score = 0.0
        return job

    text = f"{title}\n{job.description or ''}"
    signals = sorted({m.group(0).lower() for m in _ENTRY_RE.finditer(text)})
    score = 0.6 + 0.1 * min(len(signals), 4)

    years = [int(m.group(1)) for m in _YEARS_RE.finditer(job.description or "")]
    if years:
        required = min(years)
        if required >= 3:
            score -= 0.4
        elif required >= 2:
            score -= 0.2

    if job.salary_period == "hour" and job.salary_min:
        job.tags.append("hourly")
    job.tags.extend(f"signal:{s}" for s in signals)
    job.entry_level_score = round(max(0.0, min(score, 1.0)), 2)
    return job

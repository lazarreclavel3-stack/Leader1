from .adzuna import Adzuna
from .ats import Greenhouse, Lever
from .careeronestop import CareerOneStop
from .jooble import Jooble
from .usajobs import USAJobs

ALL_SOURCES = {s.name: s for s in (USAJobs(), Adzuna(), Jooble(), CareerOneStop(), Greenhouse(), Lever())}

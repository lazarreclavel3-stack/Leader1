import unittest

from jobfeed.classify import classify
from jobfeed.models import Job, SearchQuery
from jobfeed.pipeline import collect, dedupe
from jobfeed.sources import adzuna, ats, careeronestop, jooble, usajobs
from jobfeed.sources.base import Source


def job(title, description="", **kw):
    return Job(source="t", source_id=title, title=title, url=kw.pop("url", ""), description=description, **kw)


class ClassifyTest(unittest.TestCase):
    def test_entry_level_blue_collar_is_kept(self):
        j = classify(job("Warehouse Associate", "No experience needed, paid training. Weekly pay."))
        self.assertEqual(j.category, "warehouse_logistics")
        self.assertGreaterEqual(j.entry_level_score, 0.9)
        self.assertIn("signal:paid training", j.tags)

    def test_senior_and_white_collar_titles_are_dropped(self):
        for title in ("Warehouse Manager", "Sr. Welder", "Maintenance Supervisor",
                      "Software Engineer", "Plumber III", "Construction Estimator"):
            self.assertEqual(classify(job(title)).entry_level_score, 0, title)

    def test_experience_requirement_lowers_score(self):
        j = classify(job("CNC Machine Operator", "Requires 5+ years of machining experience."))
        self.assertLess(j.entry_level_score, 0.5)

    def test_unrelated_title_has_no_category(self):
        self.assertIsNone(classify(job("Marketing Associate")).category)


class ParserTest(unittest.TestCase):
    def test_usajobs(self):
        payload = {"SearchResult": {"SearchResultItems": [{
            "MatchedObjectId": "123",
            "MatchedObjectDescriptor": {
                "PositionTitle": "Laborer", "PositionURI": "https://usajobs.gov/job/123",
                "OrganizationName": "Army", "PositionLocationDisplay": "Fort Hood, Texas",
                "PublicationStartDate": "2026-10-01",
                "PositionRemuneration": [{"MinimumRange": "18.50", "MaximumRange": "21.00",
                                          "RateIntervalCode": "PH"}],
                "PositionSchedule": [{"Name": "Full-time"}],
                "UserArea": {"Details": {"JobSummary": "<p>Moves supplies.</p>"}},
            }}]}}
        [j] = usajobs.parse(payload)
        self.assertEqual((j.id, j.salary_min, j.salary_period), ("usajobs:123", 18.5, "hour"))
        self.assertEqual(j.description, "Moves supplies.")

    def test_adzuna(self):
        [j] = adzuna.parse({"results": [{
            "id": 9, "title": "<strong>Forklift</strong> Operator", "redirect_url": "https://a/9",
            "company": {"display_name": "Acme"}, "location": {"display_name": "Dallas, TX"},
            "salary_min": 38000, "salary_max": 42000, "salary_is_predicted": "1",
            "created": "2026-10-02T00:00:00Z", "contract_time": "full_time"}]})
        self.assertEqual((j.title, j.company, j.salary_period), ("Forklift Operator", "Acme", "year"))
        self.assertIn("salary_predicted", j.tags)

    def test_jooble_salary(self):
        self.assertEqual(jooble.parse_salary("$18 - $22 per hour"), (18, 22, "hour"))
        self.assertEqual(jooble.parse_salary("$45k - $50k"), (45000, 50000, "year"))
        self.assertEqual(jooble.parse_salary(""), (None, None, None))
        [j] = jooble.parse({"jobs": [{"id": 1, "title": "Dishwasher", "link": "https://j/1",
                                      "salary": "$15/hr", "company": "Diner"}]})
        self.assertEqual((j.salary_min, j.salary_period), (15, "hour"))

    def test_careeronestop(self):
        [j] = careeronestop.parse({"Jobs": [{"JvId": "AB1", "JobTitle": "Janitor", "Company": "City",
                                             "URL": "https://c/1", "Location": "Austin, TX",
                                             "DatePosted": "10/3/2026"}]})
        self.assertEqual((j.id, j.location), ("careeronestop:AB1", "Austin, TX"))

    def test_greenhouse_and_lever(self):
        [g] = ats.parse_greenhouse({"jobs": [{"id": 5, "title": "Picker", "absolute_url": "https://g/5",
                                              "location": {"name": "Reno, NV"},
                                              "content": "&lt;p&gt;Pick orders&lt;/p&gt;"}]}, "acme")
        self.assertEqual((g.id, g.company, g.description), ("greenhouse:acme:5", "acme", "Pick orders"))
        [lv] = ats.parse_lever([{"id": "x", "text": "Delivery Driver", "hostedUrl": "https://l/x",
                                 "createdAt": 1759276800000, "categories": {"location": "Ohio"},
                                 "salaryRange": {"min": 20, "max": 24, "interval": "per-hour-wage"}}],
                               "acme")
        self.assertEqual((lv.salary_period, lv.posted_at[:10]), ("hour", "2025-10-01"))


class PipelineTest(unittest.TestCase):
    def test_dedupe_merges_cross_source_copies(self):
        a = job("Warehouse Associate", company="Acme", location="Dallas, TX", url="https://a")
        b = job("Warehouse  associate", company="ACME", location="Dallas TX", url="https://b",
                salary_min=18.0, salary_period="hour")
        c = job("Forklift Operator", company="Acme", url="https://a")  # same URL as a
        [merged] = dedupe([a, b, c])
        self.assertEqual((merged.url, merged.salary_min), ("https://a", 18.0))

    def test_collect_filters_and_survives_broken_source(self):
        class Fake(Source):
            name = "fake"
            def fetch(self, query):
                yield job("General Laborer", "Will train", posted_at="2026-10-02")
                yield job("Accountant")

        class Broken(Source):
            name = "broken"
            def fetch(self, query):
                raise RuntimeError("boom")

        jobs = collect([Broken(), Fake()], SearchQuery(keywords=["x"]))
        self.assertEqual([j.title for j in jobs], ["General Laborer"])


if __name__ == "__main__":
    unittest.main()

# Daily executive job search — runbook

Run every morning. Goal: email Clavel 7–10 well-matched roles paying **$180K+**, each with a
resume tailored to that posting, built in the approved format.

## 0. Setup (each run)
- `git fetch origin claude/admiring-bardeen-62rshk && git checkout claude/admiring-bardeen-62rshk && git pull`
- Work in `jobsearch/`. Today's outputs go in `jobsearch/runs/YYYY-MM-DD/`.
- Read `career_database.xlsx` sheets: *Career Evidence*, *Role Families*, *Search Rules*,
  *Search Profile*, *Conflict Review*. These are the source of truth.
- Read `history.csv` (date, org, title, url) and never resend a job already listed there.

## 1. Find roles
- **Role families** (from the database, all High priority unless noted): Finance Executive (CFO, VP Finance,
  Deputy CFO), Finance + Operations (CFO/COO, Chief Business Officer, VP Finance & Ops, CAO),
  Operations Executive (COO, SVP/VP Ops), Strategy/Growth, Business Development (CDO, Chief Growth Officer),
  Workforce Executive, Programs/Social Impact, Executive Director (medium-high), Public Sector/Contracts
  (medium-high), Financial Services (medium). Lead with CFO and finance-plus-operations roles, but surface
  any lane that scores well. Match the work, not just the title.
- **Pay floor: $180,000/yr.** Include a role only if the posted range reaches $180K+, or no salary is
  posted but the level and organization size make $180K+ realistic (mark it "Salary not posted, est.").
- **Location (Clavel, 2026-10-27): DC (incl. close-in DC metro, flagged), New York City (5 boroughs only), and Connecticut.**
  Fully remote US roles are still fine (workable from NYC). No Long Island, Westchester, NJ, or relocation roles.
- **Sources:** avoid the mass job boards (LinkedIn, Indeed, ZipRecruiter, Glassdoor, Monster,
  CareerBuilder, SimplyHired, Google Jobs). Prefer executive-search firm postings (Koya Partners,
  Isaacson Miller, Diversified Search, Phillips Oppenheim, On Ramps, Moss Kanter, Campbell & Co.,
  Morris & Berger, Bridge Partners, NPAG, Marcum Search, Kittleman, fractional-CFO firms),
  organizations' own career pages, and niche boards (Idealist, Chronicle of Philanthropy, PND,
  Nonprofit HR, NY Nonprofit Media, Human Services Council, FEI, AFP/HFMA, Built In NYC,
  Wellfound, Bridgespan).
- Fetch each posting and confirm it is live. Never invent links, salaries, or application addresses.
- **Score** each role 0–100 using the *Search Rules* weights (capability 38%, achievement/scope 24%,
  leadership 12%, industry 10%, title 8%, practical constraints incl. salary/location/credentials 8%).
  Drop roles below 72. Mark 82+ as Strong and 90+ as Priority. If fewer than 7 qualify, send fewer and say so.

## 2. Tailor a resume per role
- Copy `base_cfo.json` (or start from it for non-CFO lanes) to `runs/<date>/<NN>_<org>.json`.
- Rewrite the tagline, profile, stats, capabilities, and bullet order/wording to mirror the posting's
  language and priorities. Pull extra bullets from *Career Evidence* where relevant.
- **Evidence rule:** every bullet must cite evidence IDs; the builder rejects bullets that don't.
  Do not use metrics flagged on *Conflict Review* unless that row is marked confirmed (e.g. no $3.5M/$350K
  capital-raise figure, no Haiti child counts, no Fitness location counts or timing, no $62.5M pipeline).
  Never claim credentials Clavel doesn't hold (no CPA).
- Keep it to 2 pages. Build: `python3 build_resume.py runs/<date>/<file>.json runs/<date>/Clavel_Lazarre_<Org>_<Title>.docx --pdf`
- Spot-check at least one rendered PDF (`pdftoppm -jpeg -r 70`).
- Never use gendered pronouns for Clavel in any generated text.
- Put each evidence bullet under its real employer from the *Career Evidence* Organization column. Earlier
  financial-services evidence (E028–E031: PFP Financial, American Express consulting, First Providence) goes
  in its own "EARLIER FINANCIAL SERVICES EXPERIENCE" section, never under Monark (see runs/2026-10-21/make_specs.py).
- Pattern that works: a small per-day script that copies base_cfo.json and, per job, sets the tagline,
  profile and capability list, reorders bullets by the evidence IDs the posting cares about most, and adds
  relevant extra evidence bullets (max 6 per role). See `runs/2026-10-19/make_specs.py`.

## 3. Deliver
- Email **lazarreclavel3@gmail.com** (Gmail `send_message`), subject `Executive Job Picks — <Weekday, Mon D>`,
  HTML body: for each job J1..Jn give title, organization, location, salary, source, **direct link**,
  how to apply, score/rating, 2–3 sentences on why it fits, gaps, and the matching resume file name.
  Gmail attachments need inline base64, so do NOT attach resumes to the digest. Instead, commit and push
  `runs/<date>/` (specs, .docx, .pdf) FIRST, then link each resume in the email as
  `https://github.com/lazarreclavel3-stack/Leader1/raw/claude/admiring-bardeen-62rshk/jobsearch/runs/<date>/<file>.docx`
  (and the .pdf the same way). Clavel is fine with the repo being public.
- Also deliver the .docx resumes with SendUserFile (status `proactive`, display `attach`).
  End with: "Reply APPLY J2, J5 and I'll draft cover letters and application emails on the next run."
- If Gmail is unavailable: post the same list (with links) in the session and send the resumes
  with SendUserFile (status `proactive`).
- Append each sent job to `history.csv`; commit and push it with the day's `runs/<date>/` folder.

## 3b. Thin days
- If no new role qualifies, still email: say so plainly, then list the best still-open earlier picks
  (re-check each posting is live) with their resume links. Never pad with weak roles.
- If Clavel replies "WIDEN", from then on also include hybrid roles outside NYC and very strong roles
  topping out slightly under $180K, flagged as such. Record that choice here.
- **WIDEN is ON (Clavel replied 2026-10-26), narrowed 2026-10-27:** locations limited to DC, NYC (5 boroughs), CT,
  or remote. Strong roles whose range tops out at or near $180K are OK. Label each.
- Applied (per Clavel, 2026-10-26): Lantern Community Services, The Clean Slate Initiative. Don't re-pitch.

## 4. Approvals
- Check Gmail for replies from lazarreclavel3@gmail.com in "Executive Job Picks" threads (last 14 days)
  containing "APPLY" without a later "Processed" reply from us.
- For each approved job, write a tailored cover letter (truthful, one page). If the posting lists an
  application email, create a Gmail **draft** to it (attach the tailored resume as base64 only for that one file). **Never send to
  employers.** For portal applications, reply with the link and cover letter.
- Reply in the thread starting with "Processed" and list what was prepared for each job.

## 5. Master list upkeep
- `career_database.xlsx` is the single source for every resume. Whenever Clavel shares a new fact, skill, metric,
  title, or preference (in chat or email), add it the same day: new rows in *Career Evidence* (Status
  "Stated by Clavel, <month year>"), new or resolved rows in *Conflict Review*, and updates to *Profile & Preferences*.
- Pull facts for tailored resumes from this file first; Clavel fact-checks figures, so don't block on conflicts
  Clavel has already chosen (see the Status column).

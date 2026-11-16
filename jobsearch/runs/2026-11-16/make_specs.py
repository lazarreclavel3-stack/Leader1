"""Generate today's tailored resume specs from base_cfo.json."""
import copy, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
base = json.load(open(os.path.join(HERE, '..', '..', 'base_cfo.json')))

EXTRA = {
    'E046': ('ALLUEL LOGISTICS', 'Streamlined operations and eliminated redundancies across personnel, facilities, systems, and sales.'),
    'E007': ('MAROON STRATEGIST LLC', 'Structured the financial framework for a NYPA Clean Energy Workforce Program, aligning public funding, compliance, and performance metrics.'),
    'E019': ('MAROON STRATEGIST LLC', 'Designed and executed workforce and employment initiatives focused on equitable career pathways.'),
    'E029': ('PFP FINANCIAL · AMERICAN EXPRESS (CONSULTING) · FIRST PROVIDENCE FINANCIAL GROUP', 'Produced $23M in benefits coverage and reached 2,100+ credit-union members through consultative sales and member acquisition.'),
    'E030': ('PFP FINANCIAL · AMERICAN EXPRESS (CONSULTING) · FIRST PROVIDENCE FINANCIAL GROUP', 'Structured debt and equity financing options and advised SMEs ($1M–$50M revenue) on lines of credit, debt consolidation, private placements, and acquisitions.'),
    'E031': ('PFP FINANCIAL · AMERICAN EXPRESS (CONSULTING) · FIRST PROVIDENCE FINANCIAL GROUP', 'Managed affluent-client relationships across wealth management, private banking, and investment advisory (former Series 7 and 63).'),
    'E022': ('MAROON STRATEGIST LLC', 'Worked with NYSID on public-sector projects employing individuals with disabilities.'),
    'E023': ('MAROON STRATEGIST LLC', 'Established outcomes tracking and performance reporting against funder benchmarks for enrollments, completions, placements, and retention.'),
    'E055': ('MAROON STRATEGIST LLC', 'Build KPI dashboards, forecasts, and outcome measures that leaders use to make decisions.'),
    'E024': ('THE OSBORNE ASSOCIATION', 'Owned an agency-wide employment model integrating job readiness, placement, and wraparound supports for justice-impacted participants.'),
    'E002': ('MAROON STRATEGIST LLC', 'Provide hands-on leadership in multi-entity finance, public funding, capital strategy, and audit remediation.'),
    'E036': ('FITNESS COLLECTIVE INC', None),
    'E038': ('ALLUEL LOGISTICS', 'Selected, implemented, and trained teams on CRM and business systems, including Salesforce, Zoho, Looker, SQL, and ERP platforms.'),
    'E039': ('THE OSBORNE ASSOCIATION', 'Built and managed relationships with government, philanthropic, corporate, and community partners, including the City of New York, to generate contracts and programs.'),
    'E040': ('THE OSBORNE ASSOCIATION', 'Represented the organization publicly at panels, stakeholder forums, and NYC Climate Week.'),
    'E056': ('THE OSBORNE ASSOCIATION', 'Coached and developed managers and staff, building training and talent-development practices across the division.'),
    'E053': ('MAROON STRATEGIST LLC', 'Developed education, entrepreneurship, and financial-literacy program strategies, including monetization approaches.'),
}

EXTRA.update({
    'E072': ('MAROON STRATEGIST LLC', 'Created and launched an 18-month NYPA clean-energy workforce program from inception; piloted the model before full rollout; 92% of enrolled participants completed training and earned a certificate.'),
    'E067': ('MAROON STRATEGIST LLC', 'Serve as fractional CFO for a physician practice in an IPA, managing IPA-related finances and billing to Medicaid managed care and commercial plans.'),
    'E055': ('MAROON STRATEGIST LLC', 'Build KPI dashboards, forecasts, and outcome measures that leaders use to set targets, track growth, and adjust programs.'),
    'E080': ('MAROON STRATEGIST LLC', 'Built and piloted SkyNet, an AI-supported workflow for research, evaluation, and engagement tracking, now in full daily use.'),
    'E043': ('THE OSBORNE ASSOCIATION', 'Led revenue-generating social ventures and employment programs, combining financial sustainability with measurable mission outcomes.'),
    'E058': ('THE OSBORNE ASSOCIATION', 'Led 12 direct reports across finance, grant stewardship, and operations through weekly team meetings, individual check-ins, and recurring performance reviews.'),
    'E065': ('THE OSBORNE ASSOCIATION', 'Partnered with the CEO and Board, including the Finance and Audit Committees, on planning, risk, resource allocation, and growth.'),
    'E076': ('FITNESS COLLECTIVE INC', 'Scaled the workforce from 4 to 60 full-time employees across accounting, IT, facilities, training, and group fitness; created roles and ran all staffing.'),
})
JOBS = [
 dict(slug='01_UpstreamUSA', tagline='CHIEF OPERATING OFFICER  ·  PROGRAM LAUNCH & SCALE  ·  GROWTH & PARTNERSHIPS  ·  PERFORMANCE MEASUREMENT  ·  FINANCE',
  profile='Operator and builder who owns programs end to end: launching new models, scaling what works, measuring impact, and adjusting quickly when the data says to. Held full P&L accountability for an $80M portfolio and led a 140-person, multi-program division, reversing a $1M operating deficit into a 13% surplus while negotiating $10M+ in new government, institutional, and corporate contracts. Launched a clean-energy workforce program from inception, piloting the model before rollout and reaching 92% certificate completion. Brings healthcare finance depth as fractional CFO to a physician practice in an IPA, managing billing to Medicaid managed care and commercial plans. Builds KPI dashboards and outcome measures that set clear targets for growth and impact; partners with CEOs and Boards on strategy, finances, and risk; scaled a multi-location business from 4 to 60 employees.',
  lead=['E072','E067','E055','E003','E080','E010','E012','E013','E043','E058','E065','E016','E015','E014','E017','E050','E076','E033','E036'],
  extra=['E072','E067','E055','E080','E043','E058','E065','E076'],
  caps=['Program Ownership: Launch, Scale, Adapt','Growth Strategy & Business Development','Performance Measurement & KPIs','Healthcare & Medicaid Managed Care Finance','Operating Budgets & Financial Management','Partner & Stakeholder Relationships','Board Materials & Governance','Organizational Design & Team Leadership','Change Management in Fast-Moving Settings','Data-Driven Decision Making','AI-Enabled Workflows','Culture & Accountability']),
]

def ev(b): return set(b['evidence'])
for j in JOBS:
    s = copy.deepcopy(base)
    s['tagline'], s['profile'], s['capabilities'] = j['tagline'], j['profile'], j['caps']
    lead = j['lead']
    if any(e in ('E029','E030','E031') for e in j.get('extra', [])):
        s['sections'].append({'heading': 'EARLIER FINANCIAL SERVICES EXPERIENCE', 'jobs': [{
            'org': 'PFP FINANCIAL · AMERICAN EXPRESS (CONSULTING) · FIRST PROVIDENCE FINANCIAL GROUP',
            'title': 'Sales Management Consultant; Senior Small Business Analyst; Financial Services Representative',
            'dates': '', 'location': 'New York, NY', 'bullets': []}]})
    for e in j.get('extra', []):
        org, text = EXTRA[e]
        if not text: continue
        for sec in s['sections']:
            for jb in sec['jobs']:
                if jb['org'] == org and not any(e in b['evidence'] for b in jb['bullets']):
                    jb['bullets'].append({'text': text, 'evidence': [e]})
    rank = lambda b: min([lead.index(x) for x in b['evidence'] if x in lead] or [99])
    for sec in s['sections']:
        for jb in sec['jobs']:
            jb['bullets'].sort(key=rank)
            jb['bullets'] = jb['bullets'][:6]
    s.pop('_note', None)
    json.dump(s, open(os.path.join(HERE, j['slug'] + '.json'), 'w'), indent=1, ensure_ascii=False)
    print(j['slug'])

# COO-lane tweak: Maroon title per C015 (own-firm titles may be tailored)
for j in JOBS:
    f = os.path.join(HERE, j['slug'] + '.json'); s = json.load(open(f))
    for sec in s['sections']:
        for jb in sec['jobs']:
            if jb['org'] == 'MAROON STRATEGIST LLC': jb['title'] = 'Fractional CFO & Operations Consultant'
    json.dump(s, open(f, 'w'), indent=1, ensure_ascii=False)

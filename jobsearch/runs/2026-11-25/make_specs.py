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
    'E055': ('MAROON STRATEGIST LLC', 'Design KPI dashboards, forecasts, and pipeline and performance reporting that leaders use to spot bottlenecks and act.'),
    'E062': ('THE OSBORNE ASSOCIATION', 'Modernized payment processes, redesigned workflows, and introduced compliance meetings and staff self-assessments as part of the deficit-to-surplus turnaround.'),
    'E058': ('THE OSBORNE ASSOCIATION', 'Led 12 direct reports across finance, operations, and frontline supervision through weekly operating reviews and clear performance standards.'),
    'E080': ('MAROON STRATEGIST LLC', 'Built and piloted SkyNet, an AI-supported workflow for research, document preparation, and engagement tracking, now in full daily use.'),
})
JOBS = [
 dict(slug='01_WorldBusinessLenders', tagline='CHIEF OPERATING OFFICER  ·  END-TO-END PROCESS INTEGRATION  ·  KPIs & SERVICE LEVELS  ·  SMALL-BUSINESS LENDING  ·  CONTROLS',
  profile='Operations executive who integrates fragmented functions into one accountable, end-to-end operating model, with a background in small-business lending and capital. Advised small and mid-sized businesses ($1M–$50M revenue) on lines of credit, debt consolidation, private placements, and acquisitions, served as financial architect for a $200M national banking-development initiative, and directed billing, controls, and compliance for NYCHA and NYC Department of Homeless Services contracts. Held full P&L accountability for an $80M portfolio and a 140-person division, reversing a $1M deficit into a 13% surplus through workflow redesign, controls, and cost discipline. Implemented an ERP-based system that cut processing time 60%. Builds SOPs, service levels, escalation paths, KPI dashboards, and AI-enabled workflows for remote, cross-functional teams.',
  lead=['E010','E062','E012','E058','E013','E003','E055','E080','E004','E005','E015','E016','E014','E017','E050','E051','E033','E036','E030','E031','E029'],
  extra=['E062','E058','E055','E080','E030','E031'],
  caps=['End-to-End Process Integration','SOPs, Service Levels & Escalation','KPI Dashboards & Pipeline Reporting','Small-Business Lending & Credit Advisory','Operational Controls & Compliance','Cross-Functional Coordination','Capacity Planning & Bottleneck Removal','Workflow Automation, ERP & AI','Turnaround & Cost Discipline','Remote Team Leadership','CEO Partnership & Reporting','Scalable Operating Models']),
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

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
    'E066': ('THE OSBORNE ASSOCIATION', 'Oversaw IT systems, facilities, and vendor contracts supporting multi-site program operations.'),
    'E062': ('THE OSBORNE ASSOCIATION', 'Modernized payment processes, redesigned workflows, and introduced compliance meetings and staff self-assessments as part of the deficit-to-surplus turnaround.'),
    'E058': ('THE OSBORNE ASSOCIATION', 'Led 12 direct reports across finance, operations, and frontline supervision through weekly operating reviews, individual check-ins, and clear performance expectations.'),
    'E059': ('THE OSBORNE ASSOCIATION', 'Ran staffing capacity for all 140 employees, managing staff hours, overtime, bonuses, and raises against budget.'),
    'E088': ('FITNESS COLLECTIVE INC', 'Managed landlord relationships, leases, facilities, insurance, utilities, and vendor contracts across multiple locations.'),
    'E090': ('FITNESS COLLECTIVE INC', 'Wrote safety plans and procedures for the company and its five locations, including franchise sites.'),
    'E076': ('FITNESS COLLECTIVE INC', 'Scaled the workforce from 4 to 60 full-time employees across accounting, IT, facilities, training, and group fitness; created roles and ran all staffing and scheduling.'),
    'E053': ('MAROON STRATEGIST LLC', 'Developed education, entrepreneurship, and financial-literacy program strategies for mission-driven organizations.'),
    'E072': ('MAROON STRATEGIST LLC', 'Created and led an 18-month NYPA clean-energy workforce training program from inception; piloted the model before rollout; 92% of enrolled participants completed training and earned a certificate.'),
})
JOBS = [
 dict(slug='01_AchievementFirst', tagline='CHIEF OPERATING OFFICER  ·  MULTI-SITE OPERATIONS  ·  FACILITIES & REAL ESTATE  ·  TECHNOLOGY & DATA  ·  VENDOR & RISK MANAGEMENT',
  profile='Operations executive who builds the standards, systems, and accountability that make multi-site, mission-driven organizations run reliably every day. Led a 140-person, multi-program, multi-site division with full P&L accountability for an $80M portfolio, overseeing IT systems, facilities, and vendor contracts while reversing a $1M operating deficit into a 13% surplus through workflow redesign, controls, and cost restructuring. Built and ran five locations from the ground up, including leases and landlord relationships, insurance, safety plans, and staffing that grew from 4 to 60 employees. Implemented ERP systems that cut processing time 60% and renegotiated vendor agreements to reduce costs 35%. Designs operating cadences, KPIs, and playbooks; develops leaders through clear expectations; and partners with CEOs and Boards on planning, risk, and resource allocation. Brings education and workforce-training program experience.',
  lead=['E010','E066','E012','E062','E058','E059','E013','E027','E003','E072','E053','E004','E055','E015','E014','E016','E088','E090','E076','E033','E036','E017','E050'],
  extra=['E066','E062','E058','E059','E072','E053','E088','E090','E076'],
  caps=['Multi-Site Operations Leadership','Operational Standards, Playbooks & KPIs','Facilities, Leases & Capital Planning','Technology, Data & Systems Implementation','Vendor & Service-Provider Management','Operational Risk, Safety & Insurance','Budgets & Financial Performance','Leadership Development & Accountability','Change Management & Turnaround','Board & CEO Partnership','Education & Workforce Programs','Cross-Functional Execution']),
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

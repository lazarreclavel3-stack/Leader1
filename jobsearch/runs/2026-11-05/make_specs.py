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
    'E089': ('ALLUEL LOGISTICS', 'Created and administered employee retirement plans, including at Alluel Logistics and for Maroon Strategist clients.'),
    'E088': ('FITNESS COLLECTIVE INC', 'Managed landlord relationships, leases, facilities, insurance, utilities, and vendor contracts across multiple locations.'),
    'E090': ('FITNESS COLLECTIVE INC', 'Wrote safety plans and procedures for the company and its five locations, including franchise sites.'),
    'E076': ('FITNESS COLLECTIVE INC', 'Scaled the workforce from 4 to 60 full-time employees across accounting, IT, facilities, training, and group fitness; created roles and ran all staffing and scheduling.'),
    'E066': ('THE OSBORNE ASSOCIATION', 'Oversaw IT systems, facilities, and vendor contracts supporting multi-site program operations.'),
    'E065': ('THE OSBORNE ASSOCIATION', 'Partnered with the CEO and Board, including the Finance and Audit Committees, on planning, risk, resource allocation, and sustainability.'),
    'E059': ('THE OSBORNE ASSOCIATION', 'Ran staffing capacity for all 140 employees, managing staff hours, overtime, bonuses, and raises against budget.'),
    'E060': ('THE OSBORNE ASSOCIATION', 'Built pricing, monetization plans, and budgets for earned-revenue service lines, including landscaping and warehouse cleaning.'),
    'E085': ('THE OSBORNE ASSOCIATION', 'Ran HR for a workforce program overseeing hundreds of workers, including hiring, supervision, and employee relations, applying New York employment law.'),
    'E024': ('THE OSBORNE ASSOCIATION', 'Owned an employment and workforce-development model integrating job readiness, placement, and wraparound supports for justice-impacted participants.'),
    'E072': ('MAROON STRATEGIST LLC', 'Created and led an 18-month NYPA clean-energy workforce program from inception; piloted the model before rollout; 92% of enrolled participants completed training and earned a certificate.'),
    'E022': ('MAROON STRATEGIST LLC', 'Worked with NYSID on public-sector projects employing individuals with disabilities.'),
    'E053': ('MAROON STRATEGIST LLC', 'Developed entrepreneurship, small-business, and financial-literacy program strategies, including service menus and monetization approaches.'),
    'E058': ('THE OSBORNE ASSOCIATION', 'Led 12 direct reports across finance, grant stewardship, and operations through weekly team meetings, individual check-ins, and recurring financial reviews.'),
})
JOBS = [
 dict(slug='01_WHEDco', tagline='CHIEF OPERATING OFFICER  ·  STRATEGIC PLANNING  ·  BUDGETS & FINANCIAL MODELING  ·  REAL ESTATE & FACILITIES  ·  BOARD GOVERNANCE',
  profile='Operations and finance executive who builds the systems, teams, and financial discipline that let community-development and human-services organizations deepen their impact. Partners with presidents, CFOs, and Boards on multi-year strategic plans, annual operating and capital budgets, risk management, and compliance reporting. Brings hands-on depth in financial modeling, facilities and lease management, insurance, IT systems, and retirement-plan administration, plus direct experience with NYCHA and NYC Department of Homeless Services contracts. Held full P&L accountability for an $80M portfolio and led a 140-person division, reversing a $1M operating deficit into a 13% surplus. Built and ran earned-revenue social ventures and small-business programs, and scaled a multi-location business from 4 to 60 employees. Develops leaders through clear expectations, coaching, and accountability.',
  lead=['E010','E012','E027','E065','E066','E058','E013','E042','E003','E004','E009','E053','E072','E016','E089','E014','E015','E088','E076','E090','E033','E017','E050'],
  extra=['E066','E058','E053','E089','E088','E076'],
  caps=['Strategic Planning & Execution','Operating & Capital Budgets','Financial Modeling & Analysis','Real Estate & Facilities Oversight','Leases, Insurance & Risk Management','Compliance & Regulatory Reporting','Board & Committee Engagement','IT & Organizational Systems','Retirement Plan Administration','NYCHA & NYC Agency Contracts','Small-Business & Earned-Revenue Programs','Capacity Building & Talent Development']),
 dict(slug='02_Fedcap', tagline='CHIEF OPERATING OFFICER  ·  WORKFORCE DEVELOPMENT  ·  FACILITIES SERVICES  ·  GOVERNMENT CONTRACTS & COMPLIANCE  ·  GROWTH',
  profile='Operations executive who scales workforce-development and service organizations while holding them to contractual, regulatory, and financial goals. Led a 140-person, multi-program division with full P&L accountability for an $80M portfolio, running employment programs and earned-revenue service lines, including facility services, landscaping, warehouse cleaning, and power washing, that employed people returning from incarceration. Reversed a $1M operating deficit into a 13% surplus, negotiated $10M+ in government and institutional contracts, and directed controls, billing, and compliance for NYCHA and NYC Department of Homeless Services contracts. Built a clean-energy workforce program from inception with 92% certificate completion and partnered with NYSID on projects employing people with disabilities. Develops high-performing leadership teams through KPIs, coaching, and a steady management cadence.',
  lead=['E010','E012','E042','E060','E024','E059','E085','E013','E066','E027','E072','E022','E003','E004','E016','E014','E015','E088','E090','E076','E033','E017','E050'],
  extra=['E060','E024','E059','E085','E066','E072','E022','E088','E090','E076'],
  caps=['Multi-Site Operations Leadership','Facilities & Building Services','Workforce Development & Vocational Programs','Government Contracts & Compliance','Quality Assurance & Risk Management','KPI Dashboards & Performance Management','Operating Budgets & Financial Performance','Pricing & Earned-Revenue Growth','Strategic Partnerships','Safety Plans & Procedures','HR & Workforce Planning','Leadership Team Development']),
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

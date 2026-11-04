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
    'E068': ('MAROON STRATEGIST LLC', 'Oversee payroll, AP, AR, vendor payments, invoicing, bank reconciliations, and monthly, quarterly, and annual financial statements for boards and funders.'),
    'E069': ('MAROON STRATEGIST LLC', 'Compile Form 990 returns for multiple nonprofits and prepare business and individual tax filings, including state and local returns; IRS-registered preparer with an active PTIN.'),
    'E070': ('MAROON STRATEGIST LLC', 'Lead annual audit coordination and readiness testing for workforce development, healthcare, and smaller 501(c)(3) organizations.'),
    'E061': ('THE OSBORNE ASSOCIATION', 'Managed multiple program budgets with monthly reconciliation and quarterly performance tracking; monitored restricted and unrestricted cash flow.'),
    'E058': ('THE OSBORNE ASSOCIATION', 'Led 12 direct reports across finance, grant stewardship, and operations through weekly team meetings, individual check-ins, and recurring financial reviews.'),
})
JOBS = [
 dict(slug='01_Borealis', tagline='NONPROFIT FINANCE  ·  BUDGETING & FORECASTING  ·  AUDIT & FORM 990  ·  RESTRICTED FUNDS  ·  FINANCE TEAM LEADERSHIP',
  profile='Nonprofit finance executive who builds the systems, controls, and teams that let mission-driven organizations move resources with confidence. Leads annual operating and program budgets, multi-year forecasting, treasury, and reserves strategy; directs audit coordination and readiness; and compiles Form 990 returns for multiple nonprofits as an IRS-registered preparer with an active PTIN. Manages grant and restricted-fund accounting with monthly reconciliation and funder reporting, and partners with CEOs, Boards, and Finance and Audit Committees on planning, risk, and resource allocation. Reversed a $1M operating deficit into a 13% surplus and recovered $1.5M+ in tax savings. Leads and develops finance teams, including 12 direct reports across finance, grant stewardship, and operations, with a commitment to equity-centered, community-accountable organizations.',
  lead=['E003','E068','E069','E070','E004','E008','E005','E061','E010','E012','E027','E058','E013','E016','E015','E014','E017'],
  extra=['E068','E069','E070','E061','E058'],
  caps=['Annual & Multi-Year Budgeting','Forecasting & Cash Management','Reserves & Investment Oversight','Audit Coordination & Readiness','Form 990 Preparation (Active PTIN)','Grants & Restricted-Fund Accounting','Fund Accounting & Internal Controls','GAAP & Uniform Guidance Compliance','Board & Finance Committee Partnership','Payroll, AP & AR Oversight','Financial Systems & ERP','KPI Dashboards & Reporting','Risk Management','Finance Team Leadership']),
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

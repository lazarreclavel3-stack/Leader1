"""Generate today's tailored resume specs from base_cfo.json."""
import copy, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
base = json.load(open(os.path.join(HERE, '..', '..', 'base_cfo.json')))

EXTRA = {
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

JOBS = [
 dict(slug='01_WES', tagline='STRATEGIC FINANCE & INVESTMENTS  ·  MULTI-ENTITY FP&A  ·  RISK & AUDIT  ·  ECONOMIC INCLUSION',
  profile='Finance executive for mission-driven social enterprises, with hands-on leadership in multi-entity finance, capital strategy, and economic-mobility work. Leads financial strategy, long-range forecasting, budgeting, treasury, and liquidity across multi-entity structures; directs audit readiness, internal controls, and compliance under GAAP and Uniform Guidance; and supports investment and capital decisions through scenario modeling. Served as financial architect for a $200M national banking-development initiative and structured SME debt, equity, and private-placement financing earlier in a financial-services career (former Series 7 and 63). At a $50M+ nonprofit, held P&L accountability for workforce and social-enterprise programs serving immigrant and justice-impacted New Yorkers, reversing a $1M deficit into a 13% surplus. Partners with CEOs and Boards on growth and risk.',
  lead=['E002','E003','E006','E017','E009','E004','E012','E043','E019','E027'], extra=['E002','E030','E031','E019'],
  caps=['Financial & Investment Strategy','Long-Range Forecasting & Budgeting','Multi-Entity & Cross-Border Finance','Accounting, FP&A & Procurement Oversight','Investment Portfolios & Capital Strategy','Structured & Impact Finance','Grants Management','Financial & Compliance Risk','Audit Committee Liaison','Board & CEO Advisory','Finance & Investment Team Leadership','Immigrant Economic Inclusion & Workforce']),
 dict(slug='02_BAM', tagline='STRATEGIC FINANCE  ·  FP&A & BOARD REPORTING  ·  MULTI-SITE OPERATIONS  ·  SCALABLE SYSTEMS',
  profile='Finance and operations executive who scales multi-site, people-intensive service businesses. Co-founded and ran a multi-location fitness and wellness company from a $5K investment to a $1M enterprise, building pricing, HR, payroll, and benefits infrastructure for a 50+ person team and delivering 33% YoY revenue growth with an 11% margin improvement. Now leads FP&A, budgeting, cash management, accounting controls, and audit readiness for client organizations, and reports to Boards. Implements Salesforce, ERP, and CRM systems, manages outsourced providers and vendors, and uses data and AI-enabled tools to make finance faster. Reversed a $1M operating deficit into a 13% surplus at a $50M+ nonprofit serving low-income communities.',
  lead=['E003','E033','E034','E036','E004','E038','E015','E014','E012','E027'], extra=['E038','E055'],
  caps=['Finance Strategy & FP&A','Forecasting & Board Reporting','Accounting, GAAP & Controls','External Audit','Cash Management','Multi-Site & Seasonal Operations','Payroll & Benefits Partnership with HR','Vendor & Outsourced Provider Oversight','Salesforce & Financial Systems','Data & AI-Enabled Workflows','Low-Income Community Programs','Finance Team Leadership']),
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

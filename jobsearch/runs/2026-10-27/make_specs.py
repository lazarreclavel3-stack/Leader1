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

JOBS = [
 dict(slug='01_EveryMind', tagline='CHIEF OPERATING LEADERSHIP  ·  FINANCE, IT & OPERATIONS  ·  SCALING INFRASTRUCTURE  ·  BEHAVIORAL HEALTH & HUMAN SERVICES',
  profile='Operations and finance executive who builds the systems, infrastructure, and discipline that fast-growing human-services organizations need. Led finance and operations for a 140-person, multi-program social-services division within a $50M+ nonprofit, reversing a $1M operating deficit into a 13% surplus; directed billing, controls, and compliance for NYC Department of Homeless Services and NYCHA contracts. Leads budgeting, multi-year projections, audit readiness, and Board Finance and Audit Committee reporting; implements ERP, CRM, and dashboard systems (60% processing-efficiency gain); and designs staffing plans, accountability structures, and cross-department collaboration. A hands-on builder who coaches managers and stays close to the work.',
  lead=['E011','E010','E012','E016','E003','E004','E015','E038','E055','E027','E046','E056'], extra=['E038','E055','E046','E056'],
  caps=['Enterprise Operations Leadership','Finance, Accounting & Audit Readiness','IT & Outsourced Technology Oversight','Facilities & Administrative Operations','Risk Management & Compliance','Budgeting & Multi-Year Projections','Performance Measures & Dashboards','Multi-Year Staffing Plans','Board Finance & Audit Committee Liaison','Change Management','Team Coaching & Inclusive Culture','Behavioral Health & Homelessness Services']),
 dict(slug='02_IWPR', tagline='CHIEF FINANCIAL & OPERATING LEADERSHIP  ·  GRANTS & AUDIT  ·  PEOPLE, IT & COMPLIANCE  ·  ECONOMIC EQUITY',
  profile='Combined finance and operations executive for mission-driven research and policy organizations. Advises CEOs and Board Finance Committees on budgeting, forecasting, cash flow, and long-range planning; runs grants accounting, audit, and tax compliance under GAAP and Uniform Guidance; and oversees people, payroll, technology, vendors, and administration. Held P&L accountability for a 140-person division within a $50M+ nonprofit focused on workforce and economic mobility, reversing a $1M operating deficit into a 13% surplus. Implements finance and HR systems, manages consultants and outsourced providers, and leads with a commitment to economic and racial equity. MBA.',
  lead=['E003','E004','E012','E010','E011','E036','E038','E027','E014','E019'], extra=['E036','E038','E019'],
  caps=['CEO & Board Finance Committee Advisory','Budgeting, Grants, Audit & Tax','Payroll & HR / People and Culture','IT & Systems Leadership','Administration & Compliance','Vendor & Consultant Management','Cash Flow & Forecasting','Uniform Guidance & GAAP','Project Leadership','Team Leadership','Policy & Research Organizations','Economic & Gender Equity']),
 dict(slug='03_Opportunity180', tagline='CHIEF FINANCE & OPERATIONS  ·  FEDERAL GRANTS & RESTRICTED FUNDS  ·  FACILITY FINANCE  ·  EDUCATION',
  profile='Finance and operations executive experienced in restricted funds, public grants, and capital structuring for mission-driven organizations. Leads multi-year financial strategy, budgeting, forecasting, reserves, internal controls, and audits; directs Uniform Guidance compliance and fund accounting for government-funded programs; and oversees affiliated-entity finance. Structured capital and financing for a $200M national banking-development initiative and SME debt, equity, and private-placement deals earlier in a financial-services career, giving a strong base for facility financing and lender partnerships. Leads finance, grants, and operations teams; reversed a $1M operating deficit into a 13% surplus at a $50M+ nonprofit; and has designed education and financial-literacy program strategies.',
  lead=['E003','E004','E002','E007','E017','E006','E012','E011','E053','E046'], extra=['E002','E030','E053'],
  caps=['Multi-Year Financial Strategy & Reserves','Budgeting, Forecasting & Internal Controls','Federal Grants & Subgrant Compliance','Restricted Funds & Nonprofit GAAP','Affiliated-Entity Oversight','Facility Financing & Lender Partnerships','Risk, Contracting & Technology','Process Improvement','Finance, Grants & Operations Team Leadership','Workforce & Compensation Planning','Education Sector','Executive Team Partnership']),
 dict(slug='04_BOMA', tagline='FINANCE & ADMINISTRATION LEADERSHIP  ·  BUDGET ACCOUNTABILITY  ·  MULTI-ENTITY REPORTING  ·  SCALABLE PROCESSES',
  profile='Finance and administration executive who builds documented, scalable finance functions for membership and mission-driven organizations. Leads the annual budget process and holds leaders accountable to approved budgets; directs month-end close, cash-flow forecasting, audits, tax and regulatory filings, and internal controls; and reports clearly to executives and Boards. Brings multi-entity financial leadership, ERP implementation (60% efficiency gain), and oversight of payroll, banking, HR, and outsourced providers. Reversed a $1M operating deficit into a 13% surplus and recovered $1.5M+ in tax savings through detailed financial analysis.',
  lead=['E003','E004','E002','E015','E036','E009','E012','E008','E027','E046'], extra=['E002','E046'],
  caps=['Annual Budget Process & Accountability','Executive & Board Financial Reporting','Month-End Close & Controls','Cash-Flow Forecasting','Audit, Tax & Regulatory Filings','Multi-Entity Consolidated Reporting','ERP Implementation (Sage Intacct-class)','AP/AR, Payroll & Banking Oversight','HR & Administration (Outsourced)','Documented, Scalable Processes','Association & Membership Organizations','Team Leadership']),
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

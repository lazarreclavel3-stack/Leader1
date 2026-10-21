"""Generate today's tailored resume specs from base_cfo.json."""
import copy, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
base = json.load(open(os.path.join(HERE, '..', '..', 'base_cfo.json')))

EXTRA = {
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
 dict(slug='01_NJFCU', tagline='CREDIT UNION FINANCE  ·  LIQUIDITY & ALM  ·  CONTROLS, AUDITS & EXAMS  ·  BOARD REPORTING',
  profile='Finance executive with a financial-services foundation and senior experience leading finance in regulated, publicly funded organizations. Earlier career in credit-union and financial-services markets, including benefits programs that reached 2,100+ credit-union members, SME debt and equity financing, and wealth management; previously held FINRA Series 7 and 63 licenses. Leads budgeting, forecasting, treasury, and liquidity management, including covenant monitoring, short-term financing analysis, and stress testing; directs audit readiness, GAAP compliance, and internal controls; and explains complex financial information clearly to CEOs, Boards, and committees. Reversed a $1M operating deficit into a 13% surplus and recovered $1.5M+ in tax savings.',
  lead=['E009','E003','E004','E029','E030','E031','E027','E012','E008','E005'], extra=['E029','E030','E031'],
  caps=['Liquidity, Investments & ALM Support','Interest-Rate & Stress Testing Analysis','Budgeting, Forecasting & Reporting','GAAP, Audits & Regulatory Exams','Internal Controls','Board & Committee Reporting','Credit Union & Member Markets','SME Lending & Financing Structures','Collections & Working Capital','Finance Team Leadership','Former FINRA Series 7 / 63','CRM & ERP Systems']),
 dict(slug='02_Inclusiv', tagline='NONPROFIT FINANCE  ·  CDFI & CREDIT UNION MARKETS  ·  BUDGET & MULTI-YEAR PLANNING  ·  CONTROLS & AUDIT',
  profile='Finance executive combining nonprofit financial leadership with deep roots in community finance. Leads annual budgets, multi-year financial planning, revenue and expense forecasting with variance reporting, cash management, and internal controls; directs audit readiness and fund accounting under GAAP and Uniform Guidance; and supports capital allocation and investment decisions through scenario modeling. Earlier career in credit-union, small-business finance, and wealth-management markets, structuring debt and equity options for SMEs with $1M–$50M in revenue; previously held FINRA Series 7 and 63 licenses. Reversed a $1M operating deficit into a 13% surplus at a $50M+ nonprofit and modernizes financial systems and reporting.',
  lead=['E003','E004','E006','E030','E029','E031','E012','E015','E038','E027'], extra=['E029','E030','E038'],
  caps=['Annual Budget & Multi-Year Planning','Forecasting & Variance Reporting','Controller & Finance Team Oversight','Cash Management & Internal Controls','Portfolio & Investment Analytics','Audit & Form 990 Oversight','Financial Systems & Reporting Improvement','CDFI & Credit Union Markets','Small-Business & Community Lending','Nonprofit Financial Management','Board Reporting','Former FINRA Series 7 / 63']),
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

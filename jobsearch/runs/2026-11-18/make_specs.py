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
    'E069': ('MAROON STRATEGIST LLC', 'Prepare and file business and individual tax returns, including dozens of state and local filings, and compile Form 990s for multiple nonprofits; IRS-registered preparer with an active PTIN.'),
    'E068': ('MAROON STRATEGIST LLC', 'Oversee bookkeeping, payroll, AP, AR, invoicing, bank reconciliations, and monthly, quarterly, and annual financial statements for clients.'),
    'E071': ('MAROON STRATEGIST LLC', 'Manage hourly billing and client engagements across multiple accounts, tracked in Salesforce CRM.'),
    'E080': ('MAROON STRATEGIST LLC', 'Built and piloted SkyNet, an AI-supported workflow for research, document preparation, and engagement tracking with cost controls, now in full daily use.'),
    'E055': ('MAROON STRATEGIST LLC', 'Build KPI dashboards, forecasts, and client and retention analytics that leaders use to make decisions.'),
    'E077': ('FITNESS COLLECTIVE INC', 'Created pricing for all services, connecting cost, staffing, and demand.'),
    'E076': ('FITNESS COLLECTIVE INC', 'Scaled the workforce from 4 to 60 full-time employees; created roles and ran recruitment, staffing, and scheduling.'),
})
JOBS = [
 dict(slug='01_TaxAdvisory_PresidentCOO', tagline='PRESIDENT & COO  ·  P&L OWNERSHIP  ·  TAX & ADVISORY OPERATIONS  ·  GROWTH & RETENTION  ·  AI-ENABLED SCALE',
  profile='Operator who has owned the P&L, sales, delivery, people, and finance together, and who measures growth by collected profit, not booked revenue. Held full P&L accountability for an $80M portfolio and a 140-person division, reversing a $1M operating deficit into a 13% surplus through cost ownership, controls, and pricing discipline. Tax-advisory fluent: an IRS-registered tax preparer with an active PTIN who prepares business, individual, and multi-state returns, oversees client bookkeeping, and recovered $1.5M+ in tax savings for clients. Former Series 7/63 wealth and small-business advisor. Built a multi-location business from $5K to $1M in revenue, set pricing for every service, and scaled the team from 4 to 60. Scales with systems and AI: built SkyNet, an AI workflow now in daily use, and led ERP and CRM rollouts that cut processing time 60%.',
  lead=['E010','E012','E013','E069','E008','E068','E080','E055','E071','E003','E005','E015','E014','E016','E017','E050','E033','E077','E076','E036','E029','E030','E031'],
  extra=['E069','E068','E080','E055','E071','E077','E076','E030','E031'],
  caps=['Full P&L & EBITDA Ownership','Collected-Cash Discipline & Budgets','Tax Preparation & Advisory (Active PTIN)','Bookkeeping & Client Accounting Services','Sales, Channels & Partnerships','Pricing & Product Packaging','Client Delivery & Retention','Executive Team Building & Accountability','Workforce Planning & Salary Bands','AI Adoption & Operating Systems','CRM & ERP Implementation','Wealth & Small-Business Advisory']),
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

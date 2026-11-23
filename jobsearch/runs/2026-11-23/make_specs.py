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
    'E069': ('MAROON STRATEGIST LLC', 'Compile Form 990 returns for multiple nonprofits and prepare business and individual tax filings, including state and local returns; IRS-registered preparer with an active PTIN.'),
    'E070': ('MAROON STRATEGIST LLC', 'Lead annual audit coordination and readiness testing for workforce development, healthcare, and smaller 501(c)(3) organizations.'),
    'E068': ('MAROON STRATEGIST LLC', 'Oversee payroll, AP, AR, bank reconciliations, and monthly, quarterly, and annual financial statements for boards and funders.'),
    'E067': ('MAROON STRATEGIST LLC', 'Serve as fractional CFO for a physician practice in an IPA, managing IPA-related finances and billing to Medicaid managed care and commercial insurance plans.'),
    'E080': ('MAROON STRATEGIST LLC', 'Built and piloted SkyNet, an AI-supported workflow for research, document preparation, and engagement tracking, now in full daily use.'),
    'E061': ('THE OSBORNE ASSOCIATION', 'Managed multiple restricted program budgets with monthly reconciliation and quarterly performance tracking; monitored restricted and unrestricted cash flow against donor and grant intent.'),
    'E065': ('THE OSBORNE ASSOCIATION', 'Partnered with the CEO and Board, including the Finance and Audit Committees, on planning, risk, resource allocation, and sustainability.'),
    'E060': ('THE OSBORNE ASSOCIATION', 'Built pricing, monetization plans, and budgets for earned-revenue service lines.'),
    'E079': ('PFP FINANCIAL · AMERICAN EXPRESS (CONSULTING) · FIRST PROVIDENCE FINANCIAL GROUP', 'Advised Medicare and Medicaid beneficiaries on Aetna plan benefits and enrollment; worked with hospitals and health-insurance agents; sold commercial insurance to organizations.'),
})
JOBS = [
 dict(slug='01_BrooklynOrg', tagline='CHIEF FINANCIAL OFFICER  ·  FUND ACCOUNTING & RESTRICTED FUNDS  ·  INVESTMENT OVERSIGHT  ·  AUDIT & FORM 990  ·  BOARD REPORTING',
  profile='Brooklyn-rooted finance executive who pairs nonprofit fund accounting with investment and wealth-management depth. Leads budgeting, cash-flow forecasting, monthly board reporting, and internal controls; manages annual audits and compiles Form 990s as an IRS-registered preparer with an active PTIN. Tracks restricted and designated funds against donor and grant intent across multi-program portfolios, including an $80M portfolio with full P&L accountability, and partners with Boards and Finance and Audit Committees. Former Series 7/63 wealth-management and private-banking advisor who managed affluent-client relationships across investment advisory; builds pricing and fee models, break-even analyses, and growth scenarios. Reversed a $1M deficit into a 13% surplus and recovered $1.5M+ in tax savings. Founded and ran a business in Brooklyn for over a decade.',
  lead=['E003','E004','E069','E070','E068','E008','E005','E010','E061','E065','E012','E060','E013','E016','E015','E014','E017','E050','E051','E033','E036','E031','E030','E029'],
  extra=['E069','E070','E068','E061','E065','E060','E030','E031'],
  caps=['Nonprofit Fund Accounting (GAAP)','Restricted, Designated & Endowed Funds','Investment Oversight & Advisor Relations','Fee, Pricing & Break-Even Modeling','Budgeting & Cash-Flow Forecasting','Annual Audit & Form 990 (Active PTIN)','Board & Committee Reporting','Internal Controls & Financial Systems','Wealth Management Background (Series 7/63, former)','Finance Team Leadership','Donor Intent & Compliance','Brooklyn Community Roots']),
 dict(slug='02_Granted', tagline='CHIEF OPERATING OFFICER  ·  HEALTHCARE & INSURANCE  ·  FINANCE & PLANNING  ·  PARTNERSHIPS  ·  AI-NATIVE OPERATIONS',
  profile='Operator who builds functions from scratch and runs them with commercial and financial rigor, with hands-on fluency in how US healthcare payment works. Serves as fractional CFO to a physician practice in an IPA, managing billing to Medicaid managed care and commercial plans, and earlier advised Medicare and Medicaid beneficiaries on plan benefits and sold commercial insurance to employers. Held full P&L accountability for an $80M portfolio and led a 140-person division, reversing a $1M deficit into a 13% surplus and negotiating $10M+ in partner contracts. Founded and scaled a multi-location business from 4 to 60 employees. Runs budgeting, forecasting, cash, and board reporting; designs org structures and compensation; and works AI-native, having built SkyNet, an AI workflow now in daily use. MBA.',
  lead=['E067','E080','E003','E068','E055','E010','E012','E013','E060','E027','E079','E015','E014','E016','E033','E076','E036','E017','E050'],
  extra=['E067','E080','E068','E060','E079'],
  caps=['Company Operating System & Goal Cadence','Budget, Forecast, Cash & Runway','Board & Investor Reporting','Healthcare Payers, Benefits & Billing','Partnerships & B2B2C Deals','Pricing & Business Cases','Org Design, Leveling & Compensation','Contracts & Outside Counsel','AI-Native Workflows','Building Functions from Scratch','P&L Ownership','Team Leadership']),
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

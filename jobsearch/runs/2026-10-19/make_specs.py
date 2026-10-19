"""Generate today's tailored resume specs from base_cfo.json."""
import copy, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
base = json.load(open(os.path.join(HERE, '..', '..', 'base_cfo.json')))

EXTRA = {
    'E002': ('MAROON STRATEGIST LLC', 'Provide hands-on leadership in multi-entity finance, public funding, capital strategy, and audit remediation.'),
    'E036': ('FITNESS COLLECTIVE INC', None),
    'E038': ('ALLUEL LOGISTICS', 'Selected, implemented, and trained teams on CRM and business systems, including Salesforce, Zoho, Looker, SQL, and ERP platforms.'),
    'E039': ('THE OSBORNE ASSOCIATION', 'Built and managed relationships with government, philanthropic, corporate, and community partners, including the City of New York, to generate contracts and programs.'),
    'E040': ('THE OSBORNE ASSOCIATION', 'Represented the organization publicly at panels, stakeholder forums, and NYC Climate Week.'),
    'E056': ('THE OSBORNE ASSOCIATION', 'Coached and developed managers and staff, building training and talent-development practices across the division.'),
    'E053': ('MAROON STRATEGIST LLC', 'Developed education, entrepreneurship, and financial-literacy program strategies, including monetization approaches.'),
}

JOBS = [
 dict(slug='01_CCM', tagline='NONPROFIT FINANCE  ·  GOVERNMENT CONTRACT COMPLIANCE  ·  AUDIT & CONTROLS  ·  IT & FACILITIES',
  profile='Nonprofit finance executive with deep experience in government-funded human services, bringing hands-on leadership of budgeting, forecasting, cash management, audit readiness, and internal controls. Directed financial controls, billing, and compliance for New York City agency contracts (NYCHA, Department of Homeless Services) and led a 140-person, multi-program social-services division with full P&L accountability. Reversed a $1M operating deficit into a 13% surplus and designed fund-accounting and grant-compliance frameworks under GAAP and Uniform Guidance. Partners closely with the CEO and Board Finance and Audit Committees, and modernizes ERP, IT, and operating systems to give leadership clear, timely financial reporting.',
  lead=['E004','E016','E012','E003','E027','E015','E038','E010','E011'], extra=['E038'],
  caps=['Nonprofit & Fund Accounting','Government & Private Grant Compliance','Budgeting & Forecasting','Cash & Banking Management','Audit & Tax Filing Oversight','Internal Controls','Board Finance & Audit Committee Support','Financial Reporting to Funders','IT & ERP Systems','Facilities & Vendor Oversight','Turnaround & Cost Restructuring','Team Leadership & Development']),
 dict(slug='02_Lantern', tagline='GOVERNMENT CONTRACT FINANCE  ·  GAAP & UNIFORM GUIDANCE  ·  BUDGETING & CASH FLOW  ·  HUMAN SERVICES',
  profile='Finance executive for mission-driven human-services organizations, with direct experience serving New York City homelessness and housing systems. Directed financial controls, billing, and compliance for NYC Department of Homeless Services and NYCHA contracts, and led finance and operations for a 140-person social-services division within a $50M+ nonprofit. Leads annual budgeting, multi-year planning, forecasting, cash flow, and banking relationships; directs audit readiness under GAAP and Uniform Guidance and designs internal controls and fund-accounting frameworks. Reversed a $1M operating deficit into a 13% surplus and serves as a trusted advisor to the Executive Director and Board Finance and Audit Committee.',
  lead=['E016','E004','E003','E012','E009','E027','E010','E011'], extra=['E038'],
  caps=['Government Contract Finance & Claiming','Cost Allocation & Indirect Cost Recovery','GAAP for Nonprofits','Uniform Guidance & Audit Readiness','Budgeting & Multi-Year Planning','Cash Flow & Banking Relationships','Internal Controls','Form 990 & Regulatory Filings Oversight','Board Finance & Audit Committee','Financial Systems & Excel Modeling','Supportive Housing & Homeless Services','Finance Team Leadership']),
 dict(slug='03_NewVisions', tagline='STRATEGIC FINANCE  ·  NYC & NYS GOVERNMENT CONTRACTS  ·  MULTI-YEAR MODELING  ·  SYSTEMS & DATA',
  profile='Finance and administration executive who builds the financial infrastructure mission-driven organizations need to grow. Leads long-term planning, forecasting, and multi-year scenario modeling; directs audit readiness, internal controls, and fund accounting; and has managed New York City agency contracts end to end, from budgeting and billing through compliance and audit preparation. Held P&L accountability for an $8M portfolio and a 140-person division within a $50M+ nonprofit, reversing a $1M deficit into a 13% surplus. MBA with a record of modernizing ERP, CRM, and data systems and of explaining finance clearly to program leaders, executives, and Boards. Also brings experience designing education and financial-literacy program strategies.',
  lead=['E006','E003','E016','E004','E015','E038','E012','E027','E053'], extra=['E038','E053'],
  caps=['Long-Term Financial Planning','Multi-Year Financial Modeling','NYC/NYS Government Contract Budgeting, Billing & Compliance','Audit Oversight & Preparation','Internal Controls','Financial Systems & Data Infrastructure','Administration Team Leadership','Board & President Partnership','Translating Finance for Non-Financial Leaders','Cash Flow & Treasury','Education & Nonprofit Sector','Change Management']),
 dict(slug='04_FPHNYC', tagline='NONPROFIT CFO  ·  GRANTS & GOVERNMENT CONTRACTS  ·  ERP & SALESFORCE  ·  BOARD REPORTING',
  profile='Nonprofit finance executive who pairs public-sector contract expertise with modern financial systems. Leads financial policy, budgeting, forecasting, and compliance; directs audit readiness under GAAP and Uniform Guidance; and has overseen billing and compliance for New York City agency contracts. Implemented ERP and CRM platforms, including Salesforce, and renegotiated vendor contracts to cut costs 35%. Held P&L accountability for an $8M portfolio and a 140-person division within a $50M+ nonprofit, turning a $1M deficit into a 13% surplus. Presents financial analysis clearly to Boards and Finance Committees and advises executive teams on financial and risk matters.',
  lead=['E004','E016','E003','E038','E015','E014','E027','E012','E010'], extra=['E038'],
  caps=['Financial Policy & Compliance','Budgeting & Financial Reporting','Single-Audit Readiness & Auditor Liaison','Grant Management & Government Contract Billing','ERP & Financial Systems (Salesforce)','Office Operations & Vendor Contracts','Board & Finance Committee Presentations','Risk Advisory','Controller & Finance Team Leadership','Public Health & Human Services','Strategic Planning','Turnaround & Cost Restructuring']),
 dict(slug='05_Seamens', tagline='STRATEGIC FINANCE  ·  GOVERNMENT GRANTS & CONTRACTS  ·  CASH MANAGEMENT  ·  SYSTEMS MODERNIZATION',
  profile='Finance executive for multi-site, government-funded human-services organizations. Strategic advisor to CEOs, executive teams, and Boards on budgeting, forecasting, cash management, and growth. Directed financial controls, billing, and compliance for New York City agency contracts; designed internal controls and fund-accounting frameworks; and led audit readiness under GAAP and Uniform Guidance. Modernized operations by implementing ERP-based systems that improved processing efficiency 60%. Held P&L accountability for a 140-person, multi-program division and reversed a $1M operating deficit into a 13% surplus.',
  lead=['E003','E016','E004','E009','E015','E027','E012','E011','E005'], extra=['E038','E056'],
  caps=['Enterprise Budgeting & Forecasting','Cash Management & Liquidity','Government Grant & Contract Finance','Compliance & Risk Management','Audit Oversight','Financial Systems Modernization (ERP, Procurement)','Multi-Site Operations','NYC & NYS Funders','CEO & Board Advisory','Finance Team Development','Child & Family Services Sector','Turnaround & Remediation']),
 dict(slug='06_NHeLP', tagline='CHIEF OPERATING & FINANCIAL LEADERSHIP  ·  TREASURY  ·  GRANT COMPLIANCE  ·  OPERATIONS, IT & PEOPLE',
  profile='Combined finance and operations executive who builds scalable infrastructure for growing mission-driven organizations. Leads financial planning, budgeting, forecasting, treasury, and liquidity strategy; manages restricted and unrestricted funding under GAAP and Uniform Guidance with fund-accounting frameworks; and directs audit readiness and enterprise risk work. Has overseen operations, systems, HR, and payroll infrastructure, and led a 140-person, multi-program division within a $50M+ nonprofit. Executed financial clean-ups and audit remediation for client organizations, and partners with Executive Directors and Board committees on long-range planning, risk, and growth.',
  lead=['E003','E004','E009','E005','E027','E011','E038','E036'], extra=['E038','E036','E002'],
  caps=['Financial Planning, Budgeting & Forecasting','Treasury & Investment Oversight','Restricted & Unrestricted Grant Compliance','Enterprise Risk Management','Audit & Form 990 Oversight','In-House Accounting Buildout','Operations, IT & HR Leadership','Fund Accounting','Board Committee Advisory','Executive Team Leadership','Policy & Advocacy Organizations','Remote Team Management']),
 dict(slug='07_CLA', tagline='OUTSOURCED CFO SERVICES  ·  NONPROFIT CLIENTS  ·  CAPITAL PLANNING  ·  BOARD ADVISORY',
  profile='Advisory CFO who leads finance for multiple nonprofit and mission-driven clients at once. Through Maroon Strategist, provides FP&A, budgeting, treasury, cash-flow forecasting, audit readiness, internal controls, and fund accounting for organizations across nonprofit, private, education, and public-sector settings. Executes turnarounds and audit remediation, recovered $1.5M+ in client tax savings, and structures funding and capital strategy through scenario modeling. Previously held P&L accountability for an $8M portfolio within a $50M+ nonprofit, reversing a $1M deficit into a 13% surplus. Builds lasting client relationships and represents organizations at public forums.',
  lead=['E003','E005','E008','E006','E004','E009','E039','E040','E012'], extra=['E039','E040','E002'],
  caps=['Outsourced / Fractional CFO Services','Multi-Client Engagement Management','Financial Policy & Strategy','Capital Planning & Risk Management','KPI & Ratio Analysis','Budgeting & Long-Term Cost Management','Cash Flow & Forecasting','Audit Coordination','Board Presentations','Client Relationship Development','Nonprofit Accounting','Thought Leadership & Public Speaking']),
 dict(slug='08_KIPPNYC', tagline='MULTI-ENTITY FINANCE  ·  CAPITAL STRATEGY  ·  FP&A  ·  SYSTEMS MODERNIZATION',
  profile='Strategic finance executive with experience in multi-entity structures, capital strategy, and systems modernization. Leads FP&A, budgeting, forecasting, treasury, and cash management across multi-entity client organizations; directs audit readiness and internal controls; and has served as financial architect for a $200M national banking-development initiative covering capital planning and financial structuring. Built payroll, HR, and benefits infrastructure and implemented ERP systems that improved processing efficiency 60%. Advises CEOs and Boards on long-range planning and builds financial literacy across leadership teams.',
  lead=['E002','E003','E017','E006','E009','E004','E015','E036','E027'], extra=['E002','E036','E053'],
  caps=['Multi-Entity Finance','FP&A, Budgeting & Forecasting','Capital & Real Estate Strategy Support','Debt & Financing Analysis','Treasury & Cash Management','Audit Readiness & Internal Controls','Payroll Integration','Finance Systems Modernization','CEO & Board Advisory','Financial Literacy for Leaders','Education Sector','Finance Team Leadership']),
]

def ev(b): return set(b['evidence'])
for j in JOBS:
    s = copy.deepcopy(base)
    s['tagline'], s['profile'], s['capabilities'] = j['tagline'], j['profile'], j['caps']
    lead = j['lead']
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

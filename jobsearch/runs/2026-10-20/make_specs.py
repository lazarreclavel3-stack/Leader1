"""Generate today's tailored resume specs from base_cfo.json."""
import copy, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
base = json.load(open(os.path.join(HERE, '..', '..', 'base_cfo.json')))

EXTRA = {
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
 dict(slug='01_CleanSlate', tagline='CHIEF FINANCIAL & ADMINISTRATIVE LEADERSHIP  ·  GRANTS ADMINISTRATION  ·  SYSTEMS  ·  REENTRY & JUSTICE',
  profile='Finance and administration executive with deep roots in criminal-justice and reentry work. At The Osborne Association, held P&L accountability for an $8M portfolio and a 140-person division serving justice-impacted New Yorkers, reversing a $1M operating deficit into a 13% surplus. Leads financial planning, budgeting, treasury, and cash-flow forecasting; manages restricted funding and grant compliance under GAAP and Uniform Guidance; and builds modern financial and organizational systems that give staff and Boards real-time visibility. Integrates finance, grants, talent, and operations, with hands-on experience in HR, payroll, and ERP/CRM implementation, and partners with Presidents and Boards on long-range planning and growth.',
  lead=['E003','E004','E012','E010','E011','E024','E038','E036','E027','E002'], extra=['E038','E002','E056'],
  caps=['Integrated Finance, Grants & Operations Strategy','Grants Administration & Compliance','Budgeting, Forecasting & Treasury','Real-Time Financial Reporting Systems','Talent & Culture / HR Infrastructure','Board & President Partnership','Audit Readiness & Internal Controls','Scaling Organizations Through Growth','Restricted Funding Management','Criminal Justice & Reentry Sector','ERP / CRM Implementation','Team Leadership & Development']),
 dict(slug='02_NDWA', tagline='CHIEF OPERATING LEADERSHIP  ·  FINANCIAL STRATEGY  ·  HR, TECHNOLOGY & OPERATIONS  ·  MULTI-ENTITY',
  profile='Operations and finance executive with 20+ years leading multi-functional teams in mission-driven, worker-centered, and entrepreneurial organizations. Has directly overseen organizational finance at a senior level: long-term planning, business modeling, budgeting, forecasting, reserves and capital strategy, and Board and Finance Committee reporting. Led a 140-person division spanning workforce development, social services, and social enterprises within a $50M+ nonprofit, reversing a $1M deficit into a 13% surplus. Brings multi-entity finance experience, HR and payroll infrastructure, technology implementation, and a career-long commitment to economic justice and good jobs for workers. MBA.',
  lead=['E011','E010','E012','E006','E003','E002','E027','E036','E038','E019','E024'], extra=['E002','E036','E038'],
  caps=['Senior Organizational Finance Oversight','Business Modeling & Long-Term Forecasting','Budgeting, Reserves & Capital Planning','Board & Finance Committee Reporting','Multi-Entity Nonprofit Structures','HR, Legal, Technology & Operations','Cost Management','Workforce & Economic Justice','Multi-Functional Team Leadership','Remote & Distributed Teams','Change Management','Strategic Planning']),
 dict(slug='03_NDRN', tagline='CHIEF OPERATING LEADERSHIP  ·  FEDERAL GRANTS & CONTRACTS  ·  ACCOUNTABILITY SYSTEMS  ·  DISABILITY INCLUSION',
  profile='Chief operating executive who aligns operations with strategy and builds accountability and performance systems that hold. Has overseen complex government grants and contracts, including New York City agency contracts and a publicly funded NYPA clean-energy workforce program, along with their compliance, deliverables, and performance metrics. Partnered with NYSID on projects employing people with disabilities across public-sector initiatives. Led a 140-person, multi-program division with senior managers reporting directly, and partners with CEOs and Boards on long-range planning, risk, and growth. 20+ years of progressive leadership; MBA.',
  lead=['E016','E007','E023','E022','E011','E027','E055','E004','E012'], extra=['E022','E023','E055'],
  caps=['Operations Aligned to Strategy','Accountability & Performance Systems','Federal Grants, Cooperative Agreements & Contracts','Grant Compliance & Deliverables','Senior Staff Leadership','Cross-Functional Coordination','Board Support & Governance','Coalition & Stakeholder Engagement','Disability Employment & Inclusion','KPI Dashboards','Resource Stewardship','Change Management']),
 dict(slug='04_NRPA', tagline='STRATEGIC FINANCE  ·  FINANCE FUNCTION MODERNIZATION  ·  CONTROLS & RISK  ·  BOARD ADVISORY',
  profile='Nonprofit finance executive who builds and modernizes finance functions and turns financial data into decisions. Leads financial planning, budgeting, treasury, liquidity, and cash-flow forecasting; directs audit readiness, internal controls, and compliance under GAAP and Uniform Guidance; and advises CEOs, executive teams, and Boards on long-range planning, investments, and enterprise risk. Reversed a $1M operating deficit into a 13% surplus, recovered $1.5M+ in tax savings, and implemented ERP and analytics systems that improved processing efficiency 60%. Develops finance teams and partners with business-line leaders on revenue growth.',
  lead=['E003','E004','E009','E006','E055','E015','E012','E008','E027','E013'], extra=['E055','E038'],
  caps=['Finance Function Modernization','Actionable Financial Insights & KPIs','Financial Controls, Compliance & Risk','Investments & Enterprise Risk Oversight','Budgeting & Forecasting','Treasury & Liquidity','Board Governance Support','Business-Line Partnership & Growth','Finance Team Development','Audit Readiness','ERP & Analytics','Membership & Association Organizations']),
 dict(slug='05_RIPA', tagline='STRATEGIC FINANCE  ·  REVENUE MIX & RESERVES  ·  BOARD PARTNERSHIP  ·  PARKS & PUBLIC SPACE',
  profile='Hands-on finance executive for mission-driven organizations with mixed public, philanthropic, and earned revenue. Shapes long-term financial strategy, including revenue mix, reserves, and investment and funding strategy, through scenario modeling; leads budgeting, cash flow, audit readiness, and internal controls; and works closely with Presidents and Boards of Trustees. Built earned-revenue social enterprises, structured $10M+ in government and institutional contracts, and reversed a $1M deficit into a 13% surplus. Experienced running finance with a lean team while modernizing systems and reporting.',
  lead=['E006','E003','E042','E043','E013','E012','E027','E004','E009'], extra=['E039'],
  caps=['Long-Term Financial Strategy','Revenue Mix & Earned Revenue','Reserves & Investment Strategy','Board of Trustees Partnership','Budgeting & Cash Flow','Audit & Internal Controls','Public-Private Partnerships','Government Contracts','Lean Team Leadership','Scenario Modeling','Financial Systems','Parks, Recreation & Public Space']),
 dict(slug='06_Columbia', tagline='BUDGET & FINANCIAL PLANNING  ·  MULTI-ENTITY FP&A  ·  SCENARIO MODELING  ·  CAPITAL STRATEGY',
  profile='Strategic finance executive specializing in budgeting, financial planning, and scenario modeling for complex, multi-entity organizations. Leads FP&A, budgeting, treasury, liquidity, and cash-flow forecasting for client organizations across nonprofit, education, private, and public-sector settings, and supports capital allocation through scenario modeling and funding strategy. Served as financial architect for a $200M national banking-development initiative and reversed a $1M operating deficit into a 13% surplus. Pairs analytical depth (SQL, Looker, KPI dashboards) with clear communication to senior leadership and Boards.',
  lead=['E003','E006','E002','E009','E017','E055','E012','E027','E053'], extra=['E002','E055','E053'],
  caps=['University-Wide Budget Strategy Support','Financial Planning & Analysis','Multi-Year Scenario Modeling','Capital Allocation','Multi-Entity Budgeting','Liquidity & Cash Forecasting','KPI Dashboards & Analytics (SQL, Looker)','Executive & Board Communication','Education Sector','Budget Process Design','Team Leadership','Change Management']),
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

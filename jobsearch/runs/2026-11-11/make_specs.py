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
    'E072': ('MAROON STRATEGIST LLC', 'Created and led an 18-month NYPA clean-energy workforce program from inception; piloted the model before rollout; 92% of enrolled participants completed training and earned a certificate.'),
    'E058': ('THE OSBORNE ASSOCIATION', 'Led 12 direct reports across finance, grant stewardship, and operations through weekly team meetings, individual check-ins, and recurring financial reviews.'),
    'E061': ('THE OSBORNE ASSOCIATION', 'Managed multiple program budgets with monthly reconciliation and quarterly performance tracking; monitored restricted and unrestricted cash flow.'),
    'E085': ('THE OSBORNE ASSOCIATION', 'Ran HR for a workforce program overseeing hundreds of workers, including hiring, supervision, compensation, and employee relations under New York employment law.'),
    'E086': ('THE OSBORNE ASSOCIATION', 'Created HR manuals for the department and the organization.'),
    'E089': ('ALLUEL LOGISTICS', 'Created and administered employee retirement plans, including at Alluel Logistics and for Maroon Strategist clients.'),
    'E076': ('FITNESS COLLECTIVE INC', 'Scaled the workforce from 4 to 60 full-time employees across accounting, IT, facilities, training, and group fitness; created roles and ran recruitment, staffing, and scheduling.'),
})
JOBS = [
 dict(slug='01_Wadhwani', tagline='FINANCE & HUMAN RESOURCES LEADERSHIP  ·  MULTI-ENTITY FINANCE  ·  AUDIT & CONTROLS  ·  TREASURY & GRANTS  ·  PEOPLE OPERATIONS',
  profile='Finance and people executive who builds the financial and organizational infrastructure that mission-driven organizations need to grow. Leads entity-level budgets and forecasts, internal controls, clean audits, treasury, and grant disbursement and reporting across multi-entity and publicly funded organizations; compiles Form 990 returns as an IRS-registered preparer with an active PTIN. Has run HR end to end, including hiring, compensation, HR manuals, retirement plans, payroll and benefits, and employee relations, for workforces ranging from a 60-person company to programs overseeing hundreds of workers. Partners with CEOs and Boards on financial strategy, resource allocation, and risk; held full P&L accountability for an $80M portfolio and reversed a $1M deficit into a 13% surplus. Built workforce-skilling and entrepreneurship programs, including a clean-energy training program with 92% certificate completion.',
  lead=['E003','E004','E068','E069','E070','E072','E009','E010','E012','E085','E061','E058','E027','E086','E016','E089','E015','E014','E017','E050','E051','E076','E036','E033'],
  extra=['E068','E069','E070','E072','E058','E061','E085','E086','E089','E076'],
  caps=['Finance & HR Function Leadership','Entity-Level Budgets & Forecasting','FP&A & Financial Governance','Internal Controls & Clean Audits','Treasury & Grant Disbursement','Form 990 & Tax Compliance (Active PTIN)','Multi-Entity Accounting','HR Policies, Manuals & Compliance','Compensation, Payroll & Benefits','Retirement Plan Administration','Board & CEO Partnership','Workforce & Entrepreneurship Programs']),
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

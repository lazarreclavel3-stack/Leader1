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
    'E072': ('MAROON STRATEGIST LLC', 'Created and led an 18-month NYPA clean-energy workforce training program from inception; piloted the model before full rollout; 92% of enrolled participants completed training and earned a certificate.'),
    'E073': ('MAROON STRATEGIST LLC', 'Built a coalition of city and state agencies, elected officials, academic partners, Stanford Innovation Lab, KPMG, and NYPA around training delivery and employer pathways.'),
    'E081': ('MAROON STRATEGIST LLC', 'Designed a Citi Foundation proposal for an AI career-launch program linking AI learning, workforce preparation, and employment support, with measures for skills, employment, wages, and retention.'),
    'E080': ('MAROON STRATEGIST LLC', 'Built and piloted SkyNet, an AI-supported workflow for research, evaluation, document preparation, and engagement tracking, now in full daily use.'),
    'E055': ('MAROON STRATEGIST LLC', 'Design KPI dashboards, forecasts, and outcome measures that give leaders and funders a real-time view of performance.'),
    'E024': ('THE OSBORNE ASSOCIATION', 'Owned an employment and workforce-development model integrating job readiness, placement, and wraparound supports for justice-impacted adults.'),
    'E058': ('THE OSBORNE ASSOCIATION', 'Led 12 direct reports across finance, grant stewardship, and operations through weekly operating reviews, individual check-ins, and clear performance standards.'),
    'E085': ('THE OSBORNE ASSOCIATION', 'Ran HR for a workforce program overseeing hundreds of workers, including hiring, supervision, compensation, and employee relations; wrote the HR manuals.'),
    'E060': ('THE OSBORNE ASSOCIATION', 'Built pricing, monetization plans, and budgets for earned-revenue service lines.'),
})
JOBS = [
 dict(slug='01_Pursuit', tagline='CHIEF OPERATING OFFICER  ·  WORKFORCE DEVELOPMENT  ·  KPIs & DASHBOARDS  ·  FINANCE & PEOPLE OPERATIONS  ·  AI-NATIVE SCALE',
  profile='Operator with both an advisory and a hands-on operating track record, who turns strategy into the KPIs, dashboards, workflows, and accountability systems that let mission-driven organizations scale. Ran a 140-person workforce and social-enterprise division with full P&L accountability for an $80M portfolio, owning an employment model for justice-impacted adults, earned-revenue lines, and HR for hundreds of program workers; reversed a $1M operating deficit into a 13% surplus. Created a clean-energy workforce training program from inception, piloting before rollout and reaching 92% certificate completion, and built a coalition with Stanford Innovation Lab, KPMG, NYPA, and city and state partners. Designed an AI career-launch program and built SkyNet, an AI workflow now in daily use. Leads finance and people functions as a fractional CFO, and partners with CEOs and Boards on planning, organizational design, and growth. MBA.',
  lead=['E072','E073','E081','E080','E055','E003','E010','E024','E012','E085','E058','E013','E060','E042','E027','E015','E014','E016','E050','E017','E051','E033','E036'],
  extra=['E072','E073','E081','E080','E055','E024','E058','E085','E060'],
  caps=['Enterprise Operations & Strategic Execution','KPI Architecture & Executive Dashboards','Performance Management & Accountability','Organizational Design & Change Management','Finance Leadership & Multi-Year Budgeting','People, HR & Talent Systems','Workforce Development & Job Placement','Earned Revenue & Collections','AI-Native Workflows & Internal Tools','Employer, Government & Academic Partnerships','Board Reporting & Governance','Consulting + Hands-On Operating']),
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

"""Resume and cover letter tailored to the YWCA of the City of New York COO search.

Usage:
    python3 resumes/build_ywca.py resume out.docx
    python3 resumes/build_ywca.py letter out.docx
"""
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT

import build_executive_ats as ats
from build_executive_ats import ACCENT, MUTED, RIGHT_TAB, bottom_border, bullet, para, section, style_run
from build_ccm import CONTACT, NAME, page_setup

SKILLS = ('HR Policy & Employee Relations  |  New York Employment Law  |  Payroll, Benefits & Retirement Plans  |  '
          'Talent Acquisition & Performance Management  |  Compensation  |  Board Finance Committee Liaison  |  Budgeting & '
          'Accounts Payable  |  Risk & Insurance  |  Outsourced IT Oversight  |  Facilities & Safety Planning  |  Change Management  |  KPIs')

HEADLINE = 'Chief Operating Officer  |  HR & People Operations  |  Finance, Compliance & Facilities'

SUMMARY = (
    'Operations executive and HR leader with 20+ years of experience building and running the people, finance, '
    'compliance, and facilities infrastructure of mission-driven and multi-site organizations. Has overseen HR for '
    'hundreds of workers, including hiring, supervision, employee relations, compensation, and policy, with working '
    'knowledge of New York employment law. Built HR, payroll, benefits, retirement, and safety systems from the ground up '
    'while growing a five-location business from 4 to 60 full-time employees. Partners with CEOs and Board Finance '
    'Committees, manages outsourced accounting, IT, and vendor relationships, and leads change with a commitment to '
    'equity and social justice in New York City.')

JOBS = [
    ('OSBORNE ASSOCIATION', 'New York, NY', 'Vice President, Business Development & Social Ventures', 'Jan 2023 – Oct 2025',
     'Led a 140-person division and a workforce program employing hundreds of workers in a human-services organization '
     'serving people affected by the criminal legal system.',
     ['Oversaw HR for a workforce program with hundreds of workers, directing hiring, onboarding, supervision, performance '
      'management, and resolution of employee complaints in line with New York employment law.',
      'Wrote HR manuals for the department and for Osborne, establishing policies and procedures for hiring, conduct, '
      'supervision, and compensation.',
      'Managed staff hours, overtime, bonuses, and salary increases for all 140 division employees against budget; '
      'supervised 12 direct reports across finance, grant stewardship, operations, and frontline management.',
      'Established weekly team meetings, individual check-ins, and recurring financial and operational reviews; led '
      'continuous improvement through workflow redesign, compliance meetings, and staff self-assessments.',
      'Helped move the division from a deficit exceeding $1M to a 13% operating surplus within one year; managed multiple '
      'program budgets with monthly reconciliation and quarterly reviews.',
      'Partnered with the CEO and Board, including the Finance and Audit Committees, on planning, risk, and '
      'sustainability; oversaw IT systems, facilities, and vendor contracts across sites.',
      'Oversaw a nine-month transitional-employment program serving 300+ formerly incarcerated people annually, '
      'coordinating employer partnerships and tracking outcomes against funder requirements.',
      'Built pricing, monetization plans, and budgets for earned-revenue social ventures, including landscaping and '
      'warehouse cleaning.',
      'Evaluated a proposed Rikers Island service expansion, modeling staffing, supervision, delivery costs, and '
      'infrastructure needs.',
      'Partnered with the Director of El Rio, a substance use treatment program for people returning from incarceration, '
      'on budgeting, hiring, and participant placements.']),
    ('MAROON STRATEGIST, LLC', 'Brooklyn, NY', 'Fractional Chief Financial Officer', 'Mar 2024 – Present',
     'Fractional CFO and operational leadership for nonprofit, healthcare, education, and service organizations.',
     ['Oversee payroll, accounts payable, vendor payments, invoicing, bank reconciliations, and monthly, quarterly, and '
      'annual financial statements, working alongside outsourced bookkeepers and accountants.',
      'Create and administer retirement plans for client organizations, alongside payroll and benefits processes.',
      'Manage hourly billing and client engagement tracking in CRM systems, including Salesforce.',
      'Direct budgeting, forecasting, cash-flow planning, internal controls, and annual audit coordination; as an '
      'IRS-registered tax preparer, compile Form 990 returns for nonprofits.',
      'Support a behavioral health practice’s payroll and benefits processes, staffing, vendor oversight, and financial '
      'controls.',
      'Created and led an 18-month NYPA workforce program from inception, standing up staffing, budgets, partnerships, '
      'and training; 92% of enrolled participants completed training and earned a certificate.',
      'Lead reconciliations and reporting remediation with clients, bookkeepers, and accounting advisers to improve the '
      'reliability of financial records.',
      'Lead proposal development and partnership agreements with public agencies, academic partners, and employers; '
      'track program KPIs and funder compliance through monthly and quarterly reviews.',
      'Build KPI dashboards and standard operating procedures that help leadership track performance and implement '
      'changes.']),
    ('ALLUEL LOGISTICS', 'New York, NY', 'Vice President of Operations', 'Nov 2021 – Aug 2022', None,
     ['Created and administered the company’s retirement plan; recruited and managed field, sales, and administrative '
      'staff and improved HR workflows and data accuracy with IT.',
      'Managed a $2M operating budget and vendor agreements that cut costs 35%; led a warehouse-management system rollout '
      'that reduced processing time 60%.',
      'Directed contract billing and compliance for NYC Department of Homeless Services and NYCHA contracts.']),
    ('FITNESS COLLECTIVE INC.', 'Brooklyn, NY', 'Co-Founder & Chief Executive Officer', '2004 – 2016',
     'Built and led a five-location health and wellness business, including franchise sites, creating its people, '
     'payroll, facilities, and technology infrastructure from the ground up.',
     ['Scaled the workforce from 4 to 60 full-time employees across accounting, IT, facilities, personal training, and '
      'group fitness; created roles, recruited, supervised, and trained staff.',
      'Built HR, payroll, and benefits infrastructure from scratch, overseeing recruitment, training, performance '
      'management, scheduling, and approximately $65K in monthly payroll.',
      'Wrote safety plans and procedures for all five locations, including company-owned and franchise sites, '
      'standardizing site safety and emergency readiness.',
      'Managed facilities, landlord relationships, insurance, utilities, and vendor contracts across all locations.',
      'Established a training academy that certified 25 trainers, creating a career pathway and internal talent pipeline.',
      'Grew a $5,000 investment into $1M in annual revenue within 24 months, then built a franchise model and expanded to '
      'five locations and $10M in annual sales.',
      'Built neighborhood partnerships, outreach, and community events to establish a presence at each location.',
      'Implemented Mindbody CRM for scheduling, client records, and reporting across 4,000+ clients.']),
    ('LAZARRE CONSULTING GROUP', 'New York, NY', 'Founder & Fractional CFO', 'Dec 2016 – Present', None,
     ['Led financial remediation for a behavioral health practice, reconciling records, identifying approximately $251K in '
      'unclaimed deductions, and preparing corrected financial statements.',
      'Developed operational and performance-improvement strategies for organizations including American Express OPEN, '
      'Ogilvy, and Chubb; supported capital planning for a $200M national banking development initiative.']),
]

ADDITIONAL = ('Sold commercial insurance and advised organizations on employee benefits structures and coverage costs; '
              'previously held Life, Accident & Health insurance licenses.')
SYSTEMS = ('QuickBooks  |  Excel  |  Monday.com  |  Salesforce  |  Zoho CRM  |  Mindbody  |  Airtable  |  Google Workspace  '
           '|  SkyNet (AI workflow, in daily use)')
EDUCATION = [
    ('Master of Business Administration, General Business Management', 'West Texas A&M University', '2023'),
    ('Bachelor of Science, Small Business Administration', 'Northern Arizona University', ''),
]

LETTER = [
    'Dear YWCA of the City of New York Hiring Committee,',
    'I am writing to apply for the position of Chief Operating Officer. Since 1858, the YWCA of the City of New York has '
    'served New Yorkers, and today it reaches more than 3,000 young people every year. A COO who keeps people, finances, compliance, and facilities running smoothly lets program '
    'teams focus on that mission. That is the work I do best, and I would welcome the opportunity to do it for the YWCA.',
    'People operations have been at the center of my career. At the Osborne Association, I oversaw HR for a workforce '
    'program with hundreds of workers, directing hiring, onboarding, supervision, performance management, and the '
    'resolution of employee complaints in line with New York employment law. I wrote HR manuals for my department and '
    'for Osborne, managed hours, overtime, bonuses, and raises for a 140-person division, and supervised 12 direct '
    'reports through a steady cadence of team meetings, check-ins, and operating reviews. I have also created and '
    'administered retirement plans, at Alluel Logistics and for clients of my fractional CFO practice.',
    'I know how to build these systems from the ground up. As co-founder of Fitness Collective, I grew a five-location '
    'business from 4 to 60 full-time employees, building its HR, payroll, and benefits infrastructure, writing safety '
    'plans for every site, managing landlord relationships, insurance, and vendors, and creating a training academy that '
    'certified 25 trainers. That experience maps directly to supporting the YWCA’s staff and sites.',
    'On the finance side, I work alongside outsourced accountants and bookkeepers to oversee payroll, accounts payable, '
    'reconciliations, budgets, and financial statements, and I partnered with Osborne’s CEO and the Board’s Finance and '
    'Audit Committees on planning and risk. I helped move my division from a deficit exceeding $1M to a 13% operating '
    'surplus within one year, and I have overseen IT systems, facilities, and vendor contracts across multiple sites.',
    'I would welcome the opportunity to discuss how I can support the YWCA’s staff, strengthen its operations, and help '
    'advance its strategic plan. Thank you for your time and consideration.',
]


def header(doc, with_headline):
    style_run(para(doc, align=WD_ALIGN_PARAGRAPH.CENTER).add_run(NAME), size=22, bold=True, color=ACCENT)
    if with_headline:
        style_run(para(doc, before=2, align=WD_ALIGN_PARAGRAPH.CENTER).add_run(HEADLINE), size=11.5, bold=True)
    p = para(doc, before=3, after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    style_run(p.add_run(CONTACT), size=10, color=MUTED)
    bottom_border(p, size=12)


def build_resume(out):
    doc = Document()
    page_setup(doc, 0.6, 0.5, ats.BODY_PT)
    header(doc, True)
    section(doc, 'Professional Summary')
    style_run(para(doc, after=1, line=1.05).add_run(SUMMARY))
    section(doc, 'Core Competencies')
    style_run(para(doc, after=1, line=1.05).add_run(SKILLS))
    section(doc, 'Selected Professional Experience')
    for org, loc, title, dates, summary, bullets in JOBS:
        p = para(doc, before=5, keep_next=True)
        p.paragraph_format.tab_stops.add_tab_stop(RIGHT_TAB, WD_TAB_ALIGNMENT.RIGHT)
        style_run(p.add_run(org), bold=True, color=ACCENT)
        style_run(p.add_run(f'  |  {loc}'), color=MUTED)
        style_run(p.add_run('\t' + dates), bold=True)
        style_run(para(doc, after=1, keep_next=True).add_run(title), bold=True, italic=True)
        if summary:
            style_run(para(doc, after=1.5, keep_next=True).add_run(summary), size=10, italic=True, color=MUTED)
        for b in bullets:
            bullet(doc, b)
    section(doc, 'Additional Experience')
    bullet(doc, ADDITIONAL, 'PFP Financial / PFP Insurance')
    bullet(doc, 'Advised Medicare and Medicaid beneficiaries on Aetna plan benefits, coverage options, and enrollment.')
    section(doc, 'Systems & Technology')
    style_run(para(doc, after=1).add_run(SYSTEMS))
    section(doc, 'Education')
    for degree, school, year in EDUCATION:
        p = para(doc, after=1)
        p.paragraph_format.tab_stops.add_tab_stop(RIGHT_TAB, WD_TAB_ALIGNMENT.RIGHT)
        style_run(p.add_run(degree), bold=True)
        style_run(p.add_run(f'  |  {school}'))
        if year:
            style_run(p.add_run('\t' + year))
    doc.core_properties.title = 'Clavel Lazarre, MBA — Resume (COO)'
    doc.core_properties.author = 'Clavel Lazarre'
    doc.save(out)


def build_letter(out):
    doc = Document()
    page_setup(doc, 0.9, 0.7, 11)
    header(doc, False)
    for i, text in enumerate(LETTER):
        style_run(para(doc, before=12 if i == 0 else 0, after=8, line=1.1).add_run(text), size=11)
    style_run(para(doc, before=2, after=2).add_run('Sincerely,'), size=11)
    style_run(para(doc, before=12).add_run('Clavel Lazarre, MBA'), size=11, bold=True)
    doc.core_properties.title = 'Clavel Lazarre, MBA — Cover Letter, YWCA NYC COO'
    doc.core_properties.author = 'Clavel Lazarre'
    doc.save(out)


if __name__ == '__main__':
    {'resume': build_resume, 'letter': build_letter}[sys.argv[1]](sys.argv[2])
    print(sys.argv[2])

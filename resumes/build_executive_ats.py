"""Two-page executive resume, ATS-friendly best-practice layout.

Single column, standard headings, no tables/text boxes/graphics, dates on
right-aligned tab stops, Calibri 10.5pt body, one restrained accent color.

Usage: python3 resumes/build_executive_ats.py out.docx
"""
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ACCENT = RGBColor(0x1F, 0x3A, 0x5F)   # deep navy
TEXT = RGBColor(0x22, 0x22, 0x22)
MUTED = RGBColor(0x55, 0x55, 0x55)
FONT = 'Calibri'
BODY_PT = 10.5
RIGHT_TAB = Inches(7.3)

NAME = 'CLAVEL LAZARRE, MBA'
CONTACT = 'New York, NY  |  347-607-8164  |  lazarreclavel3@gmail.com  |  linkedin.com/in/clavel-lazarre'
HEADLINE = 'Executive Leadership  |  Organizational Growth  |  Strategy & Operations'

SUMMARY = [
    'Operations and finance executive with 20+ years of experience building businesses, leading mission-driven '
    'programs, and creating the systems organizations need to grow. Held full P&L accountability for an $80M '
    'portfolio and financial and operational oversight of a 140-person division. Co-founded a fitness business that '
    'reached $1M in annual revenue within 24 months, then expanded through a franchise model to $10M in annual sales '
    'while growing the team from 4 to 60 full-time employees.',
    'Brings a founder’s understanding of growth and an operator’s discipline in execution, partnering with CEOs, boards, '
    'public agencies, and community organizations to translate strategy into budgets, partnerships, programs, and operations. Committed to building '
    'the people, systems, and operating discipline that allow organizations to scale sustainably and deliver on their mission.',
]

RESULTS = [
    ('Built and expanded a business', 'Grew Fitness Collective from a $5,000 investment to $10M in annual sales and from 4 to '
     '60 full-time employees (15x), establishing a franchise model and three additional locations.'),
    ('Built leadership accountability', 'Managed 12 direct reports within a 140-person division, using weekly meetings, '
     'individual check-ins, and operational and financial reviews to align priorities and guide execution.'),
    ('Created mission-driven programs', 'Led a nine-month transitional-employment program serving 300+ formerly '
     'incarcerated people annually; created and delivered an 18-month NYPA clean-energy workforce program with a 92% certificate-completion rate.'),
    ('Improved operating performance', 'Cut vendor costs 35% and processing time 60% at Alluel Logistics through '
     'negotiation and systems improvements.'),
]

EXPERTISE = ['Organizational Growth', 'General Management', 'P&L Leadership', 'Budgeting & Resource Allocation',
             'CEO & Board Partnership', 'People Operations & Talent Development', 'Program Development',
             'Coalition Building & Partnerships', 'Performance Reporting & KPIs', 'Technology & Process Improvement']

JOBS = [
    ('MAROON STRATEGIST, LLC', 'Brooklyn, NY', 'Chief Financial Strategy Officer', 'Mar 2024 – Present',
     'Fractional CFO and program leadership connecting financial planning with partnerships, operating systems, and execution.',
     ['Created and led the NYPA clean-energy workforce training program from inception through completion over 18 months, '
      'overseeing proposal development, program design, budgeting, partnerships, and training; 92% of enrolled participants '
      'completed the program and earned a certificate, and the program established new energy-sector employer relationships.',
      'Built a coalition involving city and state agencies, elected officials, academic partners, Stanford Innovation Lab, '
      'KPMG, and the New York Power Authority; coordinated responsibilities and resources around training delivery.',
      'Developed and managed a multimillion-dollar budget, allocating direct and indirect costs, managing restricted cash '
      'flow, and aligning expenditures with grant requirements and delivery milestones.',
      'Led fundraising and partnership-agreement development; brought NYSID into the partnership network and liaised with '
      'Assembly partners to develop relationships and opportunities.',
      'Direct budgeting, forecasting, cash management, and multi-entity financial planning; build financial models, KPI '
      'dashboards, and SOPs to support leadership decisions and operating accountability.']),
    ('OSBORNE ASSOCIATION', 'New York, NY', 'Vice President, Business Development & Social Ventures',
     'Jan 2023 – Oct 2025',
     'Led a 140-person division of a human-services organization serving people affected by the criminal legal system.',
     ['Managed 12 direct reports, directing hiring, onboarding, training, performance management, and day-to-day execution '
      'across financial, operational, and program responsibilities.',
      'Established a management cadence of weekly team meetings, individual check-ins, and recurring operational and '
      'financial reviews, using budgets and performance reports to identify issues, align priorities, and guide decisions.',
      'Held full P&L accountability for an $80M portfolio, aligning staffing, budgets, grant obligations, and program '
      'delivery with organizational priorities.',
      'Built growth opportunities across multiple industries through new partnerships, direct funding opportunities, and '
      'business development, incorporating expansion planning into ongoing operations.',
      'Led a nine-month transitional-employment program serving 300+ formerly incarcerated people annually, coordinating '
      'employer partnerships and tracking outcomes against funder benchmarks.',
      'Partnered with the CEO and Board on planning, risk management, resource allocation, and growth; negotiated '
      'government, corporate, and philanthropic partnerships.',
      'Authored a Rikers Island contract feasibility white paper and a roadmap for potentially doubling JMS within 12 '
      'months, identifying required investments in management, staffing, training, compliance, payroll, and technology.']),
    ('ALLUEL LOGISTICS', 'New York, NY', 'Vice President of Operations', 'Nov 2021 – Aug 2022', None,
     ['Managed a $2M operating budget; renegotiated vendor agreements to cut supply-chain and logistics costs 35%.',
      'Implemented warehouse-management technology that reduced data-processing time 60%; introduced CRM systems and '
      'trained staff.',
      'Oversaw NYCHA logistics contracts serving 100 developments and supervised ~$500K in monthly NYC DHS billing.',
      'Recruited and managed field, sales, and administrative staff; improved HR workflows and data accuracy.']),
    ('LAZARRE CONSULTING GROUP', 'New York, NY', 'Chief Executive Officer', 'Dec 2016 – Present',
     'Ongoing private-client advisory practice alongside project-based fractional CFO engagements, providing business '
     'consulting, financial analysis, and personal financial and wealth-management support.',
     ['Served as financial architect for a $200M national banking development initiative, supporting capital planning '
      'and financial structuring.',
      'Developed operational and performance-improvement strategies for organizations and brands including American '
      'Express OPEN, Ogilvy, and Chubb.']),
    ('FITNESS COLLECTIVE INC.', 'Brooklyn, NY', 'CEO & Co-Founder', '2004 – 2016',
     'Built and expanded a health and wellness business by combining direct customer acquisition, neighborhood '
     'partnerships, and the people and technology systems needed to support multiple locations.',
     ['Scaled from a $5,000 investment to $1M in annual revenue within 24 months, then implemented a franchise model and '
      'launched three additional locations, growing to $10M in annual sales.',
      'Scaled the workforce from 4 to 60 full-time employees across accounting, IT, facilities, personal training, and group '
      'fitness; created roles and participated directly in recruitment, supervision, and training.',
      'Built HR, payroll, benefits, and client-management infrastructure to support expansion across multiple locations, '
      'including Mindbody CRM serving a client base of 4,000+.',
      'Led direct outreach, grassroots marketing, website development, and partnerships with local businesses to attract '
      'clients and establish a presence in each operating neighborhood.',
      'Established a training academy supporting certification of 25 trainers, expanding workforce capacity and service '
      'offerings.']),
]

INNOVATION = [
    ('SkyNet', 'Built an AI-supported workflow connecting opportunity research, evaluation, document preparation, and '
     'reporting, with evidence validation, cost controls, and performance tracking.'),
    ('JWA AI Career Launch', 'Designed and submitted a Citi Foundation proposal linking AI learning, workforce '
     'preparation, and employment support, with proposed measures for skills, employment, wages, and retention.'),
]

EDUCATION = [
    ('Master of Business Administration, General Business Management', 'West Texas A&M University', '2023'),
    ('Bachelor of Science, Small Business Administration', 'Northern Arizona University', ''),
]


def style_run(r, size=BODY_PT, bold=False, italic=False, color=TEXT, caps=False):
    r.font.name = FONT
    r._element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    r.font.all_caps = caps
    return r


def para(doc, before=0, after=0, line=1.0, align=None, keep_next=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before, pf.space_after = Pt(before), Pt(after)
    pf.line_spacing = line
    pf.keep_with_next = keep_next
    if align is not None:
        p.alignment = align
    return p


def bottom_border(p, color='1F3A5F', size=8):
    pPr = p._p.get_or_add_pPr()
    bdr = OxmlElement('w:pBdr')
    b = OxmlElement('w:bottom')
    for k, v in (('w:val', 'single'), ('w:sz', str(size)), ('w:space', '1'), ('w:color', color)):
        b.set(qn(k), v)
    bdr.append(b)
    pPr.append(bdr)


def section(doc, title):
    p = para(doc, before=7, after=2, keep_next=True)
    style_run(p.add_run(title), size=11.5, bold=True, color=ACCENT, caps=True)
    bottom_border(p)


def bullet(doc, text, lead=None):
    p = para(doc, after=1, line=1.0)
    pf = p.paragraph_format
    pf.left_indent, pf.first_line_indent = Inches(0.18), Inches(-0.14)
    style_run(p.add_run('•  '), color=ACCENT)
    if lead:
        style_run(p.add_run(lead + ': '), bold=True)
    style_run(p.add_run(text))


def build(out):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.left_margin = sec.right_margin = Inches(0.6)
    sec.top_margin = sec.bottom_margin = Inches(0.5)
    normal = doc.styles['Normal']
    normal.font.name, normal.font.size = FONT, Pt(BODY_PT)

    style_run(para(doc, align=WD_ALIGN_PARAGRAPH.CENTER).add_run(NAME), size=22, bold=True, color=ACCENT)
    style_run(para(doc, before=2, align=WD_ALIGN_PARAGRAPH.CENTER).add_run(HEADLINE), size=11.5, bold=True)
    p = para(doc, before=2, after=2, align=WD_ALIGN_PARAGRAPH.CENTER)
    style_run(p.add_run(CONTACT), size=10, color=MUTED)
    bottom_border(p, size=12)

    section(doc, 'Executive Summary')
    for i, s in enumerate(SUMMARY):
        style_run(para(doc, after=3 if i == 0 else 1, line=1.05).add_run(s))

    section(doc, 'Selected Leadership Results')
    for lead, text in RESULTS:
        bullet(doc, text, lead)

    section(doc, 'Core Expertise')
    style_run(para(doc, after=1, line=1.1).add_run('  |  '.join(EXPERTISE)))

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

    section(doc, 'Technology & Program Innovation')
    for lead, text in INNOVATION:
        bullet(doc, text, lead)

    section(doc, 'Education')
    for degree, school, year in EDUCATION:
        p = para(doc, after=1)
        p.paragraph_format.tab_stops.add_tab_stop(RIGHT_TAB, WD_TAB_ALIGNMENT.RIGHT)
        style_run(p.add_run(degree), bold=True)
        style_run(p.add_run(f'  |  {school}'))
        if year:
            style_run(p.add_run('\t' + year))

    doc.core_properties.title = 'Clavel Lazarre, MBA — Executive Resume'
    doc.core_properties.author = 'Clavel Lazarre'
    doc.save(out)
    print(out)


if __name__ == '__main__':
    build(sys.argv[1])

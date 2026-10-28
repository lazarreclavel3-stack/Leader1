"""Executive leadership resume (Clavel's own text, Oct 2026) in the approved gold/black format.

Usage: python3 resumes/build_executive.py out.docx
Reuses the XML helpers and template from jobsearch/build_resume.py.
"""
import os
import sys
import zipfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'jobsearch'))
import build_resume as br  # noqa: E402
from build_resume import p, run, heading, tbl, stat_cell, GOLD, DARK, BODY, GREY  # noqa: E402

SZ = 18          # body size (half-points)
LINE = 228       # exact line height for bullets (twips)


def bullet(text, lead=None):
    runs = run('• ', GOLD, SZ)
    if lead:
        runs += run(lead + ': ', DARK, SZ, b=True)
    runs += run(text, BODY, SZ)
    return p(runs, f'<w:spacing w:before="14" w:after="14" w:lineRule="exact" w:line="{LINE}"/>'
                   '<w:ind w:left="187" w:hanging="187"/>')


def job(org, loc, title, dates, summary, bullets):
    def cell(inner, w):
        return f'<w:tc><w:tcPr><w:tcW w:type="dxa" w:w="{w}"/></w:tcPr>{inner}</w:tc>'
    row = ('<w:tr>'
           + cell(p(run(org, DARK, 19, b=True) + run(f'  |  {loc}', GREY, 17),
                    '<w:keepNext/><w:spacing w:before="90" w:after="0"/>'), 7368)
           + cell(p(run(dates, GOLD, 18, b=True),
                    '<w:keepNext/><w:spacing w:before="90" w:after="0"/><w:jc w:val="right"/>'), 3000)
           + '</w:tr>')
    out = tbl('left', [7368, 3000], [row])
    out += p(run(title, DARK, 18, i=True), '<w:keepNext/><w:spacing w:before="0" w:after="20"/>')
    if summary:
        out += p(run(summary, GREY, 17, i=True),
                 '<w:keepNext/><w:spacing w:before="0" w:after="30" w:lineRule="exact" w:line="220"/>')
    return out + ''.join(bullet(b) for b in bullets)


def body():
    o = [
        p(run('CLAVEL LAZARRE', DARK, 46, b=True) + run(',  MBA', GOLD, 26),
          '<w:spacing w:before="0" w:after="30"/><w:jc w:val="center"/>'),
        p(run('EXECUTIVE LEADERSHIP  ·  ORGANIZATIONAL GROWTH  ·  STRATEGY & OPERATIONS', GOLD, 17, b=True),
          '<w:spacing w:before="0" w:after="30"/><w:jc w:val="center"/>'),
        p(run('New York, NY  |  347-607-8164  |  lazarreclavel3@gmail.com  |  linkedin.com/in/clavel-lazarre', GREY, 17),
          '<w:spacing w:before="0" w:after="60"/><w:jc w:val="center"/>'),
        p('', '<w:spacing w:before="0" w:after="60"/><w:pBdr><w:bottom w:val="single" w:sz="8" '
              'w:space="1" w:color="C09628"/></w:pBdr>'),
        heading('EXECUTIVE PROFILE'),
        p(run('Operations and finance executive with more than 20 years of experience building businesses, leading '
              'mission-driven programs, and creating the systems organizations need to grow. Held full P&L accountability '
              'for an $80M portfolio and financial and operational oversight of a 140-person division. Co-founded a fitness '
              'business that reached $1M in annual revenue within 24 months, then expanded through a franchise model to $10M '
              'in annual sales, with HR, payroll, and benefits infrastructure supporting 50+ employees.', BODY, 18),
          '<w:spacing w:before="20" w:after="50" w:lineRule="exact" w:line="236"/><w:jc w:val="both"/>'),
        p(run('Brings a founder’s understanding of growth and an operator’s discipline in execution. Partners with CEOs, '
              'boards, public agencies, and community organizations to evaluate opportunities, align resources, and translate '
              'strategy into budgets, partnerships, programs, and operating processes. Experience spans workforce development, '
              'social enterprise, financial advisory, logistics, and practical AI implementation.', BODY, 18),
          '<w:spacing w:before="0" w:after="60" w:lineRule="exact" w:line="236"/><w:jc w:val="both"/>'),
        tbl('center', [2592] * 4, [
            '<w:tr>' + ''.join(stat_cell(a, GOLD, 30, True, 'w:before="80" w:after="30"')
                               for a in ['$80M', '140', '300+', '$200M']) + '</w:tr>',
            '<w:tr>' + ''.join(stat_cell(b, DARK, 15, False, 'w:before="40" w:after="80"')
                               for b in ['P&L portfolio led', 'Person division overseen',
                                         'Participants served annually', 'Banking initiative structured']) + '</w:tr>']),
        heading('SELECTED LEADERSHIP RESULTS'),
        bullet('Grew Fitness Collective from a $5,000 investment, established a franchise model, and launched three additional locations.', 'Built and expanded a business'),
        bullet('Oversaw a 140-person division at Osborne Association, connecting financial accountability, workforce development, partnerships, and service delivery.', 'Led at substantial scale'),
        bullet('Led a nine-month transitional-employment program serving 300+ formerly incarcerated people annually; created and delivered an NYPA clean-energy workforce project over 18 months.', 'Created mission-driven programs'),
        bullet('Reduced vendor costs 35% and processing time 60% at Alluel through negotiations and systems improvements.', 'Improved operating performance'),
        heading('CORE EXPERTISE'),
        p(run('  •  '.join(['Organizational Growth', 'General Management', 'P&L Leadership', 'Budgeting & Resource Allocation',
                            'CEO & Board Partnership', 'People Operations', 'Program Development', 'Coalition Building',
                            'Fundraising & Grant Stewardship', 'Risk Management', 'Performance Reporting',
                            'Technology & Process Improvement']), BODY, 17),
          '<w:spacing w:before="20" w:after="40" w:lineRule="exact" w:line="230"/><w:jc w:val="center"/>'),
        heading('PROFESSIONAL EXPERIENCE'),
        job('MAROON STRATEGIST, LLC', 'Brooklyn, NY', 'Chief Financial Strategy Officer', 'Mar 2024–Present',
            'Fractional CFO and program leadership across nonprofit, public-sector, education, healthcare, personal services, '
            'tax advisory, event planning, and other business operations.', [
                'Created and led the NYPA clean-energy workforce training project from inception through final delivery over 18 months, overseeing proposal development, program design, budgeting, partner coordination, and participant training.',
                'Built a workforce coalition spanning city and state agencies, elected officials, academic partners, Stanford Innovation Lab, KPMG, and the New York Power Authority, coordinating responsibilities and resources around energy training.',
                'Developed and managed a multimillion-dollar project budget, allocating direct and indirect costs, managing restricted cash flow, and aligning expenditures with grant requirements and delivery milestones.',
                'Led fundraising and partnership-agreement development, connecting funding commitments, partner responsibilities, and implementation needs.',
                'Direct budgeting, forecasting, cash management, and multi-entity financial planning; advise leaders on financing, working capital, and growth priorities.',
                'Build financial models, KPI dashboards, and SOPs; coordinate financial cleanup and reporting remediation with clients, accountants, and stakeholders.']),
        job('OSBORNE ASSOCIATION', 'New York, NY', 'Vice President, Business Development & Social Ventures', 'Jan 2023–Oct 2025',
            'Financial and operational oversight of a 140-person division in a human-services organization supporting people '
            'affected by the criminal legal system.', [
                'Held full P&L accountability for an $80M portfolio, aligning budgets, staffing, partnerships, and program priorities.',
                'Partnered with the CEO and Board on long-range planning, risk management, resource allocation, and organizational growth.',
                'Led a nine-month transitional-employment program serving 300+ formerly incarcerated people annually, coordinating employer partnerships and tracking outcomes against funder benchmarks.',
                'Negotiated government, corporate, and philanthropic partnerships and developed earned-income social ventures to support mission delivery.',
                'Authored a strategic growth and feasibility white paper on a potential Rikers Island service contract, integrating financial modeling, workforce needs, mission alignment, employee well-being, and operational risk.',
                'Developed a roadmap for potentially doubling JMS within 12 months, identifying investments in management capacity, recruitment, training, contract oversight, payroll, compliance, and technology.',
                'Oversaw departmental talent acquisition, onboarding, staff development, and performance management.']),
        job('ALLUEL LOGISTICS', 'New York, NY', 'Vice President of Operations', 'Nov 2021–Aug 2022', None, [
                'Managed a $2M operating budget and renegotiated vendor agreements, reducing supply-chain and logistics costs 35%.',
                'Implemented warehouse-management technology that cut data-processing time 60%; introduced CRM systems and trained staff.',
                'Oversaw NYCHA logistics contracts serving 100 developments and supervised ~$500K in monthly NYC DHS billing.',
                'Recruited and managed field, sales, and administrative staff; improved HR workflows and data accuracy.']),
        job('LAZARRE CONSULTING GROUP', 'New York, NY', 'Chief Executive Officer', 'Dec 2016–Present', None, [
                'Served as financial architect for a $200M national banking development initiative, supporting capital planning and financial structuring.',
                'Developed operating and performance-improvement strategies for organizations and brands including American Express OPEN, Ogilvy, and Chubb.',
                'Led financial remediation for a psychological services practice, identifying ~$251K in unclaimed deductions and preparing corrected financial statements.']),
        job('FITNESS COLLECTIVE INC.', 'Brooklyn, NY', 'CEO and Co-Founder', '2004–2016', None, [
                'Scaled from a $5,000 investment to $1M in annual revenue within 24 months, then implemented a franchise model and launched three additional locations, growing to $10M in annual sales.',
                'Built HR, payroll, and benefits infrastructure for 50+ employees, overseeing recruitment, training, performance management, and ~$65K in monthly payroll.',
                'Implemented Mindbody CRM for client tracking, online booking, and targeted engagement across 4,000+ clients; established a training academy that certified 25 trainers.',
                'Developed local business partnerships, cross-marketing initiatives, and community events; negotiated vendor and utility agreements.']),
        heading('TECHNOLOGY & PROGRAM INNOVATION'),
        bullet('Built an AI-supported workflow connecting opportunity research, evaluation, document preparation, and reporting, with evidence validation, cost controls, and performance tracking.', 'SkyNet'),
        bullet('Designed and submitted a Citi Foundation proposal connecting AI learning, workforce preparation, and employment support, with measures for skills, employment, wages, and retention.', 'JWA AI Career Launch'),
        heading('EDUCATION'),
        p(run('Master of Business Administration, General Business Management', DARK, 18, b=True)
          + run('  |  West Texas A&M University  |  2023', BODY, 18), '<w:spacing w:before="10" w:after="10"/>'),
        p(run('Bachelor of Science, Small Business Administration', DARK, 18, b=True)
          + run('  |  Northern Arizona University', BODY, 18), '<w:spacing w:before="10" w:after="10"/>'),
    ]
    return ''.join(o)


def build(out_path):
    with zipfile.ZipFile(br.TEMPLATE) as zin, zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == 'docProps/thumbnail.jpeg':
                continue
            data = zin.read(item.filename)
            if item.filename == 'word/document.xml':
                x = data.decode('utf-8')
                head = x[:x.find('<w:body>') + len('<w:body>')]
                sect = x[x.find('<w:sectPr'):]
                sect = sect.replace('w:top="792" w:right="936" w:bottom="792" w:left="936"',
                                    'w:top="648" w:right="864" w:bottom="648" w:left="864"')
                data = (head + body() + sect).encode('utf-8')
            elif item.filename == '[Content_Types].xml':
                x = data.decode('utf-8')
                i = x.find('<Override PartName="/docProps/thumbnail.jpeg"')
                if i >= 0:
                    x = x[:i] + x[x.find('/>', i) + 2:]
                data = x.encode('utf-8')
            elif item.filename == '_rels/.rels':
                x = data.decode('utf-8')
                i = x.find('thumbnail')
                if i >= 0:
                    a = x.rfind('<Relationship ', 0, i)
                    x = x[:a] + x[x.find('/>', i) + 2:]
                data = x.encode('utf-8')
            zout.writestr(item, data)
    print(out_path)


if __name__ == '__main__':
    build(sys.argv[1])

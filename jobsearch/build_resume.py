"""Build a tailored resume (.docx) in the approved gold/black format from a JSON spec.

Usage:
    python3 build_resume.py spec.json out.docx [--pdf]

Every bullet in the spec must cite evidence IDs from career_database.xlsx
("Career Evidence" sheet). The build fails if an ID is missing or unknown,
so nothing reaches a resume that isn't backed by the database.

Spec shape (see base_cfo.json):
{
  "tagline": "...",
  "profile": "...",
  "stats": [["$1M → 13%", "Deficit reversed to surplus"], ... 4 items],
  "capabilities": ["...", ...],
  "sections": [
    {"heading": "PROFESSIONAL EXPERIENCE", "jobs": [
      {"org": "...", "title": "...", "dates": "...", "location": "...",
       "bullets": [{"text": "...", "evidence": ["E012"]}, ...]}
    ]}
  ],
  "education": ["...", ...],
  "technology": "..."
}
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from xml.sax.saxutils import escape as E

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, 'template.docx')
DB = os.path.join(HERE, 'career_database.xlsx')

GOLD, DARK, BODY, GREY = 'C09628', '1C1C1C', '3A3A3A', '555555'


def load_evidence_ids():
    import openpyxl
    ws = openpyxl.load_workbook(DB, data_only=True)['Career Evidence']
    return {str(r[0]).strip() for r in ws.iter_rows(min_row=2, values_only=True) if r[0]}


def rpr(color, sz, b=False, i=False):
    return ('<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>'
            + ('<w:b/>' if b else '<w:b w:val="0"/>')
            + ('<w:i/>' if i else '<w:i w:val="0"/>')
            + f'<w:color w:val="{color}"/><w:sz w:val="{sz}"/></w:rPr>')


def run(t, color, sz, b=False, i=False):
    return f'<w:r>{rpr(color, sz, b, i)}<w:t xml:space="preserve">{E(t)}</w:t></w:r>'


def p(runs, ppr):
    return f'<w:p><w:pPr>{ppr}</w:pPr>{runs}</w:p>'


RULE_PPR = ('<w:keepNext/><w:spacing w:before="120" w:after="40"/><w:pBdr><w:bottom w:val="single" '
            'w:sz="8" w:space="1" w:color="C09628"/></w:pBdr>')
NO_BORDERS = ''.join(f'<w:{s} w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
                     for s in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV'])


def tbl(jc, cols, rows):
    grid = ''.join(f'<w:gridCol w:w="{c}"/>' for c in cols)
    return ('<w:tbl><w:tblPr><w:tblW w:type="auto" w:w="0"/><w:tblLook w:firstColumn="1" w:firstRow="1" '
            'w:lastColumn="0" w:lastRow="0" w:noHBand="0" w:noVBand="1" w:val="04A0"/>'
            f'<w:jc w:val="{jc}"/><w:tblBorders>{NO_BORDERS}</w:tblBorders></w:tblPr>'
            f'<w:tblGrid>{grid}</w:tblGrid>{"".join(rows)}</w:tbl>')


def heading(t):
    return (p('', RULE_PPR)
            + p(run(t, GOLD, 19, b=True), '<w:keepNext/><w:spacing w:before="0" w:after="60"/><w:ind w:left="0"/>'))


def bullet(t):
    return p(run('• ', GOLD, 18) + run(t, BODY, 18),
             '<w:spacing w:before="20" w:after="20" w:lineRule="exact" w:line="230"/>'
             '<w:ind w:left="187" w:hanging="187"/>')


def job(j):
    def cell(inner):
        return f'<w:tc><w:tcPr><w:tcW w:type="dxa" w:w="5184"/></w:tcPr>{inner}</w:tc>'
    row = ('<w:tr>'
           + cell(p(run(f'{j["org"]}  |  {j["title"]}', DARK, 19, b=True),
                    '<w:keepNext/><w:spacing w:before="100" w:after="20"/>'))
           + cell(p(run(j['dates'], GOLD, 18),
                    '<w:keepNext/><w:spacing w:before="100" w:after="20"/><w:jc w:val="right"/>'))
           + '</w:tr>')
    return (tbl('left', [5184, 5184], [row])
            + p(run(j['location'], GREY, 17, i=True), '<w:keepNext/><w:spacing w:before="0" w:after="40"/>')
            + ''.join(bullet(b['text']) for b in j['bullets']))


def plain(t):
    return p(run(t, BODY, 18), '<w:spacing w:before="20" w:after="20" w:lineRule="exact" w:line="240"/>')


def stat_cell(t, fill, sz, b, spacing):
    return ('<w:tc><w:tcPr><w:tcW w:type="dxa" w:w="2592"/>'
            f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/><w:vAlign w:val="center"/></w:tcPr>'
            + p(run(t, 'FFFFFF', sz, b=b), f'<w:spacing {spacing}/><w:jc w:val="center"/>') + '</w:tc>')


def validate(spec, known_ids):
    errors = []
    if len(spec['stats']) != 4:
        errors.append('stats must have exactly 4 items')
    for s in spec['sections']:
        for j in s['jobs']:
            for b in j['bullets']:
                ev = b.get('evidence') or []
                if not ev:
                    errors.append(f'No evidence cited: {b["text"][:70]}')
                for e in ev:
                    if e not in known_ids:
                        errors.append(f'Unknown evidence ID {e}: {b["text"][:70]}')
    if errors:
        sys.exit('Spec failed evidence check:\n  ' + '\n  '.join(errors))


def body_xml(spec):
    out = [
        p(run('CLAVEL M. LAZARRE', DARK, 48, b=True) + run(',  MBA', GOLD, 26),
          '<w:spacing w:before="0" w:after="40"/><w:jc w:val="center"/>'),
        p(run(spec['tagline'], GOLD, 17), '<w:spacing w:before="20" w:after="40"/><w:jc w:val="center"/>'),
        p(run(spec.get('contact', 'Brooklyn, NY  |  347-607-8164  |  lazarreclavel3@gmail.com'), GREY, 18),
          '<w:spacing w:before="20" w:after="80"/><w:jc w:val="center"/>'),
        p('', '<w:spacing w:before="0" w:after="120"/><w:pBdr><w:bottom w:val="single" w:sz="8" '
              'w:space="1" w:color="C09628"/></w:pBdr>'),
        heading('EXECUTIVE PROFILE'),
        p(run(spec['profile'], BODY, 19), '<w:spacing w:before="40" w:after="80" w:lineRule="exact" w:line="250"/>'),
        heading(spec.get('stats_heading', 'SELECTED IMPACT')),
        tbl('center', [2592] * 4, [
            '<w:tr>' + ''.join(stat_cell(a, GOLD, 32, True, 'w:before="100" w:after="40"')
                               for a, _ in spec['stats']) + '</w:tr>',
            '<w:tr>' + ''.join(stat_cell(b, DARK, 15, False, 'w:before="60" w:after="100"')
                               for _, b in spec['stats']) + '</w:tr>']),
        heading('CORE LEADERSHIP CAPABILITIES'),
        p(run('  •  '.join(spec['capabilities']), BODY, 17),
          '<w:spacing w:before="40" w:after="80" w:lineRule="exact" w:line="240"/><w:jc w:val="center"/>'),
    ]
    for s in spec['sections']:
        out.append(heading(s['heading']))
        out.extend(job(j) for j in s['jobs'])
    out.append(heading('EDUCATION AND CREDENTIALS'))
    out.extend(plain(e) for e in spec['education'])
    if spec.get('technology'):
        out.append(heading('TECHNOLOGY'))
        out.append(p(run(spec['technology'], BODY, 18), '<w:spacing w:before="20" w:after="40"/>'))
    return ''.join(out)


def build(spec_path, out_path, pdf=False):
    spec = json.load(open(spec_path))
    validate(spec, load_evidence_ids())
    with zipfile.ZipFile(TEMPLATE) as zin, zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == 'docProps/thumbnail.jpeg':
                continue
            data = zin.read(item.filename)
            if item.filename == 'word/document.xml':
                x = data.decode('utf-8')
                head = x[:x.find('<w:body>') + len('<w:body>')]
                sect = x[x.find('<w:sectPr'):]
                data = (head + body_xml(spec) + sect).encode('utf-8')
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
    if pdf:
        outdir = os.path.dirname(os.path.abspath(out_path))
        subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', outdir, out_path],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(out_path)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) != 2:
        sys.exit(__doc__)
    build(args[0], args[1], pdf='--pdf' in sys.argv)

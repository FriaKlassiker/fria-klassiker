#!/usr/bin/env python3
"""Publish curated EPUB/PDF uploads as Fria klassiker reader pages.

The uploaded EPUB, rather than generated Markdown, is authoritative for the
website rendering. This preserves passage numbering, italics and tables.
The PDF and EPUB download files are never rewritten by this helper.

Run after build.py --bara-site and before/after enhance_site.py.
"""
from __future__ import annotations
import html
import json
import re
from pathlib import Path
from zipfile import ZipFile
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
CFG = json.loads((ROOT / 'config.json').read_text(encoding='utf-8'))
REPO = 'https://github.com/FriaKlassiker/fria-klassiker'
PAGES = 'https://friaklassiker.github.io/fria-klassiker/'


def xml_section(zipfile: ZipFile, chunk: str) -> BeautifulSoup:
    soup = BeautifulSoup(zipfile.read('EPUB/text/' + chunk + '.xhtml'), 'xml')
    section = soup.find('body').find('section')
    if section is None:
        raise ValueError(f'EPUB missing section in {chunk}')
    return section


def inner_markup(section, skip_heading=True) -> str:
    return ''.join(str(x) for x in section.contents
                   if getattr(x, 'name', None) != 'h1' or not skip_heading)


def reference_markdown(z: ZipFile) -> str:
    """Create a searchable plain-text source alongside the original EPUB."""
    sect = xml_section(z, 'ch003')
    out = []
    for e in sect.find_all(['h2', 'p', 'table']):
        if e.name == 'h2':
            label = e.get_text(' ', strip=True)
            out.append(f'### {label}')
        elif e.name == 'p':
            p = BeautifulSoup(str(e), 'html.parser').p
            mark = p.select_one('.steph')
            if mark:
                out.append('## ' + mark.get_text(strip=True))
                mark.extract()
            value = p.get_text('', strip=True)
            if value:
                out.append(value)
        elif e.name == 'table':
            rows = []
            for tr in e.find_all('tr'):
                cells = [cell.get_text(' ', strip=True) for cell in tr.find_all(['td', 'th'])]
                if cells:
                    rows.append('| ' + ' | '.join(cells) + ' |')
            if rows:
                ncols = len(e.find('tr').find_all(['td','th']))
                out.extend([rows[0], '| '+ ' | '.join(['---'] * ncols) + ' |', *rows[1:]])
        out.append('')
    return '\n'.join(out).strip() + '\n'


def make_page(book, header, alert, footer, toolbar):
    ident = book['id']
    epub = SITE / 'nedladdning' / (ident + '-granskning.epub')
    pdf = SITE / 'nedladdning' / (ident + '-granskning.pdf')
    if not epub.is_file() or not pdf.is_file():
        raise FileNotFoundError(f'Missing download files for {ident}')
    with ZipFile(epub) as z:
        assert z.testzip() is None, f'EPUB corrupt: {epub}'
        notice = xml_section(z,'ch001')
        intro = xml_section(z,'ch002')
        full = xml_section(z,'ch003')
        colophon = xml_section(z,'ch004')
        chapters = full.find_all('h2')
        if not chapters:
            raise ValueError(f'No chapter headings in {epub}')
        for i, heading in enumerate(chapters, 1):
            heading['id'] = f'{ident}-del-{i}'
        if ident == 'sjalvbetraktelser' and len(chapters) != 12:
            raise ValueError('Självbetraktelser should contain twelve books')
        # Keep source text in a readable, separately versioned plain-text file.
        md = ROOT / 'texter' / (ident + '.md')
        md.write_text('# '+ book['forfattare']+ ': '+book['titel']+ '\n\n'
                      '> AI-översättning. Granskningsexemplar. Svenskt källtextutdrag ur den uppladdade EPUB-utgåvan.\n\n'
                      + reference_markdown(z), encoding='utf-8')
        nav = ''.join(f'<a href="#{ident}-del-{i}">{html.escape(h.get_text(" ",strip=True))}</a>'
                      for i,h in enumerate(chapters,1))
        content = f'''<!doctype html><html lang="sv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(book['forfattare'])}: {html.escape(book['titel'])} – Fria klassiker</title>
<meta name="description" content="{html.escape(book['ingress'],quote=True)}">
<link rel="icon" href="../assets/brand-mark.svg" type="image/svg+xml">
<link rel="stylesheet" href="../stil.css"><link rel="stylesheet" href="../portal.css"><script defer src="../portal.js"></script></head>
<body class="reader-page imported-edition">{alert()}{header('../')}
<main class="reader-main"><a class="reader-crumb" href="../index.html#bibliotek">← Till biblioteket</a>
<h1>{html.escape(book['titel'])}</h1><p class="noindent forf">{html.escape(book['forfattare'])} · översatt från grekiskan med AI</p>
{toolbar(ident)}
<div class="ai"><h2>Om den här översättningen</h2>{inner_markup(notice)}</div>
<section aria-label="Inledning"><h2>Inledning</h2>{inner_markup(intro)}</section>
<nav class="tankarnav" aria-label="Gå till kapitel eller bok">{nav}</nav>
<section aria-label="Texten">{inner_markup(full)}</section>
<h2 id="kolofon">Om utgåvan</h2><div class="kolofon">{inner_markup(colophon)}</div>
</main>{footer('../')}</body></html>'''
        # Correct legacy placeholder links in browser views only; do not touch
        # the user-supplied PDF/EPUB bytes, which are retained verbatim.
        content = content.replace('https://github.com/ANVANDARNAMN/fria-klassiker', REPO)
        content = content.replace('https://ANVANDARNAMN.github.io/fria-klassiker/', PAGES)
        (SITE / 'verk' / (ident + '.html')).write_text(content, encoding='utf-8')
        print(f'Updated {ident}: {len(chapters)} parts; {len(content)} HTML characters')


if __name__ == '__main__':
    # Import lazily to avoid circular imports: enhance_site owns the theme.
    import enhance_site as theme
    for item in CFG.get('importerade_verk', []):
        make_page(item, theme.header, theme.alert, theme.footer, theme.book_toolbar)

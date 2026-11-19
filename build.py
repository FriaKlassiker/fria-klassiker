#!/usr/bin/env python3
"""Bygger EPUB, PDF och webbplats för Fria klassiker.

  python3 build.py            # allt
  python3 build.py --bara-site

Kräver pandoc (>= 3), xelatex (TeX Live med KOMA-Script och TeX Gyre) och Pillow.
Ändra uppgifter (granskad, ISBN, utgivare, adresser) i config.json.
"""
import html, json, re, shutil, subprocess, sys
from pathlib import Path

ROT = Path(__file__).resolve().parent
CFG = json.loads((ROT / 'config.json').read_text(encoding='utf-8'))
UT = ROT / 'site'
NED = UT / 'nedladdning'
BYGG = ROT / '_bygg'
VERK = {v['id']: v for v in CFG['verk']}
sys.path.insert(0, str(ROT))
import fragment  # noqa: E402


# ---------- text ----------------------------------------------------------

def md_escape_start(rad):
    m = re.match(r'(\d+)([.)]\s)', rad)
    if m:
        return m.group(1) + '\\' + rad[len(m.group(1)):]
    if rad[:1] in '#*+>|':
        return '\\' + rad
    return rad


def text_till_md(verk):
    """Källfilen har en rad per stycke och '## N' för Stephanus-sidor eller kapitel."""
    rader = (ROT / 'texter' / verk['fil']).read_text(encoding='utf-8').splitlines()
    ut, vantande = [], None
    for rad in rader:
        rad = rad.strip()
        if not rad:
            continue
        m = re.fullmatch(r'##\s*(\d+)', rad)
        if m:
            if verk['refsystem'] == 'kapitel':
                ut.append(f'## {m.group(1)} {{#{verk["id"]}-{m.group(1)} .unnumbered}}')
            else:
                vantande = m.group(1)
            continue
        if re.fullmatch(r'\[.*\]', rad):
            rad = '*\\[' + rad[1:-1] + '\\]*'
        else:
            s = re.match(r'([A-ZÅÄÖ]{3,}):\s+(.*)', rad)
            if s:
                rad = f'[{s.group(1).capitalize()}:]{{.smallcaps}} {s.group(2)}'
            else:
                rad = md_escape_start(rad)
        if vantande:
            rad = f'[{vantande}]{{.steph}}' + rad
            vantande = None
        ut.append(rad)
    return '\n\n'.join(ut) + '\n'


# ---------- förtext och kolofon -------------------------------------------

def grek_span(t):
    return re.sub(r'[\u0370-\u03FF\u1F00-\u1FFF][\u0370-\u03FF\u1F00-\u1FFF\s]*[\u0370-\u03FF\u1F00-\u1FFF]',
                  lambda m: '[' + m.group(0) + ']{.gr}', t)


def granskningsmening():
    if CFG['granskad']:
        return f'Översättningen har lästs igenom och redigerats av {CFG["granskare"]}.'
    return '**Detta är ett granskningsexemplar. Texten har ännu inte granskats av en människa.**'


def M(v, nyckel):
    """Uppgift per verk, med seriens värde som standard (modell, modelltillverkare, oversattningsmanad)."""
    return v.get(nyckel) or CFG[nyckel]


def modellnamn(v):
    return f'{M(v, "modell")} ({M(v, "modelltillverkare")})'


def ai_text(verk_lista):
    v0 = verk_lista[0]
    if v0.get('ai_metod'):
        metod = v0['ai_metod'].format(modell=modellnamn(v0), manad=M(v0, 'oversattningsmanad'))
    else:
        eng = '; '.join(sorted({v['engelska'] for v in verk_lista}))
        metod = (f'Texten har översatts direkt från grekiskan av språkmodellen {modellnamn(v0)} '
                 f'i {M(v0, "oversattningsmanad")}. '
                 f'Som stöd för förståelsen användes en äldre engelsk översättning ({eng}).')
    kontakt = (f'till {CFG["kontakt_epost"]} eller via ' if CFG.get("kontakt_epost") else 'via ')
    return (
        '**Det här är en AI-översättning.** ' + metod + f' {granskningsmening()}\n\n'
        'En AI-översättning kan innehålla fel: en mening kan vara feltolkad, en nyans kan ha gått förlorad '
        'eller en bisats ha fallit bort. Den ersätter inte en vetenskaplig utgåva. '
        f'Hittar du ett fel, hör gärna av dig {kontakt}{CFG["repo_url"]}/issues.\n'
    )


def hanvisning(verk_lista):
    s = set(v['refsystem'] for v in verk_lista)
    delar = []
    if 'stephanus' in s:
        delar.append('Siffrorna i marginalen anger sidorna i Henri Estiennes (Stephanus) utgåva av Platon från 1578, '
                     'det system som används för att hänvisa till Platons texter i alla språk.')
    if 'kapitel' in s:
        delar.append('Kapitelindelningen följer den vedertagna numreringen av Handboken.')
    return ' '.join(delar)


def kolofon(titel, forf, verk_lista, isbn_epub, isbn_pdf):
    v0 = verk_lista[0]
    orig = '; '.join(f'{v["titel"]}: {grek_span(v["originaltitel"])}' for v in verk_lista)
    isbn = ' · '.join(x for x in [f'ISBN {isbn_epub} (EPUB)' if isbn_epub else '',
                                   f'ISBN {isbn_pdf} (PDF)' if isbn_pdf else ''] if x)
    if v0.get('kolofon_kallor'):
        kallor = list(v0['kolofon_kallor'])
    else:
        kallor = [f'Grekisk text: {"; ".join(sorted({v["grekiska"] for v in verk_lista}))}.',
                  f'Engelsk stödöversättning: {"; ".join(sorted({v["engelska"] for v in verk_lista}))}.']
    licens_kalla = v0.get('licens_kalla', 'Den grekiska texten kommer från Perseus Digital Library, Tufts University, under samma licens.')
    rader = [
        f'{forf}: *{titel}*. Originalets titel: {orig}.',
        f'Översättning: språkmodellen {modellnamn(v0)}, {M(v0, "oversattningsmanad")}. '
        + ('Granskning och redigering: ' + CFG['granskare'] + '.' if CFG['granskad'] else 'Granskningsexemplar, ännu inte granskat av en människa.'),
        *kallor,
        f'{CFG["serie"]}, utgåva {CFG["version"]}, {CFG["datum"]}. Utgivare: {CFG["utgivare"]}.' + (f' {isbn}.' if isbn else ''),
        'Licens: Creative Commons Erkännande-DelaLika 4.0 Internationell (CC BY-SA 4.0), '
        'https://creativecommons.org/licenses/by-sa/4.0/deed.sv. Du får kopiera, sprida och bearbeta texten, '
        'även kommersiellt, om du anger källan och delar vidare under samma licens. ' + licens_kalla,
        f'Senaste version och rättelser: {CFG["site_url"]}' + (f' · DOI {CFG["doi"]}' if CFG['doi'] else ''),
    ]
    return '\n\n'.join(rader) + '\n'


def verk_md(v, niva):
    """Själva texten. Fragmentsamlingar ger ett kapitel per tänkare plus bilagor."""
    if v.get('typ') == 'fragment':
        return fragment.delar_md(v, fragment.ladda(ROT / 'texter' / v['fil']), niva, grek_span)
    return text_till_md(v)


def inledning(v_lista, ingress):
    v0 = v_lista[0]
    if v0.get('typ') == 'fragment' and len(v_lista) == 1:
        return fragment.inledning_md(v0, fragment.ladda(ROT / 'texter' / v0['fil']))
    return '::: ingress\n' + ingress + '\n:::\n\n' + hanvisning(v_lista) + '\n'


def bok_md(bok_id, titel, forf, verk_lista, ingress, isbn_epub, isbn_pdf, fmt):
    """Hela boken som markdown. fmt = 'epub' | 'pdf'."""
    d = []
    d.append('# Om den här översättningen {.unnumbered}\n\n::: ai\n' + ai_text(verk_lista) + ':::\n')
    d.append('# Inledning {.unnumbered}\n\n' + inledning(verk_lista, ingress))
    samling = len(verk_lista) > 1
    for v in verk_lista:
        if v.get('typ') == 'fragment':
            d.append(verk_md(v, 1))
            continue
        d.append(f'# {v["titel"]} {{#{v["id"]} .unnumbered}}\n')
        if samling:
            d.append('::: ingress\n' + v['ingress'] + '\n:::\n')
        d.append(verk_md(v, 1))
    d.append('# Kolofon {.unnumbered}\n\n::: kolofon\n' + kolofon(titel, forf, verk_lista, isbn_epub, isbn_pdf) + ':::\n')
    return '\n'.join(d)


# ---------- omslag ---------------------------------------------------------

def omslag(bok_id, titel, forf, ut, rad='Översatt från grekiskan'):
    from PIL import Image, ImageDraw, ImageFont
    font = str(ROT / 'mallar/fonts/Cardo-Regular.ttf')
    fonti = str(ROT / 'mallar/fonts/Cardo-Italic.ttf')
    if not Path(font).exists():
        import glob
        font = fonti = (glob.glob('/usr/share/fonts/**/DejaVuSerif.ttf', recursive=True) or [None])[0]
    W, H = 1600, 2560
    img = Image.new('RGB', (W, H), (246, 241, 232))
    dr = ImageDraw.Draw(img)
    rod = (122, 46, 31)
    dr.rectangle([90, 90, W - 90, H - 90], outline=rod, width=6)
    dr.rectangle([115, 115, W - 115, H - 115], outline=rod, width=2)

    def centrera(txt, y, storlek, f=font, farg=(31, 29, 26)):
        F = ImageFont.truetype(f, storlek)
        while dr.textlength(txt, font=F) > W - 320 and storlek > 40:
            storlek -= 6
            F = ImageFont.truetype(f, storlek)
        dr.text(((W - dr.textlength(txt, font=F)) / 2, y), txt, font=F, fill=farg)
        return y + storlek * 1.25

    centrera(CFG['serie'].upper(), 300, 64, farg=rod)
    y = centrera(forf, 820, 110)
    ord_ = titel.split()
    rader, akt = [], ''
    for o in ord_:
        test = (akt + ' ' + o).strip()
        if len(test) > 12 and akt:
            rader.append(akt); akt = o
        else:
            akt = test
    rader.append(akt)
    y += 40
    for r in rader:
        y = centrera(r, y, 190)
    dr.line([(W / 2 - 160, y + 70), (W / 2 + 160, y + 70)], fill=rod, width=4)
    centrera(rad, H - 620, 64, f=fonti)
    centrera('AI-översättning', H - 520, 64, f=fonti, farg=rod)
    if not CFG['granskad']:
        centrera('GRANSKNINGSEXEMPLAR', H - 330, 56, farg=(150, 110, 0))
    img.save(ut, quality=90)


# ---------- bygg böcker ----------------------------------------------------

def pandoc(*args):
    r = subprocess.run(['pandoc', *args], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr)
    if r.stderr.strip():
        print(r.stderr.strip()[:800])


def bocker():
    lista = [(v['id'], v['titel'], v['forfattare'], [v], v['ingress'], v['isbn_epub'], v['isbn_pdf'])
             for v in CFG['verk']]
    lista += [(s['id'], s['titel'], s['forfattare'], [VERK[x] for x in s['delar']], s['ingress'],
               s['isbn_epub'], s['isbn_pdf']) for s in CFG['samlingar']]
    return lista


def filnamn(bok_id):
    return bok_id + ('' if CFG['granskad'] else '-granskning')


def bygg_bocker():
    BYGG.mkdir(exist_ok=True)
    NED.mkdir(parents=True, exist_ok=True)
    for bok_id, titel, forf, vl, ingress, ie, ip in bocker():
        fn = filnamn(bok_id)
        cover = BYGG / f'{bok_id}-omslag.jpg'
        v0 = vl[0]
        omslag(bok_id, titel, forf, cover, v0.get('omslag_rad', 'Översatt från grekiskan'))
        shutil.copy(cover, NED / f'{bok_id}-omslag.jpg')
        meta = [
            '--metadata', f'title={titel}', '--metadata', f'author={forf}',
            '--metadata', 'lang=sv-SE', '--metadata', f'date={CFG["datum"]}',
            '--metadata', f'subtitle={v0.get("undertitel", "Översatt från grekiskan med AI")} · {CFG["serie"]}' + ('' if CFG['granskad'] else ' · Granskningsexemplar'),
            '--metadata', f'publisher={CFG["utgivare"]}',
            '--metadata', 'rights=CC BY-SA 4.0',
            '--metadata', f'contributor=Översättning: {modellnamn(v0)}'
                          + (f'; granskning: {CFG["granskare"]}' if CFG['granskad'] else ''),
            '--metadata', 'description=' + ingress + f' AI-översättning ({modellnamn(v0)}).',
        ]
        if ie:
            meta += ['--metadata', f'identifier=urn:isbn:{ie}']
        # EPUB
        src = BYGG / f'{bok_id}-epub.md'
        src.write_text(bok_md(bok_id, titel, forf, vl, ingress, ie, ip, 'epub'), encoding='utf-8')
        pandoc(str(src), '-f', 'markdown', '-o', str(NED / f'{fn}.epub'), '--toc', '--toc-depth=1',
               '--split-level=1', '--css', str(ROT / 'mallar' / 'stil.css'),
               '--epub-cover-image', str(cover), '--lua-filter', str(ROT / 'filter' / 'steph.lua'),
               '--epub-embed-font', str(ROT / 'mallar/fonts/Cardo-Regular.ttf'), *meta)
        # PDF
        src = BYGG / f'{bok_id}-pdf.md'
        src.write_text(bok_md(bok_id, titel, forf, vl, ingress, ie, ip, 'pdf'), encoding='utf-8')
        pdfargs = [str(src), '-f', 'markdown', '-o', str(NED / f'{fn}.pdf'), '--pdf-engine=xelatex',
                   '--top-level-division=chapter', '--lua-filter', str(ROT / 'filter' / 'steph.lua'),
                   '-H', str(ROT / 'mallar' / 'latex-header.tex'),
                   '-V', 'documentclass=scrbook', '-V', 'classoption=twoside,open=any',
                   '-V', 'geometry:a5paper,inner=19mm,outer=27mm,top=20mm,bottom=24mm,marginparwidth=13mm,marginparsep=3mm',
                   '-V', 'mainfont=TeX Gyre Pagella', '-V', 'sansfont=TeX Gyre Heros', '-V', 'fontsize=10pt', '-V', 'lang=sv',
                   '-V', 'colorlinks=true', '-V', 'linkcolor=black', '-V', 'urlcolor=black', *meta]
        if len(vl) > 1 or v0.get('typ') == 'fragment':
            pdfargs.append('--toc')
        if shutil.which('xelatex'):
            pandoc(*pdfargs)
        else:
            if not shutil.which('weasyprint'):
                sys.exit('PDF kräver xelatex eller weasyprint.')
            pandoc(str(src), '-f', 'markdown', '-t', 'html5', '--standalone',
                   '-o', str(NED / f'{fn}.pdf'), '--pdf-engine=weasyprint',
                   '--css', str(ROT / 'mallar/pdf.css'),
                   '--lua-filter', str(ROT / 'filter/steph.lua'),
                   '--toc', '--toc-depth=1', *meta)
        print('byggd:', fn)


# ---------- webbplats ------------------------------------------------------

def sida(titel, innehall, djup=0, beskrivning=''):
    upp = '../' * djup
    utkast = '' if CFG['granskad'] else (
        '<div class="utkast">Granskningsversion – texterna är ännu inte granskade av en människa och ska inte spridas.</div>')
    return f'''<!DOCTYPE html>
<html lang="sv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titel)}</title>
<meta name="description" content="{html.escape(beskrivning or CFG['undertitel'])}">
<link rel="stylesheet" href="{upp}stil.css"></head>
<body>{utkast}
<header class="topp"><div class="bred"><a class="namn" href="{upp}index.html">{CFG['serie']}</a>
<a href="{upp}index.html">Texter</a><a href="{upp}om.html">Om översättningarna</a><a href="{upp}rattelser.html">Rättelser</a></div></header>
{innehall}
<footer class="fot"><div class="bred">Alla texter är AI-översättningar; modell och källor anges vid varje text.
{'Granskade av ' + CFG['granskare'] + '.' if CFG['granskad'] else 'Ej granskade ännu.'}
Licens <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.sv">CC BY-SA 4.0</a>.
Utgåva {CFG['version']}, {CFG['datum']}.</div></footer>
</body></html>
'''


def fragment_nav(v):
    data = fragment.ladda(ROT / 'texter' / v['fil'])
    lankar = ''.join(f'<a href="#{v["id"]}-{a["id"]}">{html.escape(a["name_sv"].split(" från ")[0])}</a>'
                     for a in data['authors'])
    return f'<nav class="tankarnav">{lankar}<a href="#{v["id"]}-ordlista">Ordlista</a><a href="#{v["id"]}-kallor">Källor</a></nav>\n\n'


def md_till_html(md):
    r = subprocess.run(['pandoc', '-f', 'markdown', '-t', 'html5', '--lua-filter', str(ROT / 'filter' / 'steph.lua')],
                       input=md, capture_output=True, text=True, check=True)
    return r.stdout


def nedl_knappar(bok_id, upp=''):
    fn = filnamn(bok_id)
    return (f'<a href="{upp}nedladdning/{fn}.epub">EPUB</a>'
            f'<a href="{upp}nedladdning/{fn}.pdf">PDF</a>')


def bygg_site():
    UT.mkdir(exist_ok=True)
    (UT / 'verk').mkdir(exist_ok=True)
    shutil.copy(ROT / 'mallar' / 'stil.css', UT / 'stil.css')
    (UT / '.nojekyll').write_text('')
    # verkssidor
    for v in CFG['verk']:
        md = (f'# {v["titel"]}\n\n<p class="noindent forf">{v["forfattare"]} · {(lambda u: u[0].lower() + u[1:])(v.get("undertitel", "Översatt från grekiskan"))}</p>\n\n'
              f'::: ai\n{ai_text([v])}:::\n\n{inledning([v], v["ingress"])}\n\n'
              f'<div class="knappar">{nedl_knappar(v["id"], "../")}</div>\n\n'
              + (fragment_nav(v) if v.get('typ') == 'fragment' else '')
              + verk_md(v, 2) +
              f'\n\n## Om utgåvan {{.unnumbered}}\n\n::: kolofon\n'
              + kolofon(v['titel'], v['forfattare'], [v], v['isbn_epub'], v['isbn_pdf']) + ':::\n')
        (UT / 'verk' / f'{v["id"]}.html').write_text(
            sida(f'{v["forfattare"]}: {v["titel"]} – {CFG["serie"]}', '<main>' + md_till_html(md) + '</main>', 1,
                 v['ingress'][:155]), encoding='utf-8')
    # startsida
    kort = []
    for s in CFG['samlingar']:
        kort.append(f'<div class="kort"><h2>{s["titel"]}</h2><p class="forf">{s["forfattare"]} · samlingsvolym</p>'
                    f'<p>{html.escape(s["ingress"])}</p><div class="knappar">'
                    + ''.join(f'<a href="verk/{x}.html">Läs {VERK[x]["titel"]}</a>' for x in s['delar'])
                    + nedl_knappar(s['id']) + '</div></div>')
    for v in CFG['verk']:
        kort.append(f'<div class="kort"><h2><a href="verk/{v["id"]}.html">{v["titel"]}</a></h2>'
                    f'<p class="forf">{v["forfattare"]}</p><p>{html.escape(v["ingress"])}</p>'
                    f'<div class="knappar"><a href="verk/{v["id"]}.html">Läs online</a>{nedl_knappar(v["id"])}</div></div>')
    start = (f'<main><h1>{CFG["serie"]}</h1><p class="noindent">{CFG["undertitel"]}</p>'
             f'<div class="ai"><p><strong>Alla texter här är AI-översättningar.</strong> De är översatta av språkmodeller '
             f'({", ".join(sorted({modellnamn(v) for v in CFG["verk"]}))}). Vid varje text står vilken modell som använts och '
             f'från vilken källtext den översatts. '
             + ('De har lästs igenom och redigerats av ' + CFG['granskare'] + '.' if CFG['granskad'] else 'De har ännu inte granskats av en människa.')
             + ' Läs dem som en hjälp att komma in i texterna, inte som vetenskapliga utgåvor. '
             '<a href="om.html">Så gjordes översättningarna</a>.</p></div>'
             + ''.join(kort) + '</main>')
    (UT / 'index.html').write_text(sida(CFG['serie'], start), encoding='utf-8')
    # om
    om = (ROT / 'texter' / 'om.md').read_text(encoding='utf-8')
    om = om.format(**{k: v for k, v in CFG.items() if isinstance(v, str)},
                   granskning=granskningsmening())
    (UT / 'om.html').write_text(sida('Om översättningarna – ' + CFG['serie'],
                                     '<main class="prosa">' + md_till_html(om) + '</main>'), encoding='utf-8')
    ratt = (ROT / 'texter' / 'rattelser.md').read_text(encoding='utf-8').format(
        **{k: v for k, v in CFG.items() if isinstance(v, str)})
    (UT / 'rattelser.html').write_text(sida('Rättelser – ' + CFG['serie'],
                                            '<main class="prosa">' + md_till_html(ratt) + '</main>'), encoding='utf-8')
    print('webbplats byggd i', UT)


if __name__ == '__main__':
    if '--bara-site' not in sys.argv:
        bygg_bocker()
    bygg_site()

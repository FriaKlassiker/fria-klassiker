"""Fragmentsamlingar (t.ex. Försokratikerna) från JSON till markdown för build.py."""
import json, re
from collections import OrderedDict

ART = {
    'fragment': 'fragment',
    'transmitted_fragment_record': 'fragmentpost',
    'work_title': 'verkstitel',
    'testimonium_with_fragment': 'vittnesmål med fragment',
    'testimonium': 'vittnesmål',
    'testimonium_or_editorial_report': 'vittnesmål',
    'attributed_expression_or_report': 'tillskrivet yttrande',
    'editorial_cross_reference': 'hänvisning',
}
SPRAK = {'grc': 'grekiskan', 'la': 'latinet', 'mul': 'grekiskan och latinet', 'de': 'tyskan', 'en': 'engelskan'}
SPRAKORD = ('German', 'French', 'Italian', 'English', 'Spanish')


def esc(t):
    t = t.replace('\\', '\\\\')
    for c in '*_`[]<>$~^@':
        t = t.replace(c, '\\' + c)
    return t


def esc_rad(rad):
    rad = esc(rad)
    m = re.match(r'(\d+)([.)])(\s|$)', rad)
    if m:
        rad = m.group(1) + '\\' + rad[len(m.group(1)):]
    elif re.match(r'[-+#|:](\s|$)', rad):
        rad = '\\' + rad
    return rad


def stycken(text):
    ut = []
    for st in re.split(r'\n\s*\n', text.strip()):
        rader = [esc_rad(r.strip()) for r in st.split('\n') if r.strip()]
        if rader:
            ut.append('\\\n'.join(rader))
    return ut


def ladda(sokvag):
    return json.loads(open(sokvag, encoding='utf-8').read())


def referens(r):
    rs, ref = r['reference_system'], r['reference']
    if rs.startswith('DK'):
        return 'DK ' + ref
    if rs.startswith('Burnet 1920, num'):
        return 'Burnet ' + ref
    if re.fullmatch(r'V\d+', ref):
        return 'Vittnesmål ' + ref[1:]
    return ref


def ar(t):
    m = re.search(r'\b(1[5-9]\d\d)\b', t)
    return m.group(1) if m else ''


def stod_kort(credit):
    delar = [p.strip() for p in credit.split(' · ')]
    if delar[0] in SPRAKORD:
        delar = delar[1:]
    namn = re.sub(r'\s*\(\d{4}[–-]\d{4}\)', '', delar[0].split(';')[0]).strip()
    a = ar(' '.join(delar[1:]))
    return f'{namn} {a}'.strip()


def kalla_kort(r):
    if r.get('support_credit'):
        return f'Från {SPRAK.get(r["source_language"], "originalet")} med stöd av {stod_kort(r["support_credit"])}.'
    if 'Burnet' in r['translation_basis'] or r['source_language'] == 'en':
        return 'Från Burnets engelska (1920).'
    return f'Från {SPRAK.get(r["source_language"], "originalet")}.'


def stod_nyckel(credit):
    delar = [p.strip() for p in credit.split(' · ')]
    if delar[0] in SPRAKORD:
        delar = delar[1:]
    rad = ' · '.join(delar)
    rad = re.sub(r'\s*\(\d{4}[–-]\d{4}\)', '', rad).replace('second edition', '2nd edition').replace('volume II', 'vol. 2')
    i = rad.find(')')
    return rad[:i + 1] if i > 0 else rad


def burnet_baserad(poster):
    return all('Burnet' in p['translation_basis'] for p in poster)


def tankare(data):
    poster = OrderedDict((a['id'], []) for a in data['authors'])
    for r in data['records']:
        poster[r['author_id']].append(r)
    return [(a, poster[a['id']]) for a in data['authors']]


def grund_mening(poster):
    if burnet_baserad(poster):
        return ('Översättningen är gjord från John Burnets engelska översättning i *Early Greek Philosophy* '
                '(3:e upplagan, 1920), inte direkt från grekiskan. Numreringen är Burnets.')
    return ('Översättningen är gjord från den grekiska eller latinska texten i Diels utgåva, med äldre '
            'översättningar som stöd. Vilken stödöversättning som använts anges vid varje post.')


def post_md(r):
    d = [f'::: {{.post #{re.sub(r"[^A-Za-z0-9-]", "-", r["id"])}}}',
         f'[{esc(referens(r))} · {ART.get(r["kind"], r["kind"])}]{{.postref}}', '']
    d += [s + '\n' for s in stycken(r['text_sv'])]
    for n in r.get('notes_sv') or []:
        d.append(f'[Not: {esc(n)}]{{.not}}\n')
    if r.get('editorial_caution_sv'):
        d.append(f'[{esc(r["editorial_caution_sv"])}]{{.not}}\n')
    d.append(f'[{kalla_kort(r)}]{{.kalla}}')
    d.append(':::\n')
    return '\n'.join(d)


def delar_md(v, data, niva=1, grek=lambda t: t):
    """Ett kapitel per tänkare + bilagor. niva=1 i böcker, 2 på webbsidan."""
    h = '#' * niva
    ut = []
    for a, poster in tankare(data):
        ut.append(f'{h} {a["name_sv"]} {{#{v["id"]}-{a["id"]} .unnumbered}}\n')
        ingress = ' '.join(x for x in [a.get('scope_sv'), a.get('editorial_note_sv')] if x)
        ut.append('::: ingress\n' + esc(ingress) + '\n\n' + grund_mening(poster) + '\n:::\n')
        ut += [post_md(r) for r in poster]
    # ordlista
    ut.append(f'{h} Ordlista {{#{v["id"]}-ordlista .unnumbered}}\n')
    ut.append('Bärande begrepp och hur de återges i översättningen.\n')
    for g in data.get('glossary', []):
        ut.append(f'**{grek(g["greek"])}** ({esc(g["transliteration"])})\n:   {esc(g["swedish"])}.'
                  + (f' *{esc(g["note"])}*' if g.get('note') else '') + '\n')
    # källor
    ut.append(f'{h} Källor {{#{v["id"]}-kallor .unnumbered}}\n')
    ut.append('**Grundtext.** ' + esc(v['grundtext']) + '\n')
    ut.append('**Äldre översättningar som använts som stöd** (alla fria från upphovsrätt):\n')
    nycklar = sorted({stod_nyckel(r['support_credit']) for r in data['records'] if r.get('support_credit')},
                     key=lambda s: s.lower())
    ut += [f'- {esc(n)}' for n in nycklar]
    ut.append('')
    return '\n'.join(ut) + '\n'


def inledning_md(v, data):
    d = [esc(v['ingress']), '']
    d.append('**Om urvalet.** ' + esc(data.get('scope_sv', '')))
    d.append('')
    d.append('**Numrering.** ' + esc(data.get('numbering_note_sv', '')) +
             ' DK står för Diels–Kranz, den vedertagna numreringen av försokratikernas fragment; '
             'B-nummer är fragment och A-nummer vittnesmål. "Burnet" anger numreringen i John Burnets *Early Greek Philosophy*.')
    d.append('')
    d.append('**Att läsa fragmenten.**\n')
    d += [f'- {esc(n)}' for n in data.get('reading_notes_sv', [])]
    d.append('')
    return '\n'.join(d)

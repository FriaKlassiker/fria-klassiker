#!/usr/bin/env python3
"""Refresh the Fria klassiker presentation after the original build.py.
The original book HTML, PDFs, EPUBs, attribution and metadata remain intact.
Usage: python3 scripts/enhance_site.py
Needs: BeautifulSoup4. Does not require network access.
"""
from __future__ import annotations
from pathlib import Path
import json, html, re
from bs4 import BeautifulSoup

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
CONFIG=json.loads((ROOT/'config.json').read_text(encoding='utf-8'))
ORG_URL='https://github.com/FriaKlassiker'
REPO_URL='https://github.com/FriaKlassiker/fria-klassiker'
SITE_URL='https://friaklassiker.github.io/fria-klassiker/'

specials={
 'sokrates-sista-dagar':{'id':'sokrates-sista-dagar','titel':'Sokrates sista dagar','forfattare':'Platon','ingress':'Följ Sokrates från anklagelsen till den sista dagen i fängelset. De fyra dialogerna Euthyfron, Sokrates försvarstal, Kriton och Faidon samlas här i den ordning som berättelsen utspelar sig.','category':'Platon','tag':'Samlingsvolym','art':'sokrates-sista-dagar','format':'-granskning','path':'sokrates-sista-dagar'},
 'staten-bok-i-ii':{'id':'staten-bok-i-ii','titel':'Staten, bok I–II','forfattare':'Platon','ingress':'Vad är rättvisa? Sokrates diskuterar den starkares rätt och stadens uppkomst med Thrasymachos, Glaukon och Adeimantos. Endast de två första av verkets tio böcker är översatta här, via Paul Shoreys engelska text med grekiska kontroller.','category':'Platon','tag':'Endast bok I–II','art':'staten-bok-i-ii','format':'-arbetsutgava','path':'staten-bok-i-ii'}
}
category={'euthyfron':'Platon','forsvarstalet':'Platon','kriton':'Platon','faidon':'Platon','handboken':'Stoa','kategorierna':'Aristoteles','forsokratikerna':'Fragment'}
book_data={b['id']:{**b,'category':category.get(b['id'],'Övrigt'),'tag':'AI-översättning','art':b['id'],'format':'-granskning','path':b['id']} for b in CONFIG['verk']}
book_data.update(specials)
ordered=['sokrates-sista-dagar','forsokratikerna','staten-bok-i-ii','euthyfron','forsvarstalet','kriton','faidon','kategorierna','handboken']


def q(s):return html.escape(str(s),quote=True)

def header(base,active=''):
 return f'''<header class="site-nav"><div class="site-container nav-inner">
 <a class="nav-brand" href="{base}index.html" aria-label="Fria klassiker – startsidan"><img src="{base}assets/brand-mark.svg" alt="" width="48" height="48">Fria klassiker</a>
 <nav class="nav-links" aria-label="Huvudnavigation">
 <a href="{base}index.html#bibliotek" {'aria-current="page"' if active=='books' else ''}>Biblioteket</a>
 <a href="{base}om.html" {'aria-current="page"' if active=='about' else ''}>Om projektet</a>
 <a href="{base}rattelser.html" {'aria-current="page"' if active=='errors' else ''}>Rättelser</a>
 <a class="nav-cta" href="{REPO_URL}" rel="noopener noreferrer">GitHub ↗</a>
 </nav></div></header>'''

def alert():
 return '<div class="edition-alert" role="note"><strong>Arbetsutgåvor.</strong> AI-framställda översättningar, ännu inte fackgranskade av en klassiker. Kontrollera viktiga citat mot originaltexten.</div>'

def footer(base):
 return f'''<footer class="site-footer"><div class="site-container footer-inner">
 <div><div class="footer-brand"><img src="{base}assets/brand-mark.svg" alt="" width="43" height="43">Fria klassiker</div>
 <p>Antik filosofi på svenska. Gratis att läsa, dela och förbättra. Oberoende öppet textprojekt och en transparent undersökning av AI-översättning.</p></div>
 <nav class="footer-links" aria-label="Sidfot"><a href="{base}index.html#bibliotek">Alla texter</a><a href="{base}om.html">Metod &amp; källor</a><a href="{base}rattelser.html">Rapportera fel</a><a href="{REPO_URL}">Källkod</a></nav>
 </div><div class="site-container footer-bottom">Arbetsutgåva 0.9 · 19 november 2026 · Svenska AI-översättningar · CC BY-SA 4.0 för publicerat textmaterial enligt angiven källlicens. Ingen extern filologisk granskning har bekräftats.</div></footer>'''

def buttons(book):
 id=book['id']
 if id=='staten-bok-i-ii': slug='staten-bok-i-ii-arbetsutgava'
 else:slug=id+'-granskning'
 return ('verk/'+book['path']+'.html','nedladdning/'+slug+'.pdf','nedladdning/'+slug+'.epub')

def card(book):
 read,pdf,epub=buttons(book)
 tag=book['tag']
 if book['id']=='sokrates-sista-dagar':tag='4 dialoger i 1'
 if book['id']=='forsokratikerna':tag='805 textposter'
 if book['id']=='staten-bok-i-ii':tag='Ofullständig utgåva'
 cover='nedladdning/'+book['art']+'-omslag.jpg'
 excerpt=book['ingress']
 if len(excerpt)>230:excerpt=excerpt[:225].rsplit(' ',1)[0]+'…'
 searchable=' '.join([book['titel'],book['forfattare'],book['ingress'],book['category']]).casefold()
 return f'''<article class="book-card" data-category="{q(book['category'])}" data-search="{q(searchable)}">
 <a href="{q(read)}" class="book-visual" aria-label="Läs {q(book['titel'])}">
 <img loading="lazy" src="{q(cover)}" alt="Bokomslag: {q(book['titel'])}" width="160" height="256"><span class="book-badge">{q(tag)}</span></a>
 <div class="book-content"><span class="book-author">{q(book['forfattare'])}</span><h3><a href="{q(read)}">{q(book['titel'])}</a></h3><p class="book-description">{q(excerpt)}</p>
 <div class="book-links"><a href="{q(read)}">Läs online ↗</a><a href="{q(epub)}" download>↓ EPUB</a><a href="{q(pdf)}" download>↓ PDF</a></div></div></article>'''

def homepage():
 cards='\n'.join(card(book_data[i]) for i in ordered)
 count=len(ordered)
 search_icon='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/></svg>'
 return f'''<!doctype html><html lang="sv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
 <title>Fria klassiker – Antik filosofi. Nytt liv på svenska.</title>
 <meta name="description" content="Fria svenska läsutgåvor av Platon, Aristoteles, Epiktetos och försokratikerna. Läs online eller ladda ned PDF och EPUB. Öppna AI-översättningar med redovisad metod.">
 <meta name="theme-color" content="#5b2b2d"><meta property="og:type" content="website"><meta property="og:title" content="Fria klassiker"><meta property="og:description" content="Antik filosofi på modern svenska, fritt att läsa, dela och förbättra.">
 <meta property="og:image" content="{SITE_URL}assets/logo-horizontal.png"><link rel="icon" href="assets/brand-mark.svg" type="image/svg+xml">
 <link rel="stylesheet" href="stil.css"><link rel="stylesheet" href="portal.css"><script defer src="portal.js"></script></head>
 <body class="home-page">{alert()}{header('',active='books')}
 <main id="innehall"><section class="hero"><div class="site-container hero-inner"><div class="hero-copy">
 <div class="eyebrow">Ett öppet bibliotek för nyfikna läsare</div>
 <h1>Gamla tankar.<br><em>Nya röster.</em></h1>
 <p class="hero-lead">Från Sokrates och stoikerna till försokratikernas gåtfulla fragment. Utforska antikens filosofi på nutida svenska, utan betalväggar.</p>
 <div class="hero-actions"><a class="btn btn-primary" href="#bibliotek">Utforska biblioteket <span aria-hidden="true">↗</span></a><a class="btn btn-quiet" href="om.html">Så görs översättningarna</a></div>
 <div class="hero-facts"><span>Gratis PDF &amp; EPUB</span><span>Läs direkt i webbläsaren</span><span>Öppen källtext och metod</span></div>
 </div><div class="hero-art" aria-hidden="true"><div class="art-circle"></div>
 <img class="hero-cover hero-cover-a" src="nedladdning/forsokratikerna-omslag.jpg" alt="">
 <img class="hero-cover hero-cover-b" src="nedladdning/sokrates-sista-dagar-omslag.jpg" alt="">
 <img class="hero-cover hero-cover-c" src="nedladdning/staten-bok-i-ii-omslag.jpg" alt="">
 <div class="hero-stamp">Läs · Dela<br>Utforska<br>Fritt</div></div></div></section>
 <div class="stats-band"><div class="site-container stats-inner"><div class="stat"><b>{count}</b><span>utgåvor i biblioteket</span></div><div class="stat"><b>805</b><span>försokratiska textposter</span></div><div class="stat"><b>2</b><span>nedladdningsformat</span></div></div></div>
 <section class="site-container section-pad" id="bibliotek"><div class="section-heading"><div><div class="eyebrow">Bokhyllan</div><h2>Upptäck ett verk</h2></div>
 <p>Hitta en dialog att börja med, följ ett filosofiskt argument eller fördjupa dig i ett helt fragmentarkiv.</p></div>
 <div class="catalog-toolbar"><div class="filter-tabs" role="group" aria-label="Filtrera efter författare eller område">
 <button class="filter" data-filter="alla" aria-pressed="true">Alla</button><button class="filter" data-filter="Platon" aria-pressed="false">Platon</button><button class="filter" data-filter="Aristoteles" aria-pressed="false">Aristoteles</button><button class="filter" data-filter="Stoa" aria-pressed="false">Stoikerna</button><button class="filter" data-filter="Fragment" aria-pressed="false">Försokratikerna</button></div>
 <label class="search-box">{search_icon}<input id="search-books" type="search" placeholder="Sök bland böckerna" aria-label="Sök bland böckerna"></label></div>
 <p class="catalog-count" id="catalog-count" aria-live="polite">{count} av {count} utgåvor</p><div id="bok-katalog" class="book-grid">{cards}</div>
 </section>
 <section class="method-section"><div class="site-container section-pad method-inner"><div><div class="eyebrow">Öppet arbete, tydlig härkomst</div><h2>Vi berättar också hur böckerna blev till.</h2>
 <p>Här hittar du inte anonyma, maskinskapade texter. Översättningarna är AI-framställda, källtexterna och arbetsmetoden redovisas och utgåvorna är märkta med sin granskningsstatus. Rättelser välkomnas.</p>
 <a class="btn btn-primary" href="om.html">Läs om metoden ↗</a></div><div class="method-quote"><b>“</b><p>Kunskap blir större när fler får läsa, ifrågasätta och förbättra den.</p><small>FRIA KLASSIKER · ÖPPET TEXTARBETE</small></div></div></section></main>
 {footer('')}</body></html>'''


def book_toolbar(id):
 b=book_data[id];read,pdf,epub=buttons(b)
 return f'''<div class="reader-toolbar" role="group" aria-label="Läsverktyg"><span>Välj läsläge eller hämta boken</span>
 <div class="reader-tools"><button type="button" data-reader-action="smaller" aria-label="Minska textstorleken">A−</button><button type="button" data-reader-action="larger" aria-label="Öka textstorleken">A+</button><button type="button" data-reader-action="night" aria-pressed="false">Mörkt läsläge</button><a href="../{q(epub)}" download>EPUB ↓</a><a href="../{q(pdf)}" download>PDF ↓</a></div></div>'''


def update_existing_page(filename,id=None):
 p=SITE/filename
 s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser')
 reader=id is not None
 s.body['class']=['reader-page' if reader else 'information-page']
 for old in s.body.select('.utkast, header.topp, footer.fot'):
  old.decompose()
 base='../' if filename.startswith('verk/') else ''
 nav=BeautifulSoup(alert()+header(base,'about' if filename=='om.html' else 'errors' if filename=='rattelser.html' else ''),'html.parser')
 s.body.insert(0,nav)
 s.body.append(BeautifulSoup(footer(base),'html.parser'))
 for x in [x for x in s.head.find_all('link',rel='icon')]:x.decompose()
 s.head.append(BeautifulSoup(f'<link rel="icon" type="image/svg+xml" href="{base}assets/brand-mark.svg"><link rel="stylesheet" href="{base}portal.css"><script defer src="{base}portal.js"></script>','html.parser'))
 desc=s.head.find('meta',attrs={'name':'description'})
 if not desc:
  s.head.append(BeautifulSoup('<meta name="description" content="Öppna svenska AI-översättningar av klassisk filosofi; redovisad metod och granskningsstatus.">','html.parser'))
 main=s.main
 if reader:
  main['class']=['reader-main']
  main.insert(0,BeautifulSoup('<a class="reader-crumb" href="../index.html#bibliotek">← Till biblioteket</a>','html.parser'))
  psub=main.find('p',class_='forf')
  if psub:psub.insert_after(BeautifulSoup(book_toolbar(id),'html.parser'))
  else:main.find('h1').insert_after(BeautifulSoup(book_toolbar(id),'html.parser'))
  for x in main.find_all('div',class_='knappar'):x.decompose()
 else:
  main.insert(0,BeautifulSoup('<a class="reader-crumb" href="index.html">← Till biblioteket</a>','html.parser'))
 # Replace generic placeholders in original content with planned project path, not active claim.
 src=str(s).replace('https://github.com/ANVANDARNAMN/fria-klassiker',REPO_URL).replace('https://ANVANDARNAMN.github.io/fria-klassiker/',SITE_URL)
 p.write_text('<!doctype html>\n'+src,encoding='utf-8')


def staten_page():
 b=book_data['staten-bok-i-ii']
 frag=(SITE/'assets/staten-reading-fragment.html').read_text(encoding='utf-8')
 # Structured section IDs for book navigation
 frag=frag.replace('<h2>Bok I</h2>','<h2 id="bok-i">Bok I</h2>').replace('<h2>Bok II</h2>','<h2 id="bok-ii">Bok II</h2>')
 head='''<!doctype html><html lang="sv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Staten, bok I–II – Platon | Fria klassiker</title><meta name="description" content="Platon: Staten, bok I och II i svensk AI-översättning. Läs gratis eller ladda ned PDF och EPUB. Observera att endast två av tio böcker ingår."><link rel="icon" type="image/svg+xml" href="../assets/brand-mark.svg"><link rel="stylesheet" href="../stil.css"><link rel="stylesheet" href="../portal.css"><script defer src="../portal.js"></script></head>'''
 body=f'''<body class="reader-page staten-page">{alert()}{header('../')}
 <main class="reader-main"><a class="reader-crumb" href="../index.html#bibliotek">← Till biblioteket</a><h1>Staten</h1><p class="noindent forf">Platon · Böckerna I–II av X · svensk läsöversättning</p>
 {book_toolbar('staten-bok-i-ii')}
 <div class="ai"><p><strong>Arbetsutgåva, inte hela Staten.</strong> Denna utgåva innehåller endast bok I och bok II. Svenskan är genererad med ChatGPT huvudsakligen från Paul Shoreys engelska översättning med kontroller mot Burnets grekiska text. Ingen extern filologisk granskning är utförd. PDF-filen är den ursprungliga typografiska utgåvan. EPUB och webbläsartexten är rekonstruerade från PDF-textlagret; för exakta citat bör PDF och källtext kontrolleras.</p></div>
 <nav class="tankarnav" aria-label="Välj bok"><a href="#bok-i">Bok I: rättvisan</a><a href="#bok-ii">Bok II: rättvisans värde</a></nav>
 {frag}</main>{footer('../')}</body></html>'''
 (SITE/'verk/staten-bok-i-ii.html').write_text(head+body,encoding='utf-8')


def socrates_page():
 entries=[('Euthyfron','euthyfron','Vad är fromhet?'),('Sokrates försvarstal','forsvarstalet','Rättegången i Aten'),('Kriton','kriton','Fångenskapen och lagen'),('Faidon','faidon','Den sista dagen och själen')]
 lis=''.join(f'<li style="margin-bottom:1.1rem"><a href="{slug}.html"><strong>{q(name)}</strong></a> · {q(sub)}</li>' for name,slug,sub in entries)
 html_doc=f'''<!doctype html><html lang="sv"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sokrates sista dagar – Fria klassiker</title><meta name="description" content="Läs de fyra Platondialogerna om Sokrates sista dagar. Svensk AI-översättning, gratis som PDF eller EPUB."><link rel="icon" type="image/svg+xml" href="../assets/brand-mark.svg"><link rel="stylesheet" href="../stil.css"><link rel="stylesheet" href="../portal.css"></head>
 <body class="information-page">{alert()}{header('../')}
 <main><a class="reader-crumb" href="../index.html#bibliotek">← Till biblioteket</a><h1>Sokrates sista dagar</h1><p class="noindent forf">Platon · Fyra dialoger i en samlingsvolym</p><img src="../nedladdning/sokrates-sista-dagar-omslag.jpg" alt="Omslag till Sokrates sista dagar" style="max-width:160px;float:right;margin:6px 0 20px 24px;box-shadow:8px 9px 22px #42322630">
 <p>Fyra dialoger följer Sokrates från anklagelsen till hans sista dag. Läs dem i följd på webben eller ladda ned hela samlingsvolymen.</p>
 <div class="ai"><p><strong>Arbetsutgåva.</strong> Svenska AI-översättningar. Inte fackgranskade. Metod och källor finns beskrivna i respektive dialog och på <a href="../om.html">om-sidan</a>.</p></div>
 <h2>Dialogerna i ordning</h2><ol>{lis}</ol><h2>Hämta hela samlingen</h2><p><a class="btn btn-primary" href="../nedladdning/sokrates-sista-dagar-granskning.epub" download>↓ Hämta EPUB</a> <a class="btn btn-quiet" href="../nedladdning/sokrates-sista-dagar-granskning.pdf" download>↓ Hämta PDF</a></p>
 </main>{footer('../')}</body></html>'''
 (SITE/'verk/sokrates-sista-dagar.html').write_text(html_doc,encoding='utf-8')


def org_profile():
 folder=ROOT/'org-profile';(folder/'profile/assets').mkdir(parents=True,exist_ok=True)
 from shutil import copyfile
 copyfile(SITE/'assets/logo-horizontal.png',folder/'profile/assets/logo-horizontal.png')
 (folder/'profile/README.md').write_text(f'''<div align="center">\n\n![Fria klassiker](assets/logo-horizontal.png)\n\n# Antik filosofi. Nytt liv på svenska.\n\n**Ett öppet bibliotek med klassiska filosofiska texter, fritt tillgängliga för läsning och granskning.**\n\n[📚 Läs biblioteket]({SITE_URL}) · [🔎 Se projektets källkod]({REPO_URL}) · [✍️ Rapportera en rättelse]({REPO_URL}/issues)\n\n</div>\n\n### Vad finns här?\n\nPlatons dialoger, Aristoteles *Kategorierna*, Epiktetos *Handboken*, försokratiska fragment och delar av Platons *Staten*, på svenska. Utgåvorna erbjuds för läsning online och som **PDF** och **EPUB**.\n\n### Öppenhet före skenbar säkerhet\n\nMaterialet är **AI-översatt och ännu inte filologiskt fackgranskat**. Vi redovisar modeller, textunderlag, licens, källor och granskningsstatus. *Staten* omfattar endast bok I–II.\n\nBidrag, källkontroller, språkliga förbättringar och andra rättelser är välkomna.\n\n**Licens:** CC BY-SA 4.0 för de utgåvor som publiceras med den märkningen. Kontrollera källangivelser per verk.\n''',encoding='utf-8')
 (folder/'README.md').write_text('Detta är innehållet till GitHub-organisationens profilrepository `.github`. Skapa `FriaKlassiker/.github` och placera `profile/` i dess rot. Detta är separat från bibliotekswebbplatsens repository.\n',encoding='utf-8')


def update_docs():
 c=CONFIG.copy();c['repo_url']=REPO_URL;c['site_url']=SITE_URL
 (ROOT/'config.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 p=ROOT/'README.md';readme=p.read_text(encoding='utf-8')
 readme=readme.replace('Varje verk finns som webbsida, EPUB och PDF (A5).','Varje utgåva finns som webbsida, EPUB och PDF. **Undantag:** *Staten* har en PDF i ursprungligt A4-format; EPUB och HTML är rekonstruerade från denna. *Staten* innehåller bara böckerna I och II (av tio).')
 readme=readme.replace('Alla texter granskas av en människa innan de publiceras.','**Utgåvorna är arbetsversioner och är ännu inte externt fackgranskade.**')
 readme=readme.replace('## Bygga','## Ny portal och logo\n\n- Webbplats: `site/index.html` och `site/portal.css` med responsiv bokkatalog, sökning och läslägen.\n- Logotyp: `site/assets/brand-mark.svg`, `site/assets/logo-horizontal.svg` samt PNG-varianter.\n- GitHub-organisationsprofil: `org-profile/profile/README.md` och profilbilden som hör dit.\n- *Staten*, bok I–II: original-PDF i `site/nedladdning/`, en från PDF-textlagret rekonstruerad EPUB, en webbläsarutgåva och ett bearbetningsbart Markdown-utdrag i `texter/`.\n- PDF-textlagrets rekonstruerade lästext bör kontrolleras mot PDF vid exakta citat.\n\n## Bygga')
 readme=readme.replace('python3 build.py --bara-site','python3 build.py --bara-site\npython3 scripts/enhance_site.py  # behöver BeautifulSoup4; kör sist')
 readme += '\n### Publicering\n\nSe `PUBLICERA_GITHUB.md` för steg för steg om repository, organisationens profil och Pages. Ingen GitHub-publicering sker automatiskt när ZIP-arkivet packas upp.\n'
 p.write_text(readme,encoding='utf-8')
 (ROOT/'PUBLICERA_GITHUB.md').write_text(f'''# Publicera Fria klassiker på GitHub\n\n## 1. Huvudrepository\n\nSkapa ett **publikt repository** med namnet `fria-klassiker` under organisationen [{ORG_URL}]({ORG_URL}). Lägg innehållet från denna katalog i **repositoryts rot** (inte i en extra underkatalog). Uteslut `org-profile/` eftersom det är ett separat repository.\n\n1. Skapa repositoryt `FriaKlassiker/fria-klassiker`.\n2. Ladda upp samtliga projektfiler eller pusha lokalt med `git`.\n3. Öppna **Settings → Pages → Build and deployment → Source → GitHub Actions**.\n4. Actions-workflowet `.github/workflows/pages.yml` publicerar `site/` när `main` uppdateras.\n5. Efter att arbetsflödet har avslutats: [{SITE_URL}]({SITE_URL}).\n6. Slå på Issues under repository-inställningarna för rättelser.\n\nExempel med lokalt Git, om repo redan är skapat:\n\n```bash\ngit init\ngit add .\ngit commit -m "Launch Fria klassiker library"\ngit branch -M main\ngit remote add origin {REPO_URL}.git\ngit push -u origin main\n```\n\n## 2. Logotyp för organisationens profil\n\nSkapa ett andra publikt repository under organisationen med namnet **`.github`**. Kopiera filerna från `org-profile/` till det repositoryts rot. GitHub visar då `profile/README.md` på {ORG_URL}. Om organisationsprofilen har en avatar kan den sättas till `site/assets/brand-mark.png`.\n\n## 3. Om GitHub-appens åtkomst saknas\n\nDen anslutna GitHub-appen måste installeras eller få rättigheter för organisationen **FriaKlassiker** och dess repositories. Först då kan verktyg som använder denna app skriva i repot direkt. Att kopplingen har åtkomst till ett annat personligt GitHub-konto räcker inte.\n\n## 4. Redaktörsvarningar\n\n- Alla böcker är markerade som **arbetsutgåvor/ej fackgranskade**. Ändra inte detta förrän verken verkligen granskats.\n- *Staten* är endast bok I–II, inte hela verket.\n- Alla PDF- och EPUB-utgåvor ligger under `site/nedladdning/`.\n- En del underlag hänvisar till DOI, ISBN eller en separat JSON för *Staten* som inte finns i paketet. Påstå inte att sådana identifierare/objekt är publicerade.\n- Kontrollera källa, licens, medverkande och eventuell upphovsrätt innan en formell lansering.\n\n## 5. Efter att texter eller mallar ändras\n\n`python3 build.py --bara-site` uppdaterar webbtexten i originalmallen. Kör därefter **alltid** `python3 scripts/enhance_site.py` för att återställa den grafiska portalen. För *Staten*-konverteringen gäller `python3 scripts/extract_staten.py`.\n''',encoding='utf-8')

if __name__=='__main__':
 for b in CONFIG['verk']:update_existing_page('verk/'+b['id']+'.html',b['id'])
 for name in ['om.html','rattelser.html']:update_existing_page(name)
 staten_page();socrates_page()
 (SITE/'index.html').write_text(homepage(),encoding='utf-8')
 update_docs();org_profile()
 print('Created modern portal, nine library entries, reading views, and organization profile.')

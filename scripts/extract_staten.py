#!/usr/bin/env python3
"""Build an accessible HTML reading edition and EPUB from the supplied, typeset Staten PDF.
This is a best-effort reconstruction from a PDF text layer. The PDF remains the archival reference.
Usage: python3 scripts/extract_staten.py
Needs: PyMuPDF, pandoc (for EPUB), Pillow (for generated cover)
"""
from __future__ import annotations
from pathlib import Path
from html import escape
import re, subprocess, json, shutil
import fitz
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
PDF=ROOT/'site/nedladdning/staten-bok-i-ii-arbetsutgava.pdf'
OUT=ROOT/'site/nedladdning/staten-bok-i-ii-arbetsutgava.epub'
COVER=ROOT/'site/nedladdning/staten-bok-i-ii-omslag.jpg'
HTML=ROOT/'site/assets/staten-reading-fragment.html'
MD=ROOT/'texter/staten-bok-i-ii.md'
FONT_REG='/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf'
FONT_BOLD='/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf'
FONT_SANS='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def f(path,size):
    try:return ImageFont.truetype(path,size)
    except:return ImageFont.load_default()


def cover():
    W,H=1600,2560
    im=Image.new('RGB',(W,H),'#243039');d=ImageDraw.Draw(im)
    # Warm brass rules, stepped classical geometry and restrained editorial typography
    gold='#D5AE72'; cream='#F1E5D1'; muted='#B5AD9C'
    d.rectangle((80,80,W-80,H-80),outline=gold,width=5)
    d.rectangle((107,107,W-107,H-107),outline='#7B6D59',width=2)
    for y in (195,212,1915,1932):d.line((235,y,W-235,y),fill=gold,width=3)
    d.ellipse((310,420,1290,1400),outline=gold,width=4)
    # Arch + column motif in the edition's brand language
    d.arc((430,520,1170,1300),180,360,fill=gold,width=16)
    for x in (490,670,850,1030):
        d.line((x,915,x,1260),fill=gold,width=20)
        d.rectangle((x-20,888,x+20,908),fill=gold)
        d.rectangle((x-27,1250,x+27,1267),fill=gold)
    d.line((420,1280,1180,1280),fill=gold,width=18)
    d.text((W/2,310),'F R I A   K L A S S I K E R',font=f(FONT_SANS,36),fill=muted,anchor='mm')
    d.text((W/2,1520),'PLATON',font=f(FONT_SANS,58),fill=gold,anchor='mm')
    d.text((W/2,1708),'Staten',font=f(FONT_BOLD,156),fill=cream,anchor='mm')
    d.text((W/2,1833),'BÖCKERNA I OCH II',font=f(FONT_SANS,51),fill=gold,anchor='mm')
    d.text((W/2,2120),'SVENSK LÄSÖVERSÄTTNING',font=f(FONT_SANS,38),fill=cream,anchor='mm')
    d.text((W/2,2192),'AI-ÖVERSATT • EJ FACKGRANSKAD',font=f(FONT_SANS,30),fill=muted,anchor='mm')
    d.text((W/2,2335),'ARBETSVERSION · 2026',font=f(FONT_SANS,32),fill=gold,anchor='mm')
    im.save(COVER,'JPEG',quality=90,optimize=True)


def clean_content():
    doc=fitz.open(PDF)
    assert len(doc)>=70
    elements=[]; md=[]; last_book=None
    # Skip PDF front cover and static PDF TOC; the HTML/EPUB has semantic navigation.
    for pno in [1]+list(range(3,len(doc))):
        page=doc[pno]
        blocks=[]
        for b in page.get_text('dict',sort=True)['blocks']:
            if 'lines' not in b:continue
            if b['bbox'][1]<55 or b['bbox'][1]>780:continue # running heading/footer
            spans=[sp for line in b['lines'] for sp in line['spans'] if sp['text'].strip()]
            if not spans:continue
            text=' '.join(sp['text'].strip() for sp in spans)
            text=re.sub(r'\s+',' ',text).strip()
            if not text:continue
            sz=max(s['size'] for s in spans)
            blocks.append([b['bbox'][1],b['bbox'][3],sz,text])
        # join consecutive physical text lines into full paragraphs, respect blank space
        merged=[]
        for top,bottom,sz,t in blocks:
            if merged and sz<12 and merged[-1][2]<12 and top-merged[-1][1]<4.2 and not re.fullmatch(r'\d{3}[a-e](?:-\d{3}[a-e])?',t):
                merged[-1][1]=bottom
                merged[-1][3] += ' '+t
            else:merged.append([top,bottom,sz,t])
        for top,bottom,sz,t in merged:
            if re.match(r'^(?:Staten\s*\|\s*|Platon\s*\|\s*Staten)',t):continue
            if re.match(r'^Stephanus\s+\d{3}[a-e]',t):
                elements.append(f'<p class="chapter-meta">{escape(t)}</p>');md.append('*'+t+'*');continue
            if pno==1 and t in ('Staten','Om översättningen'):continue
            if sz>=21:
                level='h2' if re.match(r'^(Bok I|Bok II|Översättningsnoter|Noter till bok|Källor och textunderlag)',t) else 'h3'
                if t=='Bok I' or t=='Bok II':last_book=t
                elements.append(f'<{level}>{escape(t)}</{level}>');md.append(('## ' if level=='h2' else '### ')+t)
            elif sz>=14:
                # Headers such as Om översättningen and note section subheads
                level='h2' if t in ('Om översättningen','Källor och textunderlag','Noter till bok I','Noter till bok II','Översättningsnoter') else 'h3'
                elements.append(f'<{level}>{escape(t)}</{level}>');md.append(('## ' if level=='h2' else '### ')+t)
            elif re.fullmatch(r'\d{3}[a-e](?:-\d{3}[a-e])?',t):
                elements.append(f'<span class="steph-inline">{escape(t)}</span>');md.append('**['+t+']**')
            else:
                elements.append(f'<p>{escape(t)}</p>');md.append(t)
    body='\n'.join(elements)
    HTML.write_text(body,encoding='utf-8')
    MD.write_text('# Staten: böckerna I och II\n\n> Arbetsutgåva. AI-framställd läsöversättning via Paul Shoreys engelska med grekiska kontroller. Ej extern filologisk granskning. Endast två av tio böcker. PDF är typografisk originalutgåva.\n\n'+'\n\n'.join(md)+'\n',encoding='utf-8')
    return body


def epub(body):
    meta='''<!DOCTYPE html><html lang="sv"><head><meta charset="utf-8"><title>Staten: Böckerna I och II</title><style>
body{font-family:Georgia,serif;line-height:1.55;color:#222;padding:1em;}h1,h2,h3{font-family:Georgia,serif;line-height:1.3;}h1{font-size:2.2em}h2{margin-top:2em;border-bottom:1px solid #ddd;padding-bottom:.3em;}h3{margin-top:1.5em;}p{margin:.65em 0;} .steph-inline,.chapter-meta{display:block;color:#875e44;font:75% sans-serif;margin:1em 0 .2em;} .notice{padding:1em;border-left:3px solid #875e44;background:#faf6ef;}
</style></head><body><h1>Staten</h1><h2>Böckerna I och II</h2><p><strong>Platon</strong></p><p class="notice">Arbetsutgåva · Svensk AI-översättning via Paul Shoreys engelska utgåva med kontroller mot grekiskan. Ej externt filologiskt granskad. Detta är två av verkets tio böcker.</p>'''
    full=meta+body+'</body></html>'
    tmp=ROOT/'scripts/.staten_epub_source.html';tmp.write_text(full,encoding='utf-8')
    cmd=['pandoc',str(tmp),'--from=html','--to=epub3','--standalone','--toc','--toc-depth=2','--metadata','title=Staten: böckerna I och II','--metadata','author=Platon','--metadata','lang=sv','--metadata','date=2026-11-19','--epub-cover-image',str(COVER),'-o',str(OUT)]
    subprocess.run(cmd,check=True)
    tmp.unlink(missing_ok=True)
    print('EPUB',OUT.stat().st_size,'bytes; MD chars',len(MD.read_text()))

if __name__=='__main__':
    cover();body=clean_content();epub(body)

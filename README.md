# Fria klassiker

Antik filosofi på modern svenska, fritt att läsa, kopiera och dela.

**Alla texter är AI-översättningar.** Platon, Aristoteles och Epiktetos är översatta direkt från grekiskan av Claude Opus 5.5 (Anthropic). Försokratikerna är översatta av ChatGPT 6.1 (OpenAI), delvis via John Burnets engelska. **Utgåvorna är arbetsversioner och är ännu inte externt fackgranskade.** Se `site/om.html` för metoden.

## Innehåll

| Verk | Källa (grekiska) | Stöd (engelska) |
|---|---|---|
| Platon: Sokrates försvarstal | Burnet 1905 (Perseus) | Fowler 1914 |
| Platon: Euthyfron | Burnet 1905 (Perseus) | Fowler 1914 |
| Platon: Kriton | Burnet 1905 (Perseus) | Fowler 1914 |
| Platon: Faidon | Burnet 1905 (Perseus) | Fowler 1914 |
| Aristoteles: Kategorierna | Bekker 1837 (First1KGreek) | Owen 1853 (kontroll); terminologi efter Lindén |
| Aristoteles: Om tolkningen | Bekker 1837 (First1KGreek), enligt underlaget | Owen 1853 |
| Marcus Aurelius: Självbetraktelser | Leopold 1908 (Perseus), enligt underlaget | Haines 1916 |
| Epiktetos: Handboken | Schenkl 1916 (Perseus) | Long 1890 |
| *Sokrates sista dagar* (samlingsvolym: de fyra Platondialogerna) | | |
| *Försokratikerna* (805 fragment och vittnesmål, 18 tänkare) | Diels 1903–1922 (The Presocratic Reader) | Burnet 1920 m.fl.; tio tänkare översatta via Burnets engelska |

Varje utgåva finns som webbsida, EPUB och PDF. **Undantag:** *Staten* har en PDF i ursprungligt A4-format; EPUB och HTML är rekonstruerade från denna. *Staten* innehåller bara böckerna I och II (av tio).

## Mappar

- `texter/` – de svenska källtexterna i markdown (en rad per stycke, `## N` = Stephanus-sida eller kapitel), `forsokratiker.json` (fragmentutgåvan med grekiska, stödöversättningar och svenska per post), plus `om.md` och `rattelser.md`
- `config.json` – utgåvans uppgifter: version, granskningsstatus, ISBN, utgivare, adresser
- `build.py`, `mallar/`, `filter/` – bygger allt med pandoc och XeLaTeX
- `site/` – den färdiga webbplatsen (publiceras med GitHub Pages)
- `jamforelse/` – underlaget för att jämföra översättningsmodeller: grekiska, engelska och svensk referens sida för sida, prompter, ordlistor och skript (se `jamforelse/LASMIG.md`)

## Ny portal och logo

- Webbplats: `site/index.html` och `site/portal.css` med responsiv bokkatalog, sökning och läslägen.
- Logotyp: `site/assets/brand-mark.svg`, `site/assets/logo-horizontal.svg` samt PNG-varianter.
- GitHub-organisationsprofil: `org-profile/profile/README.md` och profilbilden som hör dit.
- *Staten*, bok I–II: original-PDF i `site/nedladdning/`, en från PDF-textlagret rekonstruerad EPUB, en webbläsarutgåva och ett bearbetningsbart Markdown-utdrag i `texter/`.
- PDF-textlagrets rekonstruerade lästext bör kontrolleras mot PDF vid exakta citat.

## Bygga

```
python3 build.py            # böcker + webbplats
python3 build.py --bara-site
python3 scripts/enhance_site.py  # behöver BeautifulSoup4; kör sist
```

Kräver pandoc ≥ 3, Pillow och antingen XeLaTeX eller WeasyPrint.
Cardo-teckensnitt med OFL-licens finns i `mallar/fonts/`. Befintliga omslag
bevaras vid ombyggnad; nya omslag använder Cardo.

Så länge `"granskad": false` i `config.json` märks alla filer som granskningsexemplar och får filnamnet `-granskning`. Sätt `true` när texten är genomläst.

## Rättelser

Skapa ett ärende (issue) med verk, sida och mening, eller mejla adressen i `config.json`.

## Licens

Texterna: [CC BY-SA 4.0](LICENSE). Den grekiska texten till Platon och Epiktetos kommer från [Perseus Digital Library](https://github.com/PerseusDL/canonical-greekLit), Tufts University. Försokratikernas grundtext kommer från [The Presocratic Reader](https://github.com/sergiubisceanu/presocratic-reader) (Sergiu Alexandru Bîsceanu) med transkriptioner från Open Greek and Latin / First1KGreek, Forage och Perseus. Båda används under samma licens. De engelska stödöversättningarna är fria från upphovsrätt. Byggskripten får användas fritt.

### Publicering

Se `PUBLICERA_GITHUB.md` för steg för steg om repository, organisationens profil och Pages. Ingen GitHub-publicering sker automatiskt när ZIP-arkivet packas upp.

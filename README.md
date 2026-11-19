# Fria klassiker

Antik filosofi på modern svenska, fritt att läsa, kopiera och dela.

**Alla texter är AI-översättningar.** Platon och Epiktetos är översatta direkt från grekiskan av Claude Opus 5.5 (Anthropic). Försokratikerna är översatta av ChatGPT 6.1 (OpenAI), delvis via John Burnets engelska. Alla texter granskas av en människa innan de publiceras. Se `site/om.html` för metoden.

## Innehåll

| Verk | Källa (grekiska) | Stöd (engelska) |
|---|---|---|
| Platon: Sokrates försvarstal | Burnet (Perseus; TEI-metadata 1905) | Fowler 1914 |
| Platon: Kriton | Burnet (Perseus; TEI-metadata 1905) | Fowler 1914 |
| Platon: Faidon | Burnet (Perseus; TEI-metadata 1905) | Fowler 1914 |
| Epiktetos: Handboken | Schenkl 1916 (Perseus) | Long 1890 |
| *Sokrates sista dagar* (samlingsvolym: de tre Platondialogerna) | | |
| *Försokratikerna* (805 fragment och vittnesmål, 18 tänkare) | Diels 1903–1922 (The Presocratic Reader) | Burnet 1920 m.fl.; tio tänkare översatta via Burnets engelska |

Varje verk finns som webbsida, EPUB och PDF (A5).

## Mappar

- `texter/` – de svenska källtexterna i markdown (en rad per stycke, `## N` = Stephanus-sida eller kapitel), `forsokratiker.json` (fragmentutgåvan med grekiska, stödöversättningar och svenska per post), plus `om.md` och `rattelser.md`
- `config.json` – utgåvans uppgifter: version, granskningsstatus, ISBN, utgivare, adresser
- `build.py`, `mallar/`, `filter/` – bygger allt med pandoc och XeLaTeX
- `site/` – den färdiga webbplatsen (publiceras med GitHub Pages)
- `jamforelse/` – underlaget för att jämföra översättningsmodeller: grekiska, engelska och svensk referens sida för sida, prompter, ordlistor och skript (se `jamforelse/LASMIG.md`)

## Bygga

```
python3 build.py            # böcker + webbplats
python3 build.py --bara-site
```

Kräver pandoc ≥ 3, Pillow och antingen XeLaTeX eller WeasyPrint.
På den förberedda Mac-installationen används WeasyPrint. Cardo-teckensnitten
ligger i `mallar/fonts/` med sin OFL-licens; PDF-bygget fungerar även utan TeX Live.

Så länge `"granskad": false` i `config.json` märks alla filer som granskningsexemplar och får filnamnet `-granskning`. Sätt `true` när texten är genomläst.

GitHub Pages-arbetsflödet startas manuellt efter publiceringsbeslut, inte vid push.
ISBN och DOI är tomma tills riktiga identifierare har tilldelats. Modellnamnen
återger levererat underlag och är inte verifierade mot oberoende API-loggar.

## Rättelser

Skapa ett ärende (issue) med verk, sida och mening, eller mejla adressen i `config.json`.

## Licens

Texterna: [CC BY-SA 4.0](LICENSE). Den grekiska texten till Platon och Epiktetos kommer från [Perseus Digital Library](https://github.com/PerseusDL/canonical-greekLit), Tufts University. Försokratikernas grundtext kommer från [The Presocratic Reader](https://github.com/sergiubisceanu/presocratic-reader) (Sergiu Alexandru Bîsceanu) med transkriptioner från Open Greek and Latin / First1KGreek, Forage och Perseus. Båda används under samma licens. De engelska stödöversättningarna är fria från upphovsrätt. Byggskripten får användas fritt.

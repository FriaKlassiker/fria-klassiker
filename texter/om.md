# Om översättningarna

{serie} är ett projekt för att göra antikens filosofiska texter fritt tillgängliga på modern svenska. Många av de viktigaste texterna finns bara i äldre svenska översättningar, eller i nyare som är upphovsrättsskyddade och svåra att få tag på. Här kan alla läsa, ladda ned, skriva ut och dela texterna utan kostnad.

## Det här är AI-översättningar

Alla texter på webbplatsen har översatts av en språkmodell, inte av en mänsklig översättare. Vi säger det tydligt i varje bok och på varje sida, eftersom läsaren ska veta vad den läser. {granskning}

Översättningarna kan innehålla fel. Använd dem för att läsa och förstå texterna, men citera en vetenskaplig utgåva om noggrannheten är avgörande, till exempel i en uppsats.

## Vilken modell har översatt vad?

- Platon (*Euthyfron*, *Sokrates försvarstal*, *Kriton*, *Faidon*) och Epiktetos (*Handboken*): Claude Opus 5.5 (Anthropic), direkt från grekiskan med äldre engelsk översättning som stöd.
- Aristoteles (*Kategorierna* och *Om tolkningen*): Claude Opus 5.5 (Anthropic), direkt från grekiskan och kontrollerad mot Owens engelska (1853), med terminologi efter Mikael Lindéns översättning av Metafysiken. *Om tolkningen* följer också terminologin i seriens *Kategorierna*.
- Marcus Aurelius (*Självbetraktelser*): Claude Opus 5.5 (Anthropic), direkt från grekiskan och kontrollerad mot C. R. Haines engelska (1916). Stoisk terminologi samordnad med Epiktetos *Handboken*.
- Epiktetos (*Samtal*, Arrianos inledning och böckerna I–III): **Gemma 4 31B, lokalt finjusterad** (Fria klassiker LoRA v1), översatt **via George Longs engelska** översättning (1890), alltså inte direkt från grekiskan. Bok IV är ännu inte färdigställd.
- *Försokratikerna*: ChatGPT 6.1 (OpenAI). För tio av de arton tänkarna är översättningen gjord från John Burnets engelska översättning (1920), alltså via engelskan. För de övriga från den grekiska eller latinska texten med äldre översättningar som stöd. Varje fragment anger vad det bygger på.

## Så gick det till

1. **Grekisk originaltext.** Vi utgår från vedertagna textutgåvor: för Platon John Burnets Oxfordutgåva via Perseus Digital Library, för försokratikerna Hermann Diels *Die Fragmente der Vorsokratiker* via The Presocratic Reader.
2. **Engelskt stöd.** Den grekiska texten parades ihop, sida för sida, med en äldre engelsk översättning som är fri från upphovsrätt. Den engelska texten är bara ett stöd för förståelsen; översättningen görs från grekiskan. Undantagen är de försokratiker som översatts från Burnets engelska, och Epiktetos *Samtal*, som i sin helhet är översatt från Longs engelska av en lokalt finjusterad Gemma 4 31B; se ovan.
3. **Fast terminologi.** En ordlista med bärande begrepp (till exempel ψυχή – själ, φρόνησις – insikt, οὐσία – väsen, εἶδος – form) gavs till modellen så att samma grekiska ord översätts på samma sätt genom hela texten. Försokratikerna har en egen ordlista, som finns sist i boken.
4. **Översättning avsnitt för avsnitt.** Modellen översatte en Stephanus-sida, ett kapitel eller ett fragment i taget och fick inte utelämna eller lägga till något.
5. **Granskning.** Böckerna är publicerade som tydligt märkta granskningsexemplar och ännu inte externt fackgranskade. Läsare kan rapportera fel, och rättelser tas in i nya utgåvor.

## Varför

Projektet är också ett test av hur väl språkmodeller klarar svår prosa på svenska, och av öppna modeller jämfört med stängda. Underlaget för den jämförelsen, alltså grekisk text, engelsk text och svensk referensöversättning sida för sida, finns fritt tillgängligt i projektets arkiv.

## Licens och källor

Översättningarna ges ut under licensen [Creative Commons Erkännande-DelaLika 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.sv). Du får kopiera, sprida, skriva ut och bearbeta dem, även kommersiellt, om du anger källan och delar vidare under samma licens.

Den grekiska texten till Platon och Epiktetos kommer från [Perseus Digital Library](https://www.perseus.tufts.edu/) vid Tufts University (CC BY-SA 4.0). Försokratikernas grundtext kommer från [The Presocratic Reader](https://sergiubisceanu.github.io/presocratic-reader/) av Sergiu Alexandru Bîsceanu, med transkriptioner från Open Greek and Latin / First1KGreek, Forage och Perseus (CC BY-SA 4.0). Alla stödöversättningar, bland andra H. N. Fowler 1914, George Long 1890, Octavius Freire Owen 1853, John Burnet 1920, Hermann Diels 1922 och R. D. Hicks 1925, är fria från upphovsrätt.

Utgivare: {utgivare}. Kontakt: {kontakt_epost}. Källfiler: [{repo_url}]({repo_url}).

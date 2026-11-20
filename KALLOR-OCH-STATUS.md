# Källor och status för granskningsversionen

Denna utgåva är en AI-framställd granskningsversion. Varken en
klassikergranskning eller en fullständig mänsklig sakgranskning har bekräftats.
ISBN och DOI lämnas tomma tills verkliga identifierare har tilldelats.

Modellnamnen Claude Opus 5.5 och ChatGPT 6.1 återger uppgifter i det levererade
underlaget. De har inte verifierats mot råa API-loggar. De fyra parallellfilerna
innehåller 153 avsnitt, cirka 40 321 grekiska ord, 52 810 engelska ord och
50 927 svenska ord. Fragmentutgåvan innehåller ytterligare 805 poster.

## Grekiska texter och digitala transkriptioner

- Perseus Digital Library, Tufts University:
  https://github.com/PerseusDL/canonical-greekLit
- Licens: repositoryts `license.md` anger CC BY-SA 4.0.
- The Presocratic Reader, Sergiu Alexandru Bîsceanu:
  https://github.com/sergiubisceanu/presocratic-reader
- Dess `site/licences.txt` skiljer textdata/transkriptioner under CC BY-SA 4.0
  från historiska översättningar, som behåller sin angivna status.
- Individuella källor och översättningsvägar finns i `texter/forsokratiker.json`.
  Burnet-baserade svenska poster får inte beskrivas som direktöversättningar
  från grekiskan.

För de fyra huvudverken har hela den grekiska textströmmen kontrollerats mot
Perseus revision `dacb04909e43dc47738828d33cc3d2b0635bc54c`. Efter normalisering
av bokstavsform och skiljetecken, och exkludering av redaktionella
`del`/`bibl`/`note`-element, överensstämmer hela texten i samtliga fyra verk.
Detta är en maskinell källkontroll, inte en filologisk granskning.

Sidpaketen har delvis andra styckegränser än TEI-utgåvans sidindelning.
Exakta Stephanus-bokstäver och citatgränser ska därför kontrolleras i
originalet. Kitets etikett Oxford 1903 har för de tre Platondialogerna
ersatts med den kontrollerade TEI-källans metadata, Oxford 1905.

## Kategorierna – mänskligt granskad utgåva 1.0

Utgåvan av *Kategorierna* är den första i serien som granskats av en
människa. Hela texten har granskats av David Vesterlund (november 2026).
Rättat vid granskningen: ποσόν återges med *hur mycket* (tidigare
*mängd*), kategorin ἔχειν med *att ha* (tidigare *innehav*, som nu bara
används för ἕξις) och διωρισμένον med *åtskilt* (tidigare *avgränsad*).
Detta är utgivarens egen granskning, inte en extern filologisk
granskning, och utgåvan ersätter inte en vetenskaplig edition.

Granskningsjämförelse: webbtexten har uppdaterats från den granskade
EPUB-utgåvan, och en normaliserad jämförelse mot föregående utgåva
visar att skillnaderna är exakt de tre dokumenterade rättningarna.
PDF- och EPUB-filerna är de av utgivaren levererade utgåvorna
(2026-11-20); byggskripten skriver aldrig över dem
(`levererade_filer` i `config.json`). Filnamnen saknar
`-granskning`-suffixet eftersom utgåvan är granskad.

Kända skillnader i den levererade PDF:en: kolofonen uppgiver
fortfarande *Mikael Lindéns* (rätt uppgift är Jan-Ivar Lindén; webben
och EPUB:en är rättade), länken för senaste version pekar på repot i
stället för webbplatsen, och utgåvenumret är 1.0 medan serien i övrigt
ligger på 0.9. Felrapportering och rättelser tas in i nästa utgåva.

## Epiktetos Samtal – översättningsväg

Utgåvan omfattar Arrianos inledning och böckerna I–III; bok IV är ännu inte
färdigställd och pågår i den lokala översättningskön. Den svenska texten är
en AI-arbetsutgåva som översatts från George Longs engelska översättning
(London 1890, fri från upphovsrätt) av en lokalt finjusterad Gemma 4 31B
(Fria klassiker LoRA v1). Den får inte beskrivas som direktöversättning från
grekiskan. Grekisk jämförelsetext från Perseus Digital Library
(canonical-greekLit, tlg0557.tlg001, samma revision som ovan) är bevarad i
arbetsmaterialet utanför bokrepot. Kapitelindelningen följer den digitala
utgåvans bok- och kapitelstruktur. Texten är inte mänskligt granskad;
automatiska kontroller kan inte säkerställa betydelsetrohet.

## Losacco-uppgiften

Checklistans tidigare oklarhet om Michele Losaccos dödsår har utretts.
Stefano Miccolis artikel i *Dizionario Biografico degli Italiani*, vol. 66
(Treccani, 2006), anger att Losacco dog den 10 mars **1944**:

https://www.treccani.it/enciclopedia/michele-losacco_(Dizionario-Biografico)/

Detta placerar den namngivna historiska översättaren utanför den vanliga
livstid-plus-70-årsperioden. Det är inte en garanti om varje senare utgåva
eller varje jurisdiktion. De två berörda posterna är DK 7 B 1a och DK 7 B 6.

## Publicering och modellträning är olika frågor

CC-licensen för antika texter och digitala transkriptioner avgör inte i sig vilka
avtalsvillkor som gäller för AI-genererade referensöversättningar.
OpenAI och Anthropic beskriver ägande av output, men har också begränsningar
för användning av output till konkurrerande modeller. Exakt tillämpligt avtal,
kontotyp och tillåtet användningsfall måste bedömas separat. Den lokala
specialiserade adapterstudien är inte ett besked om generell rätt att distribuera
träningsmodeller under textlicensen.

- https://openai.com/policies/row-terms-of-use/
- https://www.anthropic.com/legal/commercial-terms
- https://support.claude.com/en/articles/12326764-can-i-use-my-outputs-to-train-an-ai-model

Ingen automatisk publicering av modellvikter ingår i detta bokrepo.
Den separata ordlistan från Lindéns *Metafysik* har inte kopierats hit eller
använts som ett fristående träningsdataset.

## Typsnitt

Cardo av David J. Perry används under SIL Open Font License 1.1.
Fontfiler och full licens finns i `mallar/fonts/`.

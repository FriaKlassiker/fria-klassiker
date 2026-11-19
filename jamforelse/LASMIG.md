# Kriton-piloten

kriton_pilot.jsonl – 12 Stephanus-sidor (43–54): grekiska (Burnet), engelska (Fowler 1914), sv_claude (referensöversättning av Claude, 2026-11-19, gjord från grekiskan med engelskan som stöd och samma ordlista).
kriton_sv_claude.md – samma svenska text att läsa i sin helhet.
prompt_sv.txt + glossary_kriton.txt – exakt den prompt de öppna modellerna ska få (samma förutsättningar som Claude hade).
run_model.py – kör en modell via OpenAI-kompatibelt API (vLLM/llama.cpp/Ollama). --no-english ger ablationen "bara grekiska".
evaluate.py – chrF++ mot referensen, längdkvot, repliktal och ordlistetermer per sida. Byt referens med --ref-field när Bergman 1918 är inlagd.

Exempel:
  python3 run_model.py --base-url http://localhost:8000/v1 --model Qwen3-32B --out sv_qwen.jsonl
  python3 run_model.py --base-url http://localhost:8000/v1 --model Qwen3-32B --out sv_qwen_utan_eng.jsonl --no-english
  pip install sacrebleu && python3 evaluate.py sv_qwen.jsonl sv_qwen_utan_eng.jsonl

Obs: chrF mot Claude mäter likhet med Claude, inte kvalitet i sig. Komplettera med blind manuell bedömning
(tillräckligt: 3 sidor × modeller, betyg 1–5 för trohet och svenska) och, när den finns, Bergman 1918 som oberoende referens.
Licens: grekiska och engelska från Perseus (CC BY-SA 4.0); de svenska texterna släpps under samma licens.

## Epiktetos, Handboken (andra piloten)
epiktetos_pilot.jsonl – 53 kapitel: grekiska (Schenkl 1916), engelska (George Long 1890), sv_claude.
epiktetos_handbok_sv_claude.md – hela den svenska texten. prompt_sv_epiktetos.txt + glossary_epiktetos.txt – prompten.
  python3 run_model.py --base-url ... --model ... --out sv_X_epik.jsonl --data epiktetos_pilot.jsonl --prompt prompt_sv_epiktetos.txt --glossary glossary_epiktetos.txt
  python3 evaluate.py sv_X_epik.jsonl --ref epiktetos_pilot.jsonl
Kapitel 53 innehåller citat (Kleanthes, Euripides, Platons Kriton 43d och Försvarstalet 30c).

## Platon, Sokrates försvarstal (tredje piloten)
forsvarstalet_pilot.jsonl – 26 Stephanus-sidor (17–42): grekiska (Burnet), engelska (Fowler 1914), sv_claude.
platon_forsvarstalet_sv_claude.md – hela texten. Hakparenteserna [Domstolen har funnit Sokrates skyldig] m.fl. är läsanvisningar
som inte finns i grekiskan; de är borttagna i jsonl-filen så att jämförelsen blir rättvis.
  python3 run_model.py --base-url ... --model ... --out sv_X_apol.jsonl --data forsvarstalet_pilot.jsonl --prompt prompt_sv_forsvarstalet.txt --glossary glossary_forsvarstalet.txt
  python3 evaluate.py sv_X_apol.jsonl --ref forsvarstalet_pilot.jsonl
Försvarstalet, Kriton och Faidon bildar Platons serie om Sokrates rättegång och död.

## Platon, Faidon (fjärde piloten)
faidon_pilot.jsonl – 62 Stephanus-sidor (57–118): grekiska (Burnet), engelska (Fowler 1914), sv_claude.
platon_faidon_sv_claude.md – hela texten, ca 27 600 ord. prompt_sv_faidon.txt + glossary_faidon.txt – prompten.
  python3 run_model.py --base-url ... --model ... --out sv_X_faidon.jsonl --data faidon_pilot.jsonl --prompt prompt_sv_faidon.txt --glossary glossary_faidon.txt
  python3 evaluate.py sv_X_faidon.jsonl --ref faidon_pilot.jsonl
Faidon är den svåraste av de fyra: långa argumentkedjor (formläran, själens odödlighet) och en myt om jordens inre (108–114).
Sidorna är långa (ofta 2 000+ tecken grekiska), så kontrollera att modellens kontextlängd och max_tokens räcker.

Hela serien: Försvarstalet → Kriton → Faidon (Sokrates rättegång, fängelse och död), plus Epiktetos Handbok.
Totalt ca 51 000 ord svensk referenstext.

"""Jämför en eller flera modellöversättningar med referensen (Claude, eller Bergman 1918 när den finns).
Användning: python3 evaluate.py sv_modellA.jsonl [sv_modellB.jsonl ...] [--ref kriton_pilot.jsonl --ref-field sv_claude]
Mått per sida: chrF++ mot referensen, längdkvot mot grekiskan, antal repliker (talarrader) jämfört med originalet,
och träffar på ordlistetermer."""
import argparse, json, re
from sacrebleu.metrics import CHRF
ap = argparse.ArgumentParser(); ap.add_argument('hyps', nargs='+')
ap.add_argument('--ref', default='kriton_pilot.jsonl'); ap.add_argument('--ref-field', default='sv_claude')
a = ap.parse_args()
ref = {json.loads(l)['ref']: json.loads(l) for l in open(a.ref, encoding='utf-8')}
chrf = CHRF(word_order=2)
TERMS = ['åsikt', 'de många', 'sakkunnig', 'orätt', 'dygd', 'rättvis', 'lagarna', 'fäderneslandet', 'överenskommelse', 'angivar',
         'i vår makt', 'viljeinriktning', 'intryck', 'omdöme', 'begär', 'undvikande', 'sinnesro', 'lekman', 'framsteg', 'styrande förnuft']
spk = lambda t: len(re.findall(r'^(SOKRATES|KRITON|ΣΩ|ΚΡ)[:.]', t, re.M))
for h in a.hyps:
    hyp = {json.loads(l)['ref']: json.loads(l)['sv'] for l in open(h, encoding='utf-8')}
    print(f'\n=== {h}  (referens: {a.ref_field})')
    print(f"{'sida':>4} {'chrF++':>7} {'längd/grc':>9} {'repliker':>9} {'termer':>7}")
    H, R = [], []
    for k, r in ref.items():
        s = hyp.get(k, ''); H.append(s); R.append(r[a.ref_field])
        sc = chrf.sentence_score(s, [r[a.ref_field]]).score
        print(f"{k:>4} {sc:7.1f} {len(s)/len(r['grc']):9.2f} {spk(s):>4}/{spk(r['grc']):<4} "
              f"{sum(t in s.lower() for t in TERMS):>3}/{sum(t in r[a.ref_field].lower() for t in TERMS)}")
    print(f"Totalt chrF++: {chrf.corpus_score(H, [R]).score:.1f}")

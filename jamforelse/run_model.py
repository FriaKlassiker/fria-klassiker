"""Översätt Kriton sida för sida med en open-weights-modell via ett OpenAI-kompatibelt API (vLLM, llama.cpp-server, Ollama m.fl.).
Användning: python3 run_model.py --base-url http://localhost:8000/v1 --model NAMN --out sv_NAMN.jsonl
  Epiktetos: lägg till --data epiktetos_pilot.jsonl --prompt prompt_sv_epiktetos.txt --glossary glossary_epiktetos.txt
"""
import argparse, json, urllib.request
ap = argparse.ArgumentParser()
ap.add_argument('--base-url', required=True); ap.add_argument('--model', required=True)
ap.add_argument('--out', required=True); ap.add_argument('--api-key', default='EMPTY')
ap.add_argument('--no-english', action='store_true', help='ablation: endast grekiska i prompten')
ap.add_argument('--temperature', type=float, default=0.2)
ap.add_argument('--data', default='kriton_pilot.jsonl')
ap.add_argument('--prompt', default='prompt_sv.txt')
ap.add_argument('--glossary', default='glossary_kriton.txt')
a = ap.parse_args()
tmpl = open(a.prompt, encoding='utf-8').read(); gl = open(a.glossary, encoding='utf-8').read()
with open(a.out, 'w', encoding='utf-8') as fo:
    for line in open(a.data, encoding='utf-8'):
        r = json.loads(line)
        prompt = tmpl.format(glossary=gl, ref=r['ref'], grc=r['grc'], eng='(utelämnad)' if a.no_english else r['eng'])
        body = json.dumps({'model': a.model, 'temperature': a.temperature, 'max_tokens': 4096,
                           'messages': [{'role': 'user', 'content': prompt}]}).encode()
        req = urllib.request.Request(a.base_url.rstrip('/') + '/chat/completions', data=body,
                                     headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + a.api_key})
        out = json.load(urllib.request.urlopen(req, timeout=600))['choices'][0]['message']['content'].strip()
        fo.write(json.dumps({'ref': r['ref'], 'sv': out}, ensure_ascii=False) + '\n'); fo.flush()
        print(r['ref'], len(out))

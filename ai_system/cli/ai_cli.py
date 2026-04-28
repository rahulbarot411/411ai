#!/usr/bin/env python3
import json, sys, httpx
prompt = ' '.join(sys.argv[1:]).strip()
if not prompt:
    print('usage: ai-cli "prompt"')
    raise SystemExit(1)
with httpx.stream('POST','http://localhost:8080/api/chat',json={'message':prompt}) as r:
    for line in r.iter_lines():
        if not line or not line.startswith('data: '):
            continue
        obj = json.loads(line[6:])
        if obj.get('delta'):
            print(obj['delta'], end='', flush=True)
print()

#!/usr/bin/env python3
"""Upload 20 counseling infographics to Supabase Storage + write inf-coun.json."""
import json, os, requests

BASE = '/home/hatch/workspace/zehen/batch4'
env = {}
with open('/home/hatch/workspace/zehen/.env.supabase') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env[k] = v
URL, KEY = env['SUPABASE_URL'], env['SUPABASE_SECRET_KEY']
H = {'apikey': KEY, 'Authorization': f'Bearer {KEY}'}

items = json.load(open(os.path.join(BASE, 'coun-takeaways.json')))
out = []
fails = []
for i, it in enumerate(items, 1):
    fname = f'coun-{i:02d}.png'
    path = os.path.join(BASE, 'inf-coun-png', fname)
    with open(path, 'rb') as fh:
        data = fh.read()
    r = requests.put(
        f'{URL}/storage/v1/object/infographics/{fname}',
        headers={**H, 'Content-Type': 'image/png', 'x-upsert': 'true'},
        data=data, timeout=60)
    if r.status_code in (200, 201):
        pub = f'{URL}/storage/v1/object/public/infographics/{fname}'
        out.append({'file': pub, 'title': it['title'], 'topic': 'Counseling & Therapy'})
        print('ok', fname, len(data)//1024, 'KB', flush=True)
    else:
        fails.append(fname)
        print('FAIL', fname, r.status_code, r.text[:150], flush=True)

json.dump(out, open(os.path.join(BASE, 'inf-coun.json'), 'w'), indent=1)
print('saved inf-coun.json:', len(out))
print('failures:', fails)

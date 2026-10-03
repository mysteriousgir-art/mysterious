#!/usr/bin/env python3
"""Upload 20 Social Psychology infographics to Supabase storage + write inf-soc.json."""
import json, os, requests

BASE = os.path.dirname(os.path.abspath(__file__))
env = {}
with open(os.path.expanduser('~/workspace/zehen/.env.supabase')) as f:
    for line in f:
        line = line.strip()
        if line and '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

URL = env['SUPABASE_URL'].rstrip('/')
KEY = env['SUPABASE_SECRET_KEY']
h_up = {
    'apikey': KEY,
    'Authorization': 'Bearer ' + KEY,
    'Content-Type': 'image/png',
    'x-upsert': 'true',
}

items = json.load(open(os.path.join(BASE, 'soc-takeaways.json')))['items']
ok, fail = [], []
for n, it in enumerate(items, 1):
    fname = 'soc-%d.png' % n
    path = os.path.join(BASE, 'inf-soc-out', fname)
    with open(path, 'rb') as f:
        data = f.read()
    r = requests.put(
        '%s/storage/v1/object/infographics/%s' % (URL, fname),
        headers=h_up, data=data, timeout=90)
    if r.status_code in (200, 201):
        pub = '%s/storage/v1/object/public/infographics/%s' % (URL, fname)
        ok.append({'file': pub, 'title': it['title'], 'topic': 'Social Psychology'})
        print('UP', fname, r.status_code, flush=True)
    else:
        fail.append(fname)
        print('FAIL', fname, r.status_code, r.text[:200], flush=True)

json.dump(ok, open(os.path.join(BASE, 'inf-soc.json'), 'w'), indent=1)
print('OK:', len(ok), 'FAIL:', len(fail), fail)

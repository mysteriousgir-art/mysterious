#!/usr/bin/env python3
"""Upload 20 org infographics to Supabase Storage + build inf-org.json manifest."""
import json, os, requests

BASE = '/home/hatch/workspace/zehen/batch4'
OUT_DIR = BASE + '/inf-org-out'

env = {}
with open(BASE + '/../.env.supabase') as f:
    for line in f:
        line = line.strip()
        if line and '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            env[k.strip()] = v.strip()

URL = env['SUPABASE_URL']
KEY = env['SUPABASE_SECRET_KEY']
H = {'apikey': KEY, 'Authorization': 'Bearer ' + KEY, 'Content-Type': 'image/png'}

manifest_src = json.load(open(BASE + '/org-manifest.json'))
results = []
ok, fail = 0, 0
for m in manifest_src:
    fname = m['file']
    path = os.path.join(OUT_DIR, fname)
    with open(path, 'rb') as fh:
        data = fh.read()
    r = requests.put(
        '%s/storage/v1/object/infographics/%s' % (URL, fname),
        headers=H, data=data, timeout=120)
    if r.status_code in (200, 201):
        pub = '%s/storage/v1/object/public/infographics/%s' % (URL, fname)
        results.append({'file': pub, 'title': m['title'], 'topic': 'Organizational Psychology'})
        ok += 1
        print('OK', fname, len(data) // 1024, 'KB', flush=True)
    else:
        fail += 1
        print('FAIL', fname, r.status_code, r.text[:150], flush=True)

json.dump(results, open(BASE + '/inf-org.json', 'w'), indent=1)
print('DONE ok=%d fail=%d manifest=%s/inf-org.json' % (ok, fail, BASE), flush=True)

// test/netlify-adapter.js — tests the Netlify catch-all adapter end to end.
// Simulates Netlify Function events (as produced by the /api/* -> /.netlify/functions/api/:splat
// rewrite in netlify.toml) and runs them against LIVE Supabase via .env.supabase.
// Usage: node test/netlify-adapter.js

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');

// ---- load .env.supabase (gitignored). NEVER prints secrets. ----
(function loadEnv() {
  const p = path.join(ROOT, '.env.supabase');
  if (!fs.existsSync(p)) { console.error('missing .env.supabase'); process.exit(1); }
  for (const line of fs.readFileSync(p, 'utf8').split('\n')) {
    const m = line.match(/^\s*([A-Z_]+)\s*=\s*(.*?)\s*$/);
    if (m) process.env[m[1]] = m[2];
  }
})();
const ADMIN_TEST_EMAIL = 'netlifytest-admin@example.com';
process.env.ADMIN_EMAIL = ADMIN_TEST_EMAIL;

const { handler, __test__ } = require('../netlify/functions/api.js');
const { createClient } = require('@supabase/supabase-js');
const sb = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_SECRET_KEY, { auth: { persistSession: false } });

let pass = 0, fail = 0;
const failures = [];
function ok(name, cond, extra) {
  if (cond) { pass++; console.log('  PASS ' + name); }
  else { fail++; failures.push(name); console.log('  FAIL ' + name + (extra ? ' -- ' + extra : '')); }
}
async function section(name, fn) {
  console.log('\n== ' + name + ' ==');
  try { await fn(); } catch (e) { fail++; failures.push(name + ' threw'); console.log('  FAIL ' + name + ' threw: ' + (e && e.message)); }
}

// Build a Netlify event as the redirect would produce it.
function ev({ method = 'GET', apiPath = '/api/health', query = {}, headers = {}, body = null }) {
  const splat = apiPath.replace(/^\/api\/?/, '');
  const h = Object.assign({ accept: 'application/json' }, headers);
  let b = null;
  if (body !== null && body !== undefined) {
    h['content-type'] = 'application/json';
    b = JSON.stringify(body);
  }
  return {
    httpMethod: method,
    path: '/.netlify/functions/api/' + splat,
    headers: h,
    queryStringParameters: query,
    multiValueQueryStringParameters: null,
    body: b,
    isBase64Encoded: false,
  };
}
function json(res) { try { return JSON.parse(res.body); } catch (e) { return null; } }
function cookieFrom(res) {
  const mv = res.multiValueHeaders || {};
  const arr = mv['Set-Cookie'] || [];
  const m = String(arr[0] || '').match(/mysterious_session=([^;]+)/);
  return m ? 'mysterious_session=' + m[1] : '';
}

(async () => {
  const TS = Date.now();
  const mkUser = (tag) => ({ email: `netlifytest-${tag}-${TS}@example.com`, password: 'testpass123', displayName: `Test ${tag}`, country: 'Pakistan' });
  const cookies = {};
  const createdIds = [];

  await section('route table', async () => {
    const { matchRoute } = __test__;
    const cases = [
      [['notes', 'abc'], 'api/notes/[slug].js', { slug: 'abc' }],
      [['notes', 'abc', 'read'], 'api/notes/[slug]/read.js', { slug: 'abc' }],
      [['notes'], 'api/notes/index.js', {}],
      [['quizzes', 'x', 'submit'], 'api/quizzes/[slug]/submit.js', { slug: 'x' }],
      [['blocks', '42'], 'api/blocks/[userId].js', { userId: '42' }],
      [['users', '7', 'public'], 'api/users/[id]/public.js', { id: '7' }],
      [['admin', 'users', '9', 'ban'], 'api/admin/users/[id]/ban.js', { id: '9' }],
      [['admin', 'reports', '3', 'resolve'], 'api/admin/reports/[id]/resolve.js', { id: '3' }],
      [['auth', 'signup'], 'api/auth/signup.js', {}],
      [['health'], 'api/health.js', {}],
    ];
    for (const [segs, wantFile, wantParams] of cases) {
      const m = matchRoute(segs);
      ok(
        'route /' + segs.join('/'),
        !!m && m.file.endsWith(wantFile.replace(/\//g, path.sep)) &&
          JSON.stringify(m.params) === JSON.stringify(wantParams),
        m ? m.file : 'no match'
      );
    }
    ok('unknown route -> null', matchRoute(['nope', 'nah']) === null);
  });

  await section('health + 404', async () => {
    let r = await handler(ev({ apiPath: '/api/health' }), {});
    ok('GET /api/health 200', r.statusCode === 200 && json(r).ok === true);
    r = await handler(ev({ method: 'POST', apiPath: '/api/health' }), {});
    ok('POST /api/health 405', r.statusCode === 405);
    r = await handler(ev({ apiPath: '/api/definitely-not-here' }), {});
    ok('unknown api path 404', r.statusCode === 404);
  });

  await section('auth: signup/login/me', async () => {
    let r = await handler(ev({ method: 'POST', apiPath: '/api/auth/signup', body: { email: ADMIN_TEST_EMAIL, password: 'testpass123', displayName: 'Test Admin', country: 'Pakistan' } }), {});
    let d = json(r);
    ok('admin signup 201', r.statusCode === 201, 'got ' + r.statusCode + ' ' + r.body.slice(0, 120));
    ok('admin promoted via ADMIN_EMAIL', d && d.user && d.user.isAdmin === true);
    ok('session cookie set (multiValueHeaders)', !!cookieFrom(r));
    cookies.admin = cookieFrom(r); createdIds.push(d.user.id);

    r = await handler(ev({ method: 'POST', apiPath: '/api/auth/signup', body: mkUser('b') }), {});
    d = json(r);
    ok('user B signup 201', r.statusCode === 201);
    cookies.b = cookieFrom(r); createdIds.push(d.user.id);
    const bId = d.user.id;

    r = await handler(ev({ method: 'POST', apiPath: '/api/auth/signup', body: mkUser('c') }), {});
    d = json(r);
    ok('user C signup 201', r.statusCode === 201);
    cookies.c = cookieFrom(r); createdIds.push(d.user.id);
    global.__cId = d.user.id; global.__bId = bId;

    r = await handler(ev({ method: 'POST', apiPath: '/api/auth/login', body: { email: mkUser('b').email, password: 'testpass123' } }), {});
    ok('login 200', r.statusCode === 200);

    r = await handler(ev({ apiPath: '/api/auth/me', headers: { cookie: cookies.b } }), {});
    ok('me with cookie 200', r.statusCode === 200 && json(r).user && json(r).user.displayName === 'Test b');

    r = await handler(ev({ apiPath: '/api/auth/me' }), {});
    ok('me without cookie 401', r.statusCode === 401);
  });

  await section('content: notes/quizzes', async () => {
    let r = await handler(ev({ apiPath: '/api/notes' }), {});
    let d = json(r);
    ok('notes list = 10', r.statusCode === 200 && Array.isArray(d) && d.length === 10, 'got ' + (Array.isArray(d) ? d.length : typeof d));

    const slug = d[0].slug;
    r = await handler(ev({ apiPath: '/api/notes/' + slug }), {});
    ok('note detail 200 (dynamic :slug)', r.statusCode === 200 && json(r).note && json(r).note.slug === slug);

    r = await handler(ev({ method: 'POST', apiPath: '/api/notes/' + slug + '/read', headers: { cookie: cookies.b } }), {});
    ok('note read 200 +xp', r.statusCode === 200, 'got ' + r.statusCode);

    r = await handler(ev({ apiPath: '/api/quizzes' }), {});
    d = json(r);
    ok('quizzes list = 5', r.statusCode === 200 && Array.isArray(d) && d.length === 5);

    const qslug = d[0].slug;
    const { data: qrow } = await sb.from('quizzes').select('questions_json').eq('slug', qslug).single();
    const questions = typeof qrow.questions_json === 'string' ? JSON.parse(qrow.questions_json) : qrow.questions_json;
    const answers = questions.map(() => 0);
    r = await handler(ev({ method: 'POST', apiPath: '/api/quizzes/' + qslug + '/submit', headers: { cookie: cookies.b }, body: { answers } }), {});
    d = json(r);
    ok('quiz submit 200 + score', r.statusCode === 200 && typeof d.score === 'number', 'got ' + r.statusCode);
  });

  await section('xp: checkin + leaderboard', async () => {
    let r = await handler(ev({ method: 'POST', apiPath: '/api/checkin', headers: { cookie: cookies.b } }), {});
    ok('checkin 200', r.statusCode === 200, 'got ' + r.statusCode);
    r = await handler(ev({ apiPath: '/api/leaderboard' }), {});
    ok('leaderboard 200', r.statusCode === 200 && Array.isArray(json(r)));
  });

  await section('chat: send + poll (adapter path params)', async () => {
    let r = await handler(ev({ method: 'POST', apiPath: '/api/chat/send', headers: { cookie: cookies.b }, body: { type: 'room', id: 'general', body: 'hello from adapter test' } }), {});
    ok('room send 201', r.statusCode === 201, 'got ' + r.statusCode + ' ' + String(r.body).slice(0, 120));

    r = await handler(ev({ apiPath: '/api/chat/messages', query: { type: 'room', id: 'general', since: '0' }, headers: { cookie: cookies.b } }), {});
    const msgs = (json(r) || {}).messages || [];
    ok('room poll returns message', r.statusCode === 200 && msgs.some((m) => m.body === 'hello from adapter test'));
  });

  await section('blocks via adapter', async () => {
    const cId = global.__cId;
    let r = await handler(ev({ method: 'POST', apiPath: '/api/blocks', headers: { cookie: cookies.b }, body: { userId: cId } }), {});
    ok('B blocks C 201', r.statusCode === 201, 'got ' + r.statusCode);

    r = await handler(ev({ method: 'POST', apiPath: '/api/chat/send', headers: { cookie: cookies.c }, body: { type: 'room', id: 'general', body: 'C says hi' } }), {});
    ok('C room send 201', r.statusCode === 201);

    r = await handler(ev({ apiPath: '/api/chat/messages', query: { type: 'room', id: 'general', since: '0' }, headers: { cookie: cookies.b } }), {});
    const msgsB = ((json(r) || {}).messages || []);
    ok("blocker's poll hides C", r.statusCode === 200 && !msgsB.some((m) => m.body === 'C says hi'));

    r = await handler(ev({ method: 'DELETE', apiPath: '/api/blocks/' + cId, headers: { cookie: cookies.b } }), {});
    ok('unblock via /api/blocks/:userId 200', r.statusCode === 200, 'got ' + r.statusCode);
  });

  await section('admin guards via adapter', async () => {
    let r = await handler(ev({ apiPath: '/api/admin/stats', headers: { cookie: cookies.b } }), {});
    ok('non-admin stats 403', r.statusCode === 403);
    r = await handler(ev({ apiPath: '/api/admin/stats', headers: { cookie: cookies.admin } }), {});
    ok('admin stats 200', r.statusCode === 200 && typeof (json(r) || {}).totalUsers === 'number');
    r = await handler(ev({ apiPath: '/api/admin/backup', headers: { cookie: cookies.admin } }), {});
    ok('admin backup 200 json', r.statusCode === 200 && (r.headers['Content-Type'] || '').includes('application/json'));
  });

  await section('cleanup test data', async () => {
    const ids = createdIds;
    await sb.from('messages').delete().in('from_id', ids);
    await sb.from('sessions').delete().in('user_id', ids);
    await sb.from('quiz_attempts').delete().in('user_id', ids);
    await sb.from('note_reads').delete().in('user_id', ids);
    await sb.from('checkins').delete().in('user_id', ids);
    await sb.from('game_plays').delete().in('user_id', ids);
    await sb.from('blocks').delete().in('blocker_id', ids);
    await sb.from('reports').delete().in('reporter_id', ids);
    const { error } = await sb.from('users').delete().in('id', ids);
    ok('test users removed', !error);
  });

  console.log('\n==== RESULT: ' + pass + ' passed, ' + fail + ' failed ====');
  if (failures.length) console.log('failures: ' + failures.join(' | '));
  process.exit(fail ? 1 : 0);
})().catch((e) => { console.error('harness crashed:', e && e.message); process.exit(2); });

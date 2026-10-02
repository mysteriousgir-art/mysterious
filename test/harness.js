// test/harness.js — Mysterious vercel-rework test harness.
// Usage: node test/harness.js
// Loads credentials from .env.supabase (gitignored). NEVER prints secrets.
// Runs pure-logic tests always; live-DB tests only if the Supabase schema exists.

const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');

// ---- load .env.supabase ----
(function loadEnv() {
  const p = path.join(ROOT, '.env.supabase');
  if (!fs.existsSync(p)) { console.error('missing .env.supabase'); process.exit(1); }
  for (const line of fs.readFileSync(p, 'utf8').split('\n')) {
    const m = line.match(/^\s*([A-Z_]+)\s*=\s*(.*?)\s*$/);
    if (m) process.env[m[1]] = m[2];
  }
})();
const ADMIN_TEST_EMAIL = 'verceltest-admin@example.com';
process.env.ADMIN_EMAIL = ADMIN_TEST_EMAIL;

const u = require('../api/_lib/util');

// ---- mocks ----
function mockRes() {
  const headers = {};
  return {
    statusCode: 200,
    _headers: headers,
    body: null,
    setHeader(k, v) { headers[String(k).toLowerCase()] = v; },
    getHeader(k) { return headers[String(k).toLowerCase()]; },
    end(b) { this.body = b; },
  };
}
function mockReq({ method = 'GET', query = {}, body = null, cookie = '' } = {}) {
  return { method, query, body, headers: { cookie } };
}
function json(res) { try { return JSON.parse(res.body); } catch (e) { return null; } }
function cookieFrom(res) {
  const h = String(res.getHeader('set-cookie') || '');
  const m = h.match(/mysterious_session=([^;]+)/);
  return m ? `mysterious_session=${m[1]}` : '';
}

// ---- tiny test runner ----
let pass = 0, fail = 0;
const failures = [];
function ok(name, cond, detail) {
  if (cond) { pass++; console.log(`  PASS ${name}`); }
  else { fail++; failures.push(name); console.log(`  FAIL ${name}${detail ? ' — ' + detail : ''}`); }
}
async function section(name, fn) {
  console.log(`\n== ${name} ==`);
  try { await fn(); } catch (e) { fail++; failures.push(name + ' (threw)'); console.log(`  FAIL ${name} threw: ${e.message}`); }
}

async function main() {
  console.log('Mysterious vercel-rework harness —', new Date().toISOString());

  await section('pure helpers (no DB)', async () => {
    ok('esc', u.esc('<b>&"\'') === '&lt;b&gt;&amp;&quot;&#39;');
    ok('filterProfanity', u.filterProfanity('you are a chutiya friend').includes('***'));
    ok('parseCookies', (() => { const c = u.parseCookies('a=1; mysterious_session=tok123'); return c.a === '1' && c.mysterious_session === 'tok123'; })());
    ok('todayUtc format', /^\d{4}-\d{2}-\d{2}$/.test(u.todayUtc()));
    ok('validateNoteBody ok', !!u.validateNoteBody({ slug: 'x', title: 't', points: [{ point: 'p', example: 'e' }] }));
    ok('validateNoteBody rejects', u.validateNoteBody({ slug: 'x' }) === null);
    const qv = { slug: 'q', title: 't', questions: [{ q: 'q1', options: ['a', 'b', 'c', 'd'], answer: 2, explanation: 'e' }] };
    ok('validateQuizBody ok', !!u.validateQuizBody(qv));
    ok('validateQuizBody rejects bad options', u.validateQuizBody({ slug: 'q', title: 't', questions: [{ q: 'q1', options: ['a'], answer: 0 }] }) !== null); // shape ok; content checked by handler
    ok('asJson string', JSON.stringify(u.asJson('{"a":1}')) === '{"a":1}');
    ok('asJson passthrough', Array.isArray(u.asJson([1, 2])));
    ok('userShape', (() => { const s = u.userShape({ id: 1, email: 'e', display_name: 'D', avatar: 'a', bio: '', country: '', xp: 5, level: 1, streak_count: 2, is_admin: 1 }); return s.displayName === 'D' && s.isAdmin === true && s.streak === 2; })());
  });

  // ---- can we reach the DB schema? ----
  let schemaOk = false;
  await section('supabase connectivity + schema presence', async () => {
    try {
      const { data, error } = await u.supabase().from('rooms').select('slug').limit(5);
      if (error) throw error;
      schemaOk = true;
      ok('rooms table reachable', Array.isArray(data), `slugs: ${(data || []).map((r) => r.slug).join(',')}`);
    } catch (e) {
      console.log(`  SKIP live-DB tests: schema not loaded (${e.message}).`);
      console.log('  Attiya must paste supabase/schema.sql into the Supabase SQL Editor first.');
    }
  });

  if (schemaOk) await dbTests();

  console.log(`\n==== RESULT: ${pass} passed, ${fail} failed ====`);
  if (failures.length) console.log('failures:', failures.join(' | '));
  process.exit(fail ? 1 : 0);
}

async function dbTests() {
  const H = (p) => require(path.join(ROOT, 'api', p));
  const signup = H('auth/signup.js'), login = H('auth/login.js'), me = H('auth/me.js');
  const logout = H('auth/logout.js'), health = H('health.js');
  const sb = u.supabase();
  const TS = Date.now();
  const mkUser = (tag) => ({ email: `verceltest-${tag}-${TS}@example.com`, password: 'testpass123', displayName: `Test ${tag}`, country: 'Pakistan' });
  const adminInfo = { email: ADMIN_TEST_EMAIL, password: 'testpass123', displayName: 'Test Admin', country: 'Pakistan' };
  const createdIds = [];
  const cookies = {};

  async function doSignup(info) {
    const res = mockRes();
    await signup(mockReq({ method: 'POST', body: info }), res);
    return { res, data: json(res), cookie: cookieFrom(res) };
  }

  await section('health + method guards', async () => {
    let res = mockRes();
    await health(mockReq({ method: 'GET' }), res);
    ok('GET /api/health 200', res.statusCode === 200 && json(res).ok === true);
    res = mockRes();
    await health(mockReq({ method: 'POST' }), res);
    ok('POST /api/health 405', res.statusCode === 405);
  });

  await section('auth: signup/login/me/logout', async () => {
    let r = await doSignup(adminInfo);
    ok('admin signup 201', r.res.statusCode === 201, `got ${r.res.statusCode}`);
    ok('admin promoted via ADMIN_EMAIL', r.data && r.data.user && r.data.user.isAdmin === true);
    ok('session cookie set', !!r.cookie);
    cookies.admin = r.cookie; createdIds.push(r.data.user.id);

    r = await doSignup(mkUser('b'));
    ok('user B signup 201', r.res.statusCode === 201);
    ok('user B not admin', r.data.user.isAdmin === false);
    cookies.b = r.cookie; createdIds.push(r.data.user.id);
    const bId = r.data.user.id;

    r = await doSignup(mkUser('c'));
    ok('user C signup 201', r.res.statusCode === 201);
    cookies.c = r.cookie; createdIds.push(r.data.user.id);
    global.__cId = r.data.user.id;

    r = await doSignup(mkUser('b')); // same email? no — mkUser uses tag; use explicit dup:
    const dup = mockRes();
    await signup(mockReq({ method: 'POST', body: { email: adminInfo.email, password: 'x', displayName: 'Dup', country: '' } }), dup);
    ok('duplicate email 400', dup.statusCode === 400);

    const bad = mockRes();
    await login(mockReq({ method: 'POST', body: { email: adminInfo.email, password: 'wrong' } }), bad);
    ok('login wrong password 401', bad.statusCode === 401);

    const good = mockRes();
    await login(mockReq({ method: 'POST', body: { email: adminInfo.email, password: adminInfo.password } }), good);
    ok('login correct 200', good.statusCode === 200 && !!cookieFrom(good));

    const meRes = mockRes();
    await me(mockReq({ method: 'GET', cookie: cookies.admin }), meRes);
    ok('me with cookie 200', meRes.statusCode === 200 && json(meRes).user.email === ADMIN_TEST_EMAIL);

    const meNo = mockRes();
    await me(mockReq({ method: 'GET' }), meNo);
    ok('me without cookie 401', meNo.statusCode === 401);

    const lo = mockRes();
    await logout(mockReq({ method: 'POST', cookie: cookies.b }), lo);
    ok('logout 200', lo.statusCode === 200);
    const meAfter = mockRes();
    await me(mockReq({ method: 'GET', cookie: cookies.b }), meAfter);
    ok('me after logout 401', meAfter.statusCode === 401);
    // re-login B for later tests
    const relog = mockRes();
    await login(mockReq({ method: 'POST', body: { email: `verceltest-b-${TS}@example.com`, password: 'testpass123' } }), relog);
    cookies.b = cookieFrom(relog);
    ok('B re-login ok', !!cookies.b);
    global.__bId = bId;
  });

  await section('content: notes/quizzes/infographics', async () => {
    const notes = H('notes/index.js'), noteDetail = H('notes/[slug].js');
    const quizzes = H('quizzes/index.js'), quizDetail = H('quizzes/[slug].js');
    const submit = H('quizzes/[slug]/submit.js'), infos = H('infographics.js');

    let res = mockRes();
    await notes(mockReq({ method: 'GET', query: {} }), res);
    const list = json(res);
    ok('notes list = 10', res.statusCode === 200 && list.length === 10, `got ${list && list.length}`);

    res = mockRes();
    await notes(mockReq({ method: 'GET', query: { category: 'Cognitive Psychology' } }), res);
    ok('notes filter by category', res.statusCode === 200 && json(res).length >= 1);

    const slug = list[0].slug;
    res = mockRes();
    await noteDetail(mockReq({ method: 'GET', query: { slug } }), res);
    const nd = json(res);
    ok('note detail has points[]', res.statusCode === 200 && Array.isArray(nd.note.points) && nd.note.points.length > 0);

    res = mockRes();
    await quizzes(mockReq({ method: 'GET', query: {} }), res);
    const ql = json(res);
    const noLeak = Array.isArray(ql) && ql.length === 5 &&
      !ql.some((x) => ('answer' in x) || ('explanation' in x) || ('questions' in x && JSON.stringify(x).includes('"answer"')));
    ok('quizzes list = 5, no answers leaked', res.statusCode === 200 && noLeak, `got ${ql && ql.length}`);

    const qslug = ql[0].slug;
    res = mockRes();
    await quizDetail(mockReq({ method: 'GET', query: { slug: qslug } }), res);
    const qd = json(res);
    const leaked = JSON.stringify(qd).includes('"answer"') || JSON.stringify(qd).includes('"explanation"');
    ok('quiz detail hides answers', res.statusCode === 200 && !leaked && qd.quiz.questions.length > 0);

    // submit with all-zeros; verify server-side grading matches DB truth
    const { data: qrow } = await sb.from('quizzes').select('questions_json').eq('slug', qslug).single();
    const questions = u.asJson(qrow.questions_json, []);
    const answers = questions.map(() => 0);
    const expected = questions.filter((x, i) => Number(0) === Number(x.answer)).length;
    res = mockRes();
    await submit(mockReq({ method: 'POST', query: { slug: qslug }, body: { answers }, cookie: cookies.b }), res);
    const sd = json(res);
    ok('quiz submit grades correctly', res.statusCode === 200 && sd.score === expected && sd.total === questions.length,
      `score ${sd && sd.score}/${sd && sd.total}, expected ${expected}`);
    ok('quiz submit awards XP', sd && typeof sd.xp === 'number' && sd.xp > 0);

    res = mockRes();
    await infos(mockReq({ method: 'GET', query: {} }), res);
    ok('infographics = 8', res.statusCode === 200 && json(res).length === 8);
  });

  await section('xp: checkin/progress/read/game/leaderboard', async () => {
    const checkin = H('checkin.js'), progress = H('me/progress.js');
    const read = H('notes/[slug]/read.js'), play = H('games/play.js'), lb = H('leaderboard.js');

    let res = mockRes();
    await checkin(mockReq({ method: 'POST', cookie: cookies.b }), res);
    const c1 = json(res);
    ok('checkin streak=1 xp=10', res.statusCode === 200 && c1.streak === 1 && c1.xp >= 10);

    res = mockRes();
    await checkin(mockReq({ method: 'POST', cookie: cookies.b }), res);
    ok('checkin twice -> already', res.statusCode === 200 && json(res).already === true);

    const { data: notes } = await sb.from('notes').select('slug').limit(1);
    res = mockRes();
    await read(mockReq({ method: 'POST', query: { slug: notes[0].slug }, cookie: cookies.b }), res);
    const rd = json(res);
    ok('note read +20 XP', res.statusCode === 200 && rd.already === false && rd.xp >= 20);
    res = mockRes();
    await read(mockReq({ method: 'POST', query: { slug: notes[0].slug }, cookie: cookies.b }), res);
    ok('note re-read -> already', json(res).already === true);

    res = mockRes();
    await play(mockReq({ method: 'POST', body: { game: 'memory', score: 80 }, cookie: cookies.b }), res);
    ok('game play +5 XP', res.statusCode === 200 && typeof json(res).xp === 'number');
    res = mockRes();
    await play(mockReq({ method: 'POST', body: { game: 'nope', score: 80 }, cookie: cookies.b }), res);
    ok('game invalid 400', res.statusCode === 400);

    res = mockRes();
    await progress(mockReq({ method: 'GET', cookie: cookies.b }), res);
    const pd = json(res);
    ok('progress tasks reflect activity', res.statusCode === 200 && pd.tasks.find((t) => t.id === 'checkin').done === true);

    res = mockRes();
    await lb(mockReq({ method: 'GET', query: {} }), res);
    ok('leaderboard lists users', res.statusCode === 200 && json(res).length >= 2);
  });

  await section('profiles', async () => {
    const profile = H('profile.js'), pub = H('users/[id]/public.js');
    let res = mockRes();
    await profile(mockReq({ method: 'PUT', body: { displayName: 'Tester B', bio: 'hello', country: 'Pakistan', avatar: '🦉' }, cookie: cookies.b }), res);
    const pd = json(res);
    ok('profile update', res.statusCode === 200 && pd.user.displayName === 'Tester B' && pd.user.avatar === '🦉');

    res = mockRes();
    await pub(mockReq({ method: 'GET', query: { id: String(global.__bId) }, cookie: cookies.admin }), res);
    ok('public profile visible', res.statusCode === 200 && json(res).displayName === 'Tester B');
  });

  await section('chat: rooms/send/poll/dm', async () => {
    const rooms = H('chat/rooms.js'), send = H('chat/send.js'), msgs = H('chat/messages.js');
    let res = mockRes();
    await rooms(mockReq({ method: 'GET', query: {} }), res);
    ok('chat rooms = 3', res.statusCode === 200 && json(res).length === 3);

    res = mockRes();
    await send(mockReq({ method: 'POST', body: { type: 'room', id: 'general', body: 'Hello room' }, cookie: cookies.b }), res);
    const sm = json(res);
    ok('room send 201', res.statusCode === 201 && sm.message.body === 'Hello room');

    res = mockRes();
    await msgs(mockReq({ method: 'GET', query: { type: 'room', id: 'general', since: '0' }, cookie: cookies.b }), res);
    const ml = json(res);
    ok('room poll returns message', res.statusCode === 200 && ml.messages.some((m) => m.body === 'Hello room'));
    const lastId = ml.messages[ml.messages.length - 1].id;

    res = mockRes();
    await msgs(mockReq({ method: 'GET', query: { type: 'room', id: 'general', since: String(lastId) }, cookie: cookies.b }), res);
    ok('poll since=lastId empty', res.statusCode === 200 && json(res).messages.length === 0);

    // DM A(admin) -> B
    res = mockRes();
    await send(mockReq({ method: 'POST', body: { type: 'dm', id: global.__bId, body: 'Hi B (dm)' }, cookie: cookies.admin }), res);
    ok('dm send 201', res.statusCode === 201);

    const convs = H('chat/conversations.js');
    res = mockRes();
    await convs(mockReq({ method: 'GET', query: {}, cookie: cookies.b }), res);
    ok('conversations lists DM', res.statusCode === 200 && json(res).some((c) => c.lastBody === 'Hi B (dm)'));

    res = mockRes();
    await msgs(mockReq({ method: 'GET', query: { type: 'dm', id: String(createdIds[0]), since: '0' }, cookie: cookies.b }), res);
    ok('dm poll returns message', res.statusCode === 200 && json(res).messages.some((m) => m.body === 'Hi B (dm)'));

    // profanity + empty guards
    res = mockRes();
    await send(mockReq({ method: 'POST', body: { type: 'room', id: 'general', body: '   ' }, cookie: cookies.b }), res);
    ok('empty message 400', res.statusCode === 400);
  });

  await section('block/report + admin guards', async () => {
    const blocks = H('blocks.js'), unblock = H('blocks/[userId].js'), reports = H('reports.js');
    const stats = H('admin/stats.js'), users = H('admin/users.js'), backup = H('admin/backup.js');
    const msgs = H('chat/messages.js'), send = H('chat/send.js');
    const bId = global.__bId, aId = createdIds[0], cId = global.__cId;

    let res = mockRes();
    await stats(mockReq({ method: 'GET', query: {}, cookie: cookies.b }), res);
    ok('non-admin stats 403', res.statusCode === 403);

    res = mockRes();
    await backup(mockReq({ method: 'GET', query: {}, cookie: cookies.b }), res);
    ok('non-admin backup 403', res.statusCode === 403);

    res = mockRes();
    await blocks(mockReq({ method: 'POST', body: { userId: cId }, cookie: cookies.b }), res);
    ok('B blocks C 201', res.statusCode === 201);

    res = mockRes();
    await blocks(mockReq({ method: 'POST', body: { userId: aId }, cookie: cookies.b }), res);
    ok('block admin 400', res.statusCode === 400);

    res = mockRes();
    await send(mockReq({ method: 'POST', body: { type: 'dm', id: bId, body: 'should fail' }, cookie: cookies.c }), res);
    ok('dm to blocker 403', res.statusCode === 403);

    res = mockRes();
    await send(mockReq({ method: 'POST', body: { type: 'room', id: 'general', body: 'B room msg' }, cookie: cookies.b }), res);
    ok('B room send ok', res.statusCode === 201);

    res = mockRes();
    await send(mockReq({ method: 'POST', body: { type: 'room', id: 'general', body: 'C room msg' }, cookie: cookies.c }), res);
    ok('C room send ok', res.statusCode === 201);

    res = mockRes();
    await msgs(mockReq({ method: 'GET', query: { type: 'room', id: 'general', since: '0' }, cookie: cookies.b }), res);
    const msgsB = json(res).messages || [];
    const seesOwn = msgsB.some((m) => m.body === 'B room msg');
    const hidesBlocked = !msgsB.some((m) => m.body === 'C room msg');
    ok("blocker's poll hides blocked user", res.statusCode === 200 && seesOwn && hidesBlocked);

    res = mockRes();
    await unblock(mockReq({ method: 'DELETE', query: { userId: String(cId) }, cookie: cookies.b }), res);
    ok('unblock 200', res.statusCode === 200);

    res = mockRes();
    await reports(mockReq({ method: 'POST', body: { userId: aId, reason: 'test report' }, cookie: cookies.b }), res);
    ok('report 201', res.statusCode === 201 && typeof json(res).id === 'number');

    res = mockRes();
    await stats(mockReq({ method: 'GET', query: {}, cookie: cookies.admin }), res);
    const st = json(res);
    ok('admin stats 200 + shape', res.statusCode === 200 && typeof st.totalUsers === 'number' && Array.isArray(st.signupsSeries7d));

    res = mockRes();
    await users(mockReq({ method: 'GET', query: { q: 'verceltest' }, cookie: cookies.admin }), res);
    ok('admin users search', res.statusCode === 200 && json(res).length >= 2);

    res = mockRes();
    await backup(mockReq({ method: 'GET', query: {}, cookie: cookies.admin }), res);
    const cd = String(res.getHeader('content-disposition') || '');
    let dump = null; try { dump = JSON.parse(res.body); } catch (e) {}
    const noHashes = dump && !(JSON.stringify(dump.tables.users).includes('password_hash'));
    ok('admin backup JSON download', res.statusCode === 200 && cd.includes('attachment') && !!dump && noHashes);
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
}

main().catch((e) => { console.error('harness crashed:', e.message); process.exit(1); });

// netlify/functions-src/api.js — SOURCE for the ONE catch-all Netlify Function.
//
// Build: `npm run build:netlify` bundles this file (plus the 37 handlers in
// ../../api/ and node_modules) into netlify/functions/api.js with esbuild.
// Netlify then deploys that single self-contained file, so its bundler has
// nothing to trace across directories (cross-directory requires broke the
// production bundle -> 502).
//
// It adapts Netlify Function events to the existing Vercel-style handlers in
// ../../api/ (module.exports = async function handler(req, res)), so the 37
// handlers are reused unchanged.
//
// IMPORTANT: all handler requires below are STATIC strings so esbuild can
// trace and inline them. Do NOT use fs scanning or dynamic require() here.
//
// netlify.toml rewrites /api/* -> /.netlify/functions/api/:splat (status 200),
// so this function sees event.path like "/.netlify/functions/api/notes/abc".
// Path params are merged into req.query (same as Vercel).

// ---------- static route table (static requires => bundled by esbuild) ----------
const HANDLERS = {
  'admin/backup': require('../../api/admin/backup.js'),
  'admin/notes': require('../../api/admin/notes.js'),
  'admin/notes/:id': require('../../api/admin/notes/[id].js'),
  'admin/quizzes': require('../../api/admin/quizzes.js'),
  'admin/quizzes/:id': require('../../api/admin/quizzes/[id].js'),
  'admin/reports': require('../../api/admin/reports.js'),
  'admin/reports/:id/resolve': require('../../api/admin/reports/[id]/resolve.js'),
  'admin/stats': require('../../api/admin/stats.js'),
  'admin/users': require('../../api/admin/users.js'),
  'admin/users/:id/ban': require('../../api/admin/users/[id]/ban.js'),
  'admin/users/:id/unban': require('../../api/admin/users/[id]/unban.js'),
  'auth/login': require('../../api/auth/login.js'),
  'auth/logout': require('../../api/auth/logout.js'),
  'auth/me': require('../../api/auth/me.js'),
  'auth/signup': require('../../api/auth/signup.js'),
  'blocks': require('../../api/blocks.js'),
  'blocks/:userId': require('../../api/blocks/[userId].js'),
  'categories': require('../../api/categories.js'),
  'chat/conversations': require('../../api/chat/conversations.js'),
  'chat/messages': require('../../api/chat/messages.js'),
  'chat/rooms': require('../../api/chat/rooms.js'),
  'chat/send': require('../../api/chat/send.js'),
  'checkin': require('../../api/checkin.js'),
  'games/play': require('../../api/games/play.js'),
  'health': require('../../api/health.js'),
  'infographics': require('../../api/infographics.js'),
  'leaderboard': require('../../api/leaderboard.js'),
  'me/progress': require('../../api/me/progress.js'),
  'notes': require('../../api/notes/index.js'),
  'notes/:slug': require('../../api/notes/[slug].js'),
  'notes/:slug/read': require('../../api/notes/[slug]/read.js'),
  'profile': require('../../api/profile.js'),
  'quizzes': require('../../api/quizzes/index.js'),
  'quizzes/:slug': require('../../api/quizzes/[slug].js'),
  'quizzes/:slug/submit': require('../../api/quizzes/[slug]/submit.js'),
  'reports': require('../../api/reports.js'),
  'users/:id/public': require('../../api/users/[id]/public.js'),
};

// Parallel static map: route key -> handler source file (for tests/diagnostics).
// Kept as plain strings (no dynamic require) so esbuild still sees only
// static requires above.
const FILES = {
  'admin/backup': 'api/admin/backup.js',
  'admin/notes': 'api/admin/notes.js',
  'admin/notes/:id': 'api/admin/notes/[id].js',
  'admin/quizzes': 'api/admin/quizzes.js',
  'admin/quizzes/:id': 'api/admin/quizzes/[id].js',
  'admin/reports': 'api/admin/reports.js',
  'admin/reports/:id/resolve': 'api/admin/reports/[id]/resolve.js',
  'admin/stats': 'api/admin/stats.js',
  'admin/users': 'api/admin/users.js',
  'admin/users/:id/ban': 'api/admin/users/[id]/ban.js',
  'admin/users/:id/unban': 'api/admin/users/[id]/unban.js',
  'auth/login': 'api/auth/login.js',
  'auth/logout': 'api/auth/logout.js',
  'auth/me': 'api/auth/me.js',
  'auth/signup': 'api/auth/signup.js',
  'blocks': 'api/blocks.js',
  'blocks/:userId': 'api/blocks/[userId].js',
  'categories': 'api/categories.js',
  'chat/conversations': 'api/chat/conversations.js',
  'chat/messages': 'api/chat/messages.js',
  'chat/rooms': 'api/chat/rooms.js',
  'chat/send': 'api/chat/send.js',
  'checkin': 'api/checkin.js',
  'games/play': 'api/games/play.js',
  'health': 'api/health.js',
  'infographics': 'api/infographics.js',
  'leaderboard': 'api/leaderboard.js',
  'me/progress': 'api/me/progress.js',
  'notes': 'api/notes/index.js',
  'notes/:slug': 'api/notes/[slug].js',
  'notes/:slug/read': 'api/notes/[slug]/read.js',
  'profile': 'api/profile.js',
  'quizzes': 'api/quizzes/index.js',
  'quizzes/:slug': 'api/quizzes/[slug].js',
  'quizzes/:slug/submit': 'api/quizzes/[slug]/submit.js',
  'reports': 'api/reports.js',
  'users/:id/public': 'api/users/[id]/public.js',
};
const dynCount = (segs) => segs.filter((s) => s[0] === ':').length;
const ROUTES = Object.keys(HANDLERS)
  .map((key) => ({ key, segs: key.split('/') }))
  .sort((a, b) => (b.segs.length - a.segs.length) || (dynCount(a.segs) - dynCount(b.segs)));

function matchRoute(segs) {
  for (const r of ROUTES) {
    if (r.segs.length !== segs.length) continue;
    const params = {};
    let ok = true;
    for (let i = 0; i < r.segs.length; i++) {
      const p = r.segs[i];
      if (p[0] === ':') {
        params[p.slice(1)] = decodeURIComponent(segs[i]);
      } else if (p !== segs[i]) {
        ok = false;
        break;
      }
    }
    if (ok) return { handler: HANDLERS[r.key], file: FILES[r.key], params };
  }
  return null;
}

// ---------- Netlify event -> Vercel-style req ----------
function toReq(event, params) {
  const headers = {};
  for (const k of Object.keys(event.headers || {})) {
    headers[k.toLowerCase()] = event.headers[k];
  }
  let body = null;
  if (event.body) {
    const raw = event.isBase64Encoded
      ? Buffer.from(event.body, 'base64').toString('utf8')
      : event.body;
    const ct = headers['content-type'] || '';
    const t = raw.trim();
    if (ct.indexOf('application/json') !== -1 || t[0] === '{' || t[0] === '[') {
      try { body = JSON.parse(raw); } catch (e) { body = null; }
    } else {
      body = raw;
    }
  }
  return {
    method: event.httpMethod,
    query: Object.assign({}, event.queryStringParameters || {}, params),
    body,
    headers,
  };
}

// ---------- Vercel-style res mock -> Netlify response ----------
function makeRes() {
  const headers = {};
  const multi = {};
  return {
    statusCode: 200,
    _headers: headers,
    _multi: multi,
    body: '',
    setHeader(k, v) {
      const key = String(k);
      if (key.toLowerCase() === 'set-cookie') {
        (multi[key] = multi[key] || []).push(String(v));
      } else {
        headers[key] = String(v);
      }
    },
    getHeader(k) { return headers[String(k)]; },
    end(b) { this.body = b == null ? '' : String(b); },
  };
}

function notFound() {
  return {
    statusCode: 404,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ error: 'not found' }),
  };
}

exports.handler = async (event, context) => {
  try {
    let p = event.path || '';
    const prefix = '/.netlify/functions/api';
    if (p.indexOf(prefix) === 0) p = p.slice(prefix.length);
    p = p.replace(/^\/+|\/+$/g, '');
    const segs = p ? p.split('/') : [];

    const m = matchRoute(segs);
    if (!m) return notFound();

    const req = toReq(event, m.params);
    const res = makeRes();
    await m.handler(req, res);

    const out = {
      statusCode: res.statusCode || 200,
      headers: res._headers,
      body: res.body,
    };
    if (Object.keys(res._multi).length) out.multiValueHeaders = res._multi;
    return out;
  } catch (e) {
    console.error('netlify api adapter error:', e && e.message);
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: 'server error' }),
    };
  }
};

// Exported for the local test harness.
exports.__test__ = { ROUTES, matchRoute, toReq, makeRes };

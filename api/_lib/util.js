// api/_lib/util.js — shared helpers for Mysterious serverless API functions.
// CommonJS on purpose: Vercel Node functions support require() reliably.
// Files under api/_lib/ are excluded from routing (underscore prefix).

const { createClient } = require('@supabase/supabase-js');
const crypto = require('crypto');
const bcrypt = require('bcryptjs');

const SESSION_TTL_DAYS = 30;
const SESSION_COOKIE = 'mysterious_session';

let _client = null;
function supabase() {
  if (!_client) {
    const url = process.env.SUPABASE_URL;
    const key = process.env.SUPABASE_SECRET_KEY;
    if (!url || !key) throw new Error('SUPABASE_URL / SUPABASE_SECRET_KEY env vars are required');
    _client = createClient(url, key, { auth: { persistSession: false } });
  }
  return _client;
}

// ---------- small helpers (ported 1:1 from server.js) ----------

function esc(v) {
  if (typeof v !== 'string') return v;
  return v.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

const PROFANE_WORDS = [
  'fuck', 'shit', 'bitch', 'bastard', 'dick', 'pussy', 'cunt', 'slut', 'whore',
  'faggot', 'nigger', 'retard', 'retarded', 'moron', 'dumbass', 'asshole',
  'chutiya', 'madarchod', 'bhenchod', 'behnchod', 'lulli', 'randi', 'gandu',
  'harami', 'kutta', 'kanjar', 'khoti', 'jahil', 'laanti',
];
const profanityRe = new RegExp(`\\b(${PROFANE_WORDS.join('|')})\\b`, 'gi');
function filterProfanity(text) {
  return String(text).replace(profanityRe, '***');
}

function todayUtc() {
  return new Date().toISOString().slice(0, 10);
}
function yesterdayUtc() {
  const d = new Date();
  d.setUTCDate(d.getUTCDate() - 1);
  return d.toISOString().slice(0, 10);
}
function isoNow() {
  return new Date().toISOString();
}

function parseCookies(header) {
  const out = {};
  if (!header) return out;
  for (const part of String(header).split(';')) {
    const i = part.indexOf('=');
    if (i > 0) out[part.slice(0, i).trim()] = decodeURIComponent(part.slice(i + 1).trim());
  }
  return out;
}

const AVATAR_ALLOWLIST = ['🧠', '🦉', '🎓', '📚', '💡', '🔬', '🧪', '🌟', '🎯', '🚀', '🌈', '🎭'];
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// JSONB columns come back as parsed objects from supabase-js; tolerate strings too.
function asJson(v, fallback) {
  if (v === null || v === undefined) return fallback;
  if (typeof v === 'string') {
    try { return JSON.parse(v); } catch (e) { return fallback; }
  }
  return v;
}

// ---------- response helpers ----------

function send(res, status, obj) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify(obj));
}

function methodNotAllowed(res, allowed) {
  res.statusCode = 405;
  res.setHeader('Allow', allowed.join(', '));
  res.setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify({ error: 'method not allowed' }));
}

// ---------- sessions / auth ----------

function setSessionCookie(res, token) {
  const maxAge = SESSION_TTL_DAYS * 24 * 60 * 60;
  res.setHeader(
    'Set-Cookie',
    `${SESSION_COOKIE}=${encodeURIComponent(token)}; HttpOnly; Path=/; SameSite=Lax; Max-Age=${maxAge}`
  );
}

function clearSessionCookie(res) {
  res.setHeader('Set-Cookie', `${SESSION_COOKIE}=; HttpOnly; Path=/; SameSite=Lax; Max-Age=0`);
}

async function createSession(userId) {
  const token = crypto.randomBytes(32).toString('hex');
  const expiresAt = new Date(Date.now() + SESSION_TTL_DAYS * 24 * 60 * 60 * 1000).toISOString();
  const { error } = await supabase().from('sessions').insert({ token, user_id: userId, expires_at: expiresAt });
  if (error) throw error;
  return token;
}

async function destroySession(req, res) {
  const token = parseCookies(req.headers && req.headers.cookie)[SESSION_COOKIE];
  if (token) {
    await supabase().from('sessions').delete().eq('token', token);
  }
  clearSessionCookie(res);
}

// Returns the user row or null. Also sweeps expired sessions (best effort).
async function getUser(req) {
  const token = parseCookies(req.headers && req.headers.cookie)[SESSION_COOKIE];
  if (!token) return null;
  const sb = supabase();
  await sb.from('sessions').delete().lt('expires_at', new Date().toISOString());
  const { data: sess } = await sb.from('sessions').select('*').eq('token', token).maybeSingle();
  if (!sess) return null;
  const { data: user } = await sb.from('users').select('*').eq('id', sess.user_id).maybeSingle();
  if (!user) {
    await sb.from('sessions').delete().eq('token', token);
    return null;
  }
  return user;
}

// Returns user or sends 401/403 and returns null.
async function requireAuth(req, res) {
  const user = await getUser(req);
  if (!user) { send(res, 401, { error: 'unauthorized' }); return null; }
  if (user.is_banned === 1) { send(res, 403, { error: 'banned' }); return null; }
  return user;
}

// Returns admin user or sends 401/403 and returns null. Re-reads is_admin from DB.
async function requireAdmin(req, res) {
  const user = await getUser(req);
  if (!user) { send(res, 401, { error: 'unauthorized' }); return null; }
  const { data: fresh } = await supabase().from('users').select('*').eq('id', user.id).maybeSingle();
  if (!fresh || fresh.is_admin !== 1) { send(res, 403, { error: 'forbidden' }); return null; }
  if (fresh.is_banned === 1) { send(res, 403, { error: 'banned' }); return null; }
  return fresh;
}

// The ONLY place is_admin may be set: matches ADMIN_EMAIL on signup/login.
async function ensureAdmin(email) {
  const adminEmail = (process.env.ADMIN_EMAIL || '').trim();
  if (!adminEmail) return false;
  if (String(email).toLowerCase() !== adminEmail.toLowerCase()) return false;
  const { data } = await supabase()
    .from('users')
    .update({ is_admin: 1 })
    .ilike('email', adminEmail)
    .select('id');
  return !!(data && data.length);
}

function userShape(u) {
  return {
    id: u.id,
    email: u.email,
    displayName: u.display_name,
    avatar: u.avatar,
    bio: u.bio,
    country: u.country,
    xp: u.xp,
    level: u.level,
    streak: u.streak_count,
    isAdmin: u.is_admin === 1,
  };
}

// addXp(userId, n): xp += n; level = floor(xp/100)+1; returns {xp, level, leveledUp}.
async function addXp(userId, n) {
  const sb = supabase();
  const { data: user } = await sb.from('users').select('id, xp, level').eq('id', userId).maybeSingle();
  if (!user) return null;
  const oldLevel = user.level;
  const xp = user.xp + n;
  const level = Math.floor(xp / 100) + 1;
  await sb.from('users').update({ xp, level }).eq('id', userId);
  return { xp, level, leveledUp: level > oldLevel };
}

function hashPassword(pw) {
  return bcrypt.hashSync(pw, 12);
}
function checkPassword(pw, hash) {
  return bcrypt.compareSync(pw, hash);
}

// ---------- admin content validators (ported 1:1) ----------

function validateNoteBody(b) {
  const slug = String(b.slug || '').trim();
  const title = esc(String(b.title || '').trim());
  const category = esc(String(b.category || 'General').trim());
  const summary = esc(String(b.summary || '').trim());
  const points = Array.isArray(b.points)
    ? b.points.map((p) => ({ point: esc(String(p.point || '')), example: esc(String(p.example || '')) }))
    : null;
  if (!slug || !title) return null;
  return { slug, title, category, summary, points };
}

function validateQuizBody(b) {
  const slug = String(b.slug || '').trim();
  const title = esc(String(b.title || '').trim());
  const noteSlug = b.noteSlug ? String(b.noteSlug).trim() : null;
  const questions = Array.isArray(b.questions)
    ? b.questions.map((x) => ({
        q: esc(String(x.q || '')),
        options: Array.isArray(x.options) ? x.options.slice(0, 4).map((o) => esc(String(o))) : [],
        answer: Number(x.answer),
        explanation: esc(String(x.explanation || '')),
      }))
    : null;
  if (!slug || !title) return null;
  return { slug, title, noteSlug, questions };
}

// ---------- chat helpers ----------

function rowToMsg(r) {
  return { id: r.id, fromId: r.from_id, fromName: r.from_name, avatar: r.avatar, body: r.body, at: r.created_at };
}

async function blockEitherWay(a, b) {
  const { data } = await supabase()
    .from('blocks')
    .select('id')
    .or(`and(blocker_id.eq.${a},blocked_id.eq.${b}),and(blocker_id.eq.${b},blocked_id.eq.${a})`)
    .limit(1);
  return !!(data && data.length);
}

module.exports = {
  supabase,
  esc,
  filterProfanity,
  todayUtc,
  yesterdayUtc,
  isoNow,
  parseCookies,
  AVATAR_ALLOWLIST,
  EMAIL_RE,
  asJson,
  send,
  methodNotAllowed,
  setSessionCookie,
  clearSessionCookie,
  createSession,
  destroySession,
  getUser,
  requireAuth,
  requireAdmin,
  ensureAdmin,
  userShape,
  addXp,
  hashPassword,
  checkPassword,
  validateNoteBody,
  validateQuizBody,
  rowToMsg,
  blockEitherWay,
  SESSION_COOKIE,
};

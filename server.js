// server.js — Mysterious backend: Express REST API + Socket.io chat.
// One service, no build step. Serves public/ statically.

require('dotenv').config();
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const http = require('http');
const express = require('express');
const bcrypt = require('bcryptjs');
const rateLimit = require('express-rate-limit');
const { Server } = require('socket.io');

const ROOT = __dirname;
const PORT = parseInt(process.env.PORT || '3000', 10);
const DATABASE_PATH = path.resolve(ROOT, process.env.DATABASE_PATH || './data/zehen.db');
const SESSION_TTL_DAYS = 30;

// ---------- graceful handling if better-sqlite3 native build is missing ----------
let Database;
try {
  Database = require('better-sqlite3');
} catch (e) {
  console.error('ERROR: better-sqlite3 could not be loaded. Run `npm install` first.');
  process.exit(1);
}

// ---------- helpers ----------

// Escape HTML-significant chars at the input boundary for user-supplied strings.
function esc(v) {
  if (typeof v !== 'string') return v;
  return v.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

// Whole-word profanity filter (~25 common English + Urdu-Roman words) -> "***".
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
  return new Date().toISOString().slice(0, 10); // yyyy-mm-dd UTC
}
function yesterdayUtc() {
  const d = new Date();
  d.setUTCDate(d.getUTCDate() - 1);
  return d.toISOString().slice(0, 10);
}
function isoNow() {
  return new Date().toISOString();
}

// Minimal cookie parser (no extra dependency needed).
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

// ---------- database ----------
fs.mkdirSync(path.dirname(DATABASE_PATH), { recursive: true });
const db = new Database(DATABASE_PATH);
db.pragma('journal_mode = WAL');
db.exec(fs.readFileSync(path.join(ROOT, 'db', 'schema.sql'), 'utf8'));

// Seed the 3 chat rooms (idempotent).
const seedRoom = db.prepare('INSERT OR IGNORE INTO rooms(slug, name, description) VALUES (?, ?, ?)');
db.transaction(() => {
  seedRoom.run('general', 'General Lounge', 'Hang out, chat and connect with fellow psychology learners.');
  seedRoom.run('exam-prep', 'Exam Prep', 'Study together, share tips and prep for psychology exams.');
  seedRoom.run('research-methods', 'Research Methods', 'Discuss research designs, statistics and methodology.');
})();

// Run the content seeder (notes/quizzes from data/*.json, skipped gracefully if missing).
try {
  require('child_process').execFileSync(process.execPath, [path.join(ROOT, 'db', 'seed.js')], {
    env: process.env,
    stdio: 'inherit',
  });
} catch (e) {
  console.warn('Content seed failed (continuing):', e.message);
}

// ---------- prepared statements ----------
const stmt = {
  userById: db.prepare('SELECT * FROM users WHERE id = ?'),
  userByEmail: db.prepare('SELECT * FROM users WHERE email = ?'),
  insertUser: db.prepare(
    'INSERT INTO users(email, password_hash, display_name, avatar, bio, country, is_admin) VALUES (?, ?, ?, ?, ?, ?, 0)'
  ),
  updateProfile: db.prepare('UPDATE users SET display_name = ?, bio = ?, avatar = ?, country = ? WHERE id = ?'),
  insertSession: db.prepare('INSERT INTO sessions(token, user_id, expires_at) VALUES (?, ?, ?)'),
  deleteSession: db.prepare('DELETE FROM sessions WHERE token = ?'),
  sessionByToken: db.prepare('SELECT * FROM sessions WHERE token = ?'),
  expireSessions: db.prepare("DELETE FROM sessions WHERE expires_at < datetime('now')"),
  updateAdmin: db.prepare('UPDATE users SET is_admin = 1 WHERE LOWER(email) = LOWER(?)'),
  blockIdsByViewer: db.prepare('SELECT blocked_id FROM blocks WHERE blocker_id = ?'),
  blockedByOther: db.prepare('SELECT id FROM blocks WHERE blocker_id = ? AND blocked_id = ?'),
  blockedMe: db.prepare('SELECT id FROM blocks WHERE blocker_id = ? AND blocked_id = ?'),
};

// ---------- XP / levels ----------

// addXp(userId, n): xp += n; level = floor(xp/100)+1; returns {xp, level, leveledUp}.
function addXp(userId, n) {
  const user = stmt.userById.get(userId);
  if (!user) return null;
  const oldLevel = user.level;
  const xp = user.xp + n;
  const level = Math.floor(xp / 100) + 1;
  db.prepare('UPDATE users SET xp = ?, level = ? WHERE id = ?').run(xp, level, userId);
  return { xp, level, leveledUp: level > oldLevel };
}

// Public shape of a user for API responses.
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

// ---------- admin promotion (the ONLY place is_admin may be set) ----------

// ensureAdmin(email): if ADMIN_EMAIL matches, flip is_admin=1. No route may do this.
function ensureAdmin(email) {
  const adminEmail = (process.env.ADMIN_EMAIL || '').trim();
  if (!adminEmail) return false;
  if (String(email).toLowerCase() === adminEmail.toLowerCase()) {
    const r = stmt.updateAdmin.run(adminEmail);
    if (r.changes > 0) console.log(`Admin account active for ${adminEmail}`);
    return true;
  }
  return false;
}

function cookieOptions() {
  return {
    httpOnly: true,
    sameSite: 'lax',
    path: '/',
    maxAge: SESSION_TTL_DAYS * 24 * 60 * 60 * 1000,
  };
}
function createSession(res, userId) {
  const token = crypto.randomBytes(32).toString('hex');
  const expiresAt = new Date(Date.now() + SESSION_TTL_DAYS * 24 * 60 * 60 * 1000).toISOString();
  stmt.insertSession.run(token, userId, expiresAt);
  res.cookie('mysterious_session', token, cookieOptions());
  return token;
}
function destroySession(req, res) {
  const token = parseCookies(req.headers.cookie)['mysterious_session'];
  if (token) stmt.deleteSession.run(token);
  res.clearCookie('mysterious_session', { path: '/' });
}

// ---------- auth middleware ----------

function loadUser(req, res, next) {
  req.user = null;
  const token = parseCookies(req.headers.cookie)['mysterious_session'];
  if (token) {
    stmt.expireSessions.run();
    const sess = stmt.sessionByToken.get(token);
    if (sess) {
      const u = stmt.userById.get(sess.user_id);
      if (u) req.user = u;
      else stmt.deleteSession.run(token); // stale session
    }
  }
  next();
}
function requireAuth(req, res, next) {
  if (!req.user) return res.status(401).json({ error: 'unauthorized' });
  if (req.user.is_banned === 1) return res.status(403).json({ error: 'banned' });
  next();
}
function requireAdmin(req, res, next) {
  if (!req.user) return res.status(401).json({ error: 'unauthorized' });
  // Re-read is_admin from DB on every request — never trust a cached copy.
  const fresh = stmt.userById.get(req.user.id);
  if (!fresh || fresh.is_admin !== 1) return res.status(403).json({ error: 'forbidden' });
  if (fresh.is_banned === 1) return res.status(403).json({ error: 'banned' });
  req.user = fresh;
  next();
}

// ---------- app ----------
const app = express();
app.set('trust proxy', 1); // running behind Render
app.use(express.json({ limit: '100kb' }));
app.use(loadUser);

// rate limiters
const authLimiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 30, standardHeaders: true, legacyHeaders: false });
const reportBlockLimiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 30, standardHeaders: true, legacyHeaders: false });

app.get('/api/health', (req, res) => res.json({ ok: true }));

// ================= auth =================

app.post('/api/auth/signup', authLimiter, (req, res) => {
  const email = String(req.body.email || '').trim().toLowerCase();
  const password = String(req.body.password || '');
  const displayName = esc(String(req.body.displayName || '').trim()).slice(0, 40);
  const country = esc(String(req.body.country || '').trim()).slice(0, 60);

  if (!EMAIL_RE.test(email)) return res.status(400).json({ error: 'invalid email' });
  if (password.length < 6) return res.status(400).json({ error: 'password must be at least 6 characters' });
  if (!displayName) return res.status(400).json({ error: 'display name is required' });
  if (stmt.userByEmail.get(email)) return res.status(400).json({ error: 'email already registered' });

  const hash = bcrypt.hashSync(password, 12);
  const info = stmt.insertUser.run(email, hash, displayName, '🧠', '', country);
  ensureAdmin(email);
  const user = stmt.userById.get(info.lastInsertRowid);
  createSession(res, user.id);
  res.status(201).json({ user: userShape(user) });
});

app.post('/api/auth/login', authLimiter, (req, res) => {
  const email = String(req.body.email || '').trim().toLowerCase();
  const password = String(req.body.password || '');
  const user = stmt.userByEmail.get(email);
  if (!user || !bcrypt.compareSync(password, user.password_hash)) {
    return res.status(401).json({ error: 'invalid credentials' });
  }
  if (user.is_banned === 1) return res.status(403).json({ error: 'banned' });
  ensureAdmin(email);
  const fresh = stmt.userById.get(user.id);
  createSession(res, fresh.id);
  res.json({ user: userShape(fresh) });
});

app.post('/api/auth/logout', (req, res) => {
  destroySession(req, res);
  res.json({ ok: true });
});

app.get('/api/auth/me', requireAuth, (req, res) => {
  res.json({ user: userShape(stmt.userById.get(req.user.id)) });
});

// ================= notes / categories / quizzes / infographics =================

app.get('/api/notes', (req, res) => {
  const { category, q } = req.query;
  let sql = 'SELECT id, slug, title, category, summary, read_count AS readCount FROM notes';
  const conds = [];
  const params = [];
  if (category) { conds.push('category = ?'); params.push(String(category)); }
  if (q) { conds.push('(title LIKE ? OR summary LIKE ?)'); params.push(`%${q}%`, `%${q}%`); }
  if (conds.length) sql += ' WHERE ' + conds.join(' AND ');
  sql += ' ORDER BY id ASC';
  res.json(db.prepare(sql).all(...params));
});

app.get('/api/categories', (req, res) => {
  res.json(db.prepare('SELECT DISTINCT category FROM notes ORDER BY category ASC').all().map((r) => r.category));
});

app.get('/api/notes/:slug', (req, res) => {
  const n = db.prepare('SELECT id, slug, title, category, summary, points_json, read_count AS readCount FROM notes WHERE slug = ?').get(req.params.slug);
  if (!n) return res.status(404).json({ error: 'not found' });
  let points = [];
  try { points = JSON.parse(n.points_json); } catch (e) { /* keep empty */ }
  res.json({ note: { id: n.id, slug: n.slug, title: n.title, category: n.category, summary: n.summary, readCount: n.readCount, points } });
});

app.get('/api/quizzes', (req, res) => {
  const rows = db.prepare('SELECT id, slug, title, note_slug AS noteSlug, questions_json, play_count AS playCount FROM quizzes ORDER BY id ASC').all();
  res.json(rows.map((r) => {
    let questionCount = 0;
    try { questionCount = JSON.parse(r.questions_json).length; } catch (e) { /* 0 */ }
    return { id: r.id, slug: r.slug, title: r.title, noteSlug: r.noteSlug, questionCount, playCount: r.playCount };
  }));
});

app.get('/api/quizzes/:slug', (req, res) => {
  const q = db.prepare('SELECT id, slug, title, questions_json FROM quizzes WHERE slug = ?').get(req.params.slug);
  if (!q) return res.status(404).json({ error: 'not found' });
  let questions = [];
  try { questions = JSON.parse(q.questions_json); } catch (e) { /* keep empty */ }
  // NEVER send answer / explanation here.
  const publicQuestions = questions.map((x) => ({ q: x.q, options: x.options }));
  res.json({ quiz: { id: q.id, slug: q.slug, title: q.title, questions: publicQuestions } });
});

app.get('/api/infographics', (req, res) => {
  const p = path.join(ROOT, 'data', 'infographics.json');
  try {
    const arr = JSON.parse(fs.readFileSync(p, 'utf8'));
    if (!Array.isArray(arr)) throw new Error('not an array');
    res.json(arr.map((g) => ({
      title: String(g.title || ''),
      topic: String(g.topic || ''),
      url: '/img/infographics/' + String(g.file || g.filename || ''),
    })));
  } catch (e) {
    console.warn('infographics.json missing or invalid:', e.message);
    res.json([]);
  }
});

// ================= XP routes =================

app.post('/api/checkin', requireAuth, (req, res) => {
  const userId = req.user.id;
  const today = todayUtc();
  const existing = db.prepare('SELECT id FROM checkins WHERE user_id = ? AND date = ?').get(userId, today);
  if (existing) {
    const u = stmt.userById.get(userId);
    return res.json({ already: true, streak: u.streak_count, xp: u.xp, level: u.level });
  }
  const me = stmt.userById.get(userId);
  // Streak math: consecutive only if last check-in was yesterday (UTC).
  const streak = (me.last_checkin === yesterdayUtc()) ? me.streak_count + 1 : 1;
  db.prepare('INSERT INTO checkins(user_id, date) VALUES (?, ?)').run(userId, today);
  db.prepare('UPDATE users SET streak_count = ?, last_checkin = ? WHERE id = ?').run(streak, today, userId);
  const xp = addXp(userId, 10);
  res.json({ already: false, streak, xp: xp.xp, level: xp.level, leveledUp: xp.leveledUp });
});

app.get('/api/me/progress', requireAuth, (req, res) => {
  const userId = req.user.id;
  const today = todayUtc();
  const me = stmt.userById.get(userId);
  const done = {
    checkin: !!db.prepare('SELECT id FROM checkins WHERE user_id = ? AND date = ?').get(userId, today),
    read: !!db.prepare("SELECT 1 FROM note_reads WHERE user_id = ? AND date(at) = ?").get(userId, today),
    quiz: !!db.prepare("SELECT 1 FROM quiz_attempts WHERE user_id = ? AND date(at) = ?").get(userId, today),
    game: !!db.prepare("SELECT 1 FROM game_plays WHERE user_id = ? AND date(at) = ?").get(userId, today),
  };
  res.json({
    streak: me.streak_count,
    xp: me.xp,
    level: me.level,
    lastCheckin: me.last_checkin,
    tasks: [
      { id: 'checkin', label: 'Daily check-in', done: done.checkin },
      { id: 'read', label: 'Read a note today', done: done.read },
      { id: 'quiz', label: 'Finish a quiz today', done: done.quiz },
      { id: 'game', label: 'Play a game today', done: done.game },
    ],
  });
});

app.post('/api/notes/:slug/read', requireAuth, (req, res) => {
  const n = db.prepare('SELECT id FROM notes WHERE slug = ?').get(req.params.slug);
  if (!n) return res.status(404).json({ error: 'not found' });
  const already = !!db.prepare('SELECT 1 FROM note_reads WHERE user_id = ? AND note_id = ?').get(req.user.id, n.id);
  if (already) {
    const u = stmt.userById.get(req.user.id);
    return res.json({ already: true, xp: u.xp, level: u.level, leveledUp: false });
  }
  db.transaction(() => {
    db.prepare('INSERT INTO note_reads(user_id, note_id) VALUES (?, ?)').run(req.user.id, n.id);
    db.prepare('UPDATE notes SET read_count = read_count + 1 WHERE id = ?').run(n.id);
  })();
  const xp = addXp(req.user.id, 20);
  res.json({ already: false, xp: xp.xp, level: xp.level, leveledUp: xp.leveledUp });
});

app.post('/api/quizzes/:slug/submit', requireAuth, (req, res) => {
  const q = db.prepare('SELECT id, questions_json FROM quizzes WHERE slug = ?').get(req.params.slug);
  if (!q) return res.status(404).json({ error: 'not found' });
  let questions = [];
  try { questions = JSON.parse(q.questions_json); } catch (e) { /* empty */ }
  const answers = req.body.answers;
  if (!Array.isArray(answers) || answers.length !== questions.length) {
    return res.status(400).json({ error: 'answers array must match question count' });
  }
  const results = questions.map((quest, i) => {
    const correct = Number(answers[i]) === Number(quest.answer);
    return { correct, correctIndex: Number(quest.answer), explanation: quest.explanation || '' };
  });
  const score = results.filter((r) => r.correct).length;
  db.transaction(() => {
    db.prepare('INSERT INTO quiz_attempts(user_id, quiz_id, score, total) VALUES (?, ?, ?, ?)').run(req.user.id, q.id, score, questions.length);
    db.prepare('UPDATE quizzes SET play_count = play_count + 1 WHERE id = ?').run(q.id);
  })();
  const xp = addXp(req.user.id, Math.max(5, score * 5));
  res.json({ score, total: questions.length, xp: xp.xp, leveledUp: xp.leveledUp, results });
});

app.post('/api/games/play', requireAuth, (req, res) => {
  const game = String(req.body.game || '');
  const score = Number(req.body.score);
  if (!['memory', 'theorist'].includes(game)) return res.status(400).json({ error: 'unknown game' });
  if (!Number.isInteger(score) || score < 0 || score > 100) return res.status(400).json({ error: 'score must be an integer 0..100' });
  db.prepare('INSERT INTO game_plays(user_id, game, score) VALUES (?, ?, ?)').run(req.user.id, game, score);
  const xp = addXp(req.user.id, 5);
  res.json({ xp: xp.xp, level: xp.level, leveledUp: xp.leveledUp });
});

app.get('/api/leaderboard', (req, res) => {
  const rows = db.prepare(
    'SELECT display_name AS displayName, avatar, country, xp, level, streak_count AS streak FROM users WHERE is_banned = 0 ORDER BY xp DESC, id ASC LIMIT 20'
  ).all();
  res.json(rows);
});

// ================= profiles =================

app.get('/api/profile', requireAuth, (req, res) => {
  res.json({ user: userShape(stmt.userById.get(req.user.id)) });
});

app.put('/api/profile', requireAuth, (req, res) => {
  const displayName = esc(String(req.body.displayName ?? req.user.display_name).trim()).slice(0, 40);
  const bio = esc(String(req.body.bio ?? req.user.bio)).slice(0, 200);
  const country = esc(String(req.body.country ?? req.user.country).trim()).slice(0, 60);
  let avatar = req.body.avatar ?? req.user.avatar;
  if (!AVATAR_ALLOWLIST.includes(avatar)) avatar = req.user.avatar;
  if (!displayName) return res.status(400).json({ error: 'display name is required' });
  stmt.updateProfile.run(displayName, bio, avatar, country, req.user.id);
  res.json({ user: userShape(stmt.userById.get(req.user.id)) });
});

app.get('/api/users/:id/public', (req, res) => {
  const id = Number(req.params.id);
  if (!Number.isInteger(id)) return res.status(404).json({ error: 'not found' });
  const target = stmt.userById.get(id);
  if (!target || target.is_banned === 1) return res.status(404).json({ error: 'not found' });
  if (req.user) {
    // 404 if either party blocked the other.
    const blocked = stmt.blockedByOther.get(req.user.id, id) || stmt.blockedMe.get(id, req.user.id);
    if (blocked) return res.status(404).json({ error: 'not found' });
  }
  res.json({
    displayName: target.display_name,
    avatar: target.avatar,
    bio: target.bio,
    country: target.country,
    level: target.level,
    xp: target.xp,
    streak: target.streak_count,
  });
});

// ================= chat REST: rooms, conversations, blocks, reports =================

app.get('/api/chat/rooms', (req, res) => {
  res.json(db.prepare('SELECT slug, name, description FROM rooms ORDER BY slug ASC').all());
});

app.get('/api/chat/conversations', requireAuth, (req, res) => {
  const me = req.user.id;
  const rows = db.prepare(`
    SELECT m.*, u.display_name AS displayName, u.avatar
    FROM messages m
    JOIN users u ON u.id = CASE WHEN m.from_id = ? THEN m.to_id ELSE m.from_id END
    WHERE m.kind = 'dm' AND (m.from_id = ? OR m.to_id = ?)
    ORDER BY m.id DESC
  `).all(me, me, me);
  const seen = new Set();
  const out = [];
  for (const r of rows) {
    const partnerId = r.from_id === me ? r.to_id : r.from_id;
    if (seen.has(partnerId)) continue;
    seen.add(partnerId);
    out.push({ userId: partnerId, displayName: r.displayName, avatar: r.avatar, lastBody: r.body, at: r.created_at });
  }
  res.json(out);
});

app.get('/api/blocks', requireAuth, (req, res) => {
  const rows = db.prepare(`
    SELECT u.id AS userId, u.display_name AS displayName, u.avatar
    FROM blocks b JOIN users u ON u.id = b.blocked_id
    WHERE b.blocker_id = ? ORDER BY b.id DESC
  `).all(req.user.id);
  res.json(rows);
});

app.post('/api/blocks', requireAuth, reportBlockLimiter, (req, res) => {
  const userId = Number(req.body.userId);
  if (!Number.isInteger(userId)) return res.status(400).json({ error: 'invalid userId' });
  if (userId === req.user.id) return res.status(400).json({ error: 'cannot block yourself' });
  const target = stmt.userById.get(userId);
  if (!target || target.is_banned === 1) return res.status(404).json({ error: 'not found' });
  if (target.is_admin === 1) return res.status(400).json({ error: 'cannot block an admin' });
  db.prepare('INSERT OR IGNORE INTO blocks(blocker_id, blocked_id) VALUES (?, ?)').run(req.user.id, userId);
  res.status(201).json({ ok: true });
});

app.delete('/api/blocks/:userId', requireAuth, (req, res) => {
  const userId = Number(req.params.userId);
  db.prepare('DELETE FROM blocks WHERE blocker_id = ? AND blocked_id = ?').run(req.user.id, userId);
  res.json({ ok: true });
});

app.post('/api/reports', requireAuth, reportBlockLimiter, (req, res) => {
  const userId = Number(req.body.userId);
  const reason = esc(String(req.body.reason || '').trim());
  if (!Number.isInteger(userId) || userId === req.user.id) return res.status(400).json({ error: 'invalid userId' });
  if (!reason) return res.status(400).json({ error: 'reason is required' });
  if (reason.length > 300) return res.status(400).json({ error: 'reason too long (max 300)' });
  const target = stmt.userById.get(userId);
  if (!target || target.is_banned === 1) return res.status(404).json({ error: 'not found' });
  const info = db.prepare('INSERT INTO reports(reporter_id, reported_id, reason) VALUES (?, ?, ?)').run(req.user.id, userId, reason);
  res.status(201).json({ id: info.lastInsertRowid });
});

// ================= admin API =================

// Admin-only database backup download (safety copy for free hosting)
app.get('/api/admin/backup', requireAdmin, (req, res) => {
  if (!fs.existsSync(DATABASE_PATH)) return res.status(404).json({ error: 'no database file' });
  const stamp = new Date().toISOString().slice(0, 10);
  res.download(DATABASE_PATH, `mysterious-backup-${stamp}.db`);
});

app.get('/api/admin/stats', requireAdmin, (req, res) => {
  const today = todayUtc();
  const one = (sql, ...p) => db.prepare(sql).get(...p);
  const totalUsers = one('SELECT COUNT(*) AS c FROM users').c;
  const bannedUsers = one('SELECT COUNT(*) AS c FROM users WHERE is_banned = 1').c;
  const newUsers7d = one("SELECT COUNT(*) AS c FROM users WHERE created_at >= datetime('now', '-7 days')").c;
  const newUsers30d = one("SELECT COUNT(*) AS c FROM users WHERE created_at >= datetime('now', '-30 days')").c;
  const dau = one(`
    SELECT COUNT(DISTINCT user_id) AS c FROM (
      SELECT user_id FROM checkins WHERE date = ?
      UNION SELECT user_id FROM (SELECT from_id AS user_id FROM messages WHERE date(created_at) = ?)
      UNION SELECT user_id FROM quiz_attempts WHERE date(at) = ?
      UNION SELECT user_id FROM game_plays WHERE date(at) = ?
    )`, today, today, today, today).c;

  const signupsSeries7d = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date();
    d.setUTCDate(d.getUTCDate() - i);
    const date = d.toISOString().slice(0, 10);
    const count = one("SELECT COUNT(*) AS c FROM users WHERE date(created_at) = ?", date).c;
    signupsSeries7d.push({ date, count });
  }
  const topCountries = db.prepare(
    "SELECT country, COUNT(*) AS count FROM users WHERE country != '' GROUP BY country ORDER BY count DESC LIMIT 8"
  ).all();
  const topNotes = db.prepare('SELECT title, read_count AS readCount FROM notes ORDER BY read_count DESC LIMIT 5').all();
  const topQuizzes = db.prepare('SELECT title, play_count AS playCount FROM quizzes ORDER BY play_count DESC LIMIT 5').all();
  const openReports = one("SELECT COUNT(*) AS c FROM reports WHERE status = 'open'").c;
  const totalMessages = one('SELECT COUNT(*) AS c FROM messages').c;

  res.json({ totalUsers, bannedUsers, newUsers7d, newUsers30d, dau, signupsSeries7d, topCountries, topNotes, topQuizzes, openReports, totalMessages });
});

app.get('/api/admin/users', requireAdmin, (req, res) => {
  const q = String(req.query.q || '').trim();
  let sql = 'SELECT id, email, display_name AS displayName, country, xp, level, streak_count AS streak, is_banned AS isBanned, is_admin AS isAdmin, created_at AS createdAt FROM users';
  const params = [];
  if (q) { sql += ' WHERE email LIKE ? OR display_name LIKE ?'; params.push(`%${q}%`, `%${q}%`); }
  sql += ' ORDER BY id DESC LIMIT 200';
  res.json(db.prepare(sql).all(...params));
});

app.post('/api/admin/users/:id/ban', requireAdmin, (req, res) => {
  const id = Number(req.params.id);
  const target = stmt.userById.get(id);
  if (!target) return res.status(404).json({ error: 'not found' });
  if (id === req.user.id || target.is_admin === 1) return res.status(400).json({ error: 'cannot ban yourself or another admin' });
  db.prepare('UPDATE users SET is_banned = 1 WHERE id = ?').run(id);
  // Drop their sessions so a banned user cannot stay logged in.
  db.prepare('DELETE FROM sessions WHERE user_id = ?').run(id);
  res.json({ ok: true });
});

app.post('/api/admin/users/:id/unban', requireAdmin, (req, res) => {
  const id = Number(req.params.id);
  const target = stmt.userById.get(id);
  if (!target) return res.status(404).json({ error: 'not found' });
  db.prepare('UPDATE users SET is_banned = 0 WHERE id = ?').run(id);
  res.json({ ok: true });
});

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
app.post('/api/admin/notes', requireAdmin, (req, res) => {
  const v = validateNoteBody(req.body);
  if (!v || !Array.isArray(v.points)) return res.status(400).json({ error: 'slug, title and points[] are required' });
  try {
    const info = db.prepare('INSERT INTO notes(slug, title, category, summary, points_json) VALUES (?, ?, ?, ?, ?)')
      .run(v.slug, v.title, v.category, v.summary, JSON.stringify(v.points));
    res.status(201).json({ id: info.lastInsertRowid });
  } catch (e) {
    if (e.code === 'SQLITE_CONSTRAINT_UNIQUE') return res.status(400).json({ error: 'slug already exists' });
    throw e;
  }
});
app.put('/api/admin/notes/:id', requireAdmin, (req, res) => {
  const id = Number(req.params.id);
  if (!db.prepare('SELECT id FROM notes WHERE id = ?').get(id)) return res.status(404).json({ error: 'not found' });
  const v = validateNoteBody(req.body);
  if (!v || !Array.isArray(v.points)) return res.status(400).json({ error: 'slug, title and points[] are required' });
  try {
    db.prepare('UPDATE notes SET slug = ?, title = ?, category = ?, summary = ?, points_json = ? WHERE id = ?')
      .run(v.slug, v.title, v.category, v.summary, JSON.stringify(v.points), id);
    res.json({ ok: true });
  } catch (e) {
    if (e.code === 'SQLITE_CONSTRAINT_UNIQUE') return res.status(400).json({ error: 'slug already exists' });
    throw e;
  }
});
app.delete('/api/admin/notes/:id', requireAdmin, (req, res) => {
  const id = Number(req.params.id);
  db.transaction(() => {
    db.prepare('DELETE FROM note_reads WHERE note_id = ?').run(id);
    db.prepare('DELETE FROM notes WHERE id = ?').run(id);
  })();
  res.json({ ok: true });
});

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
app.post('/api/admin/quizzes', requireAdmin, (req, res) => {
  const v = validateQuizBody(req.body);
  if (!v || !Array.isArray(v.questions) || !v.questions.every((x) => x.options.length === 4 && Number.isInteger(x.answer) && x.answer >= 0 && x.answer < 4)) {
    return res.status(400).json({ error: 'slug, title and questions[{q,options[4],answer,explanation}] are required' });
  }
  try {
    const info = db.prepare('INSERT INTO quizzes(slug, title, note_slug, questions_json) VALUES (?, ?, ?, ?)')
      .run(v.slug, v.title, v.noteSlug, JSON.stringify(v.questions));
    res.status(201).json({ id: info.lastInsertRowid });
  } catch (e) {
    if (e.code === 'SQLITE_CONSTRAINT_UNIQUE') return res.status(400).json({ error: 'slug already exists' });
    throw e;
  }
});
app.put('/api/admin/quizzes/:id', requireAdmin, (req, res) => {
  const id = Number(req.params.id);
  if (!db.prepare('SELECT id FROM quizzes WHERE id = ?').get(id)) return res.status(404).json({ error: 'not found' });
  const v = validateQuizBody(req.body);
  if (!v || !Array.isArray(v.questions) || !v.questions.every((x) => x.options.length === 4 && Number.isInteger(x.answer) && x.answer >= 0 && x.answer < 4)) {
    return res.status(400).json({ error: 'slug, title and questions[{q,options[4],answer,explanation}] are required' });
  }
  try {
    db.prepare('UPDATE quizzes SET slug = ?, title = ?, note_slug = ?, questions_json = ? WHERE id = ?')
      .run(v.slug, v.title, v.noteSlug, JSON.stringify(v.questions), id);
    res.json({ ok: true });
  } catch (e) {
    if (e.code === 'SQLITE_CONSTRAINT_UNIQUE') return res.status(400).json({ error: 'slug already exists' });
    throw e;
  }
});
app.delete('/api/admin/quizzes/:id', requireAdmin, (req, res) => {
  const id = Number(req.params.id);
  db.transaction(() => {
    db.prepare('DELETE FROM quiz_attempts WHERE quiz_id = ?').run(id);
    db.prepare('DELETE FROM quizzes WHERE id = ?').run(id);
  })();
  res.json({ ok: true });
});

app.get('/api/admin/reports', requireAdmin, (req, res) => {
  const rows = db.prepare(`
    SELECT r.id, r.reason, r.status, r.created_at AS createdAt,
           r.reporter_id AS reporterId, ur.display_name AS reporterName,
           r.reported_id AS reportedId, ud.display_name AS reportedName
    FROM reports r
    JOIN users ur ON ur.id = r.reporter_id
    JOIN users ud ON ud.id = r.reported_id
    WHERE r.status = 'open'
    ORDER BY r.id DESC
  `).all();
  res.json(rows);
});
app.post('/api/admin/reports/:id/resolve', requireAdmin, (req, res) => {
  const id = Number(req.params.id);
  db.prepare("UPDATE reports SET status = 'done' WHERE id = ?").run(id);
  res.json({ ok: true });
});

// ---------- static frontend ----------
app.use(express.static(path.join(ROOT, 'public')));

// ---------- Socket.io chat ----------
const server = http.createServer(app);
const io = new Server(server, {
  cors: { origin: false },
});

function socketAuth(socket) {
  const cookies = parseCookies(socket.handshake.headers.cookie);
  const token = cookies['mysterious_session'];
  if (!token) return null;
  const sess = stmt.sessionByToken.get(token);
  if (!sess) return null;
  const user = stmt.userById.get(sess.user_id);
  if (!user || user.is_banned === 1) return null;
  return user;
}

function blockedIdsOf(viewerId) {
  return new Set(stmt.blockIdsByViewer.all(viewerId).map((r) => r.blocked_id));
}
function blockEitherWay(a, b) {
  return !!(stmt.blockedByOther.get(a, b) || stmt.blockedByOther.get(b, a));
}

function rowToMsg(r) {
  return { id: r.id, fromId: r.from_id, fromName: r.from_name, avatar: r.avatar, body: r.body, at: r.created_at };
}

io.use((socket, next) => {
  const user = socketAuth(socket);
  if (!user) return next(new Error('unauthorized'));
  socket.user = user;
  // Simple per-socket rate limit: ~20 messages/minute.
  socket.msgTimestamps = [];
  next();
});

io.on('connection', (socket) => {
  const me = socket.user;

  socket.on('join', (payload = {}) => {
    const { type, id } = payload;
    if (type === 'room') {
      const room = db.prepare('SELECT slug FROM rooms WHERE slug = ?').get(String(id || ''));
      if (!room) return socket.emit('error', { message: 'room not found' });
      const socketRoom = 'room:' + room.slug;
      socket.join(socketRoom);
      const hidden = blockedIdsOf(me.id);
      const rows = db.prepare(`
        SELECT m.id, m.from_id, m.body, m.created_at, u.display_name AS from_name, u.avatar
        FROM messages m JOIN users u ON u.id = m.from_id
        WHERE m.kind = 'room' AND m.room_slug = ? AND u.is_banned = 0
        ORDER BY m.id DESC LIMIT 50
      `).all(room.slug).reverse()
        .filter((r) => !hidden.has(r.from_id)); // blocked users' messages never appear for the blocker
      socket.emit('history', rows.map(rowToMsg));
    } else if (type === 'dm') {
      const otherId = Number(id);
      if (!Number.isInteger(otherId) || otherId === me.id) return socket.emit('error', { message: 'invalid user' });
      const other = stmt.userById.get(otherId);
      if (!other || other.is_banned === 1) return socket.emit('error', { message: 'user not found' });
      if (blockEitherWay(me.id, otherId)) return socket.emit('error', { message: 'blocked' });
      const socketRoom = 'dm:' + Math.min(me.id, otherId) + '_' + Math.max(me.id, otherId);
      socket.join(socketRoom);
      const rows = db.prepare(`
        SELECT m.id, m.from_id, m.body, m.created_at, u.display_name AS from_name, u.avatar
        FROM messages m JOIN users u ON u.id = m.from_id
        WHERE m.kind = 'dm' AND ((m.from_id = ? AND m.to_id = ?) OR (m.from_id = ? AND m.to_id = ?))
        ORDER BY m.id DESC LIMIT 50
      `).all(me.id, otherId, otherId, me.id).reverse();
      socket.emit('history', rows.map(rowToMsg));
    } else {
      socket.emit('error', { message: 'invalid join type' });
    }
  });

  socket.on('message', (payload = {}) => {
    // Rate limit: max ~20 messages per rolling minute per socket.
    const now = Date.now();
    socket.msgTimestamps = socket.msgTimestamps.filter((t) => now - t < 60 * 1000);
    if (socket.msgTimestamps.length >= 20) {
      return socket.emit('error', { message: 'slow down — too many messages' });
    }
    socket.msgTimestamps.push(now);

    const { type, id } = payload;
    const body = filterProfanity(esc(String(payload.body || '').trim()).slice(0, 1000));
    if (!body) return socket.emit('error', { message: 'empty message' });

    // Re-check bans on every message.
    const fresh = stmt.userById.get(me.id);
    if (!fresh || fresh.is_banned === 1) return socket.emit('error', { message: 'banned' });

    if (type === 'room') {
      const room = db.prepare('SELECT slug FROM rooms WHERE slug = ?').get(String(id || ''));
      if (!room) return socket.emit('error', { message: 'room not found' });
      const info = db.prepare("INSERT INTO messages(kind, room_slug, from_id, body) VALUES ('room', ?, ?, ?)").run(room.slug, me.id, body);
      io.to('room:' + room.slug).emit('message', {
        id: info.lastInsertRowid, fromId: me.id, fromName: me.display_name, avatar: me.avatar, body, at: isoNow(),
      });
    } else if (type === 'dm') {
      const otherId = Number(id);
      const other = stmt.userById.get(otherId);
      if (!other || other.is_banned === 1) return socket.emit('error', { message: 'user not found' });
      // Re-check blocks both directions before saving/broadcasting.
      if (blockEitherWay(me.id, otherId)) return socket.emit('error', { message: 'blocked' });
      const info = db.prepare("INSERT INTO messages(kind, to_id, from_id, body) VALUES ('dm', ?, ?, ?)").run(otherId, me.id, body);
      const socketRoom = 'dm:' + Math.min(me.id, otherId) + '_' + Math.max(me.id, otherId);
      io.to(socketRoom).emit('message', {
        id: info.lastInsertRowid, fromId: me.id, fromName: me.display_name, avatar: me.avatar, body, at: isoNow(),
      });
    } else {
      socket.emit('error', { message: 'invalid message type' });
    }
  });
});

// ---------- startup ----------

ensureAdmin(process.env.ADMIN_EMAIL || '');
if (!(process.env.ADMIN_EMAIL || '').trim()) {
  console.log('No ADMIN_EMAIL set — no admin account');
} else {
  const u = db.prepare('SELECT is_admin FROM users WHERE LOWER(email) = LOWER(?)').get(process.env.ADMIN_EMAIL);
  if (u && u.is_admin === 1) console.log(`Admin account active for ${process.env.ADMIN_EMAIL}`);
  else console.log(`ADMIN_EMAIL set (${process.env.ADMIN_EMAIL}) — will activate on signup/login`);
}

server.listen(PORT, () => {
  console.log(`Mysterious backend listening on port ${PORT}`);
});

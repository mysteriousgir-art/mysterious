// POST /api/auth/login
const u = require('../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return u.methodNotAllowed(res, ['POST']);
  try {
    const body = req.body || {};
    const email = String(body.email || '').trim().toLowerCase();
    const password = String(body.password || '');

    const sb = u.supabase();
    const { data: user } = await sb.from('users').select('*').eq('email', email).maybeSingle();
    if (!user || !u.checkPassword(password, user.password_hash)) {
      return u.send(res, 401, { error: 'invalid credentials' });
    }
    if (user.is_banned === 1) return u.send(res, 403, { error: 'banned' });

    await u.ensureAdmin(email);
    const { data: fresh } = await sb.from('users').select('*').eq('id', user.id).single();
    const token = await u.createSession(fresh.id);
    u.setSessionCookie(res, token);
    return u.send(res, 200, { user: u.userShape(fresh) });
  } catch (e) {
    console.error('login error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

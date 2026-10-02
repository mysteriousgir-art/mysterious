// POST /api/auth/signup
const u = require('../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return u.methodNotAllowed(res, ['POST']);
  try {
    const body = req.body || {};
    const email = String(body.email || '').trim().toLowerCase();
    const password = String(body.password || '');
    const displayName = u.esc(String(body.displayName || '').trim()).slice(0, 40);
    const country = u.esc(String(body.country || '').trim()).slice(0, 60);

    if (!u.EMAIL_RE.test(email)) return u.send(res, 400, { error: 'invalid email' });
    if (password.length < 6) return u.send(res, 400, { error: 'password must be at least 6 characters' });
    if (!displayName) return u.send(res, 400, { error: 'display name is required' });

    const sb = u.supabase();
    const { data: existing } = await sb.from('users').select('id').eq('email', email).maybeSingle();
    if (existing) return u.send(res, 400, { error: 'email already registered' });

    const { data: created, error } = await sb.from('users').insert({
      email,
      password_hash: u.hashPassword(password),
      display_name: displayName,
      avatar: '🧠',
      bio: '',
      country,
      is_admin: 0,
    }).select('*').single();
    if (error) throw error;

    await u.ensureAdmin(email);
    const { data: user } = await sb.from('users').select('*').eq('id', created.id).single();
    const token = await u.createSession(user.id);
    u.setSessionCookie(res, token);
    return u.send(res, 201, { user: u.userShape(user) });
  } catch (e) {
    console.error('signup error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

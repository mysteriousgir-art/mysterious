// /api/profile — GET (own profile) / PUT (update profile). Auth required.
const u = require('./_lib/util');

module.exports = async function handler(req, res) {
  try {
    const user = await u.requireAuth(req, res);
    if (!user) return;
    const sb = u.supabase();

    if (req.method === 'GET') {
      const { data: fresh } = await sb.from('users').select('*').eq('id', user.id).single();
      return u.send(res, 200, { user: u.userShape(fresh) });
    }

    if (req.method === 'PUT') {
      const body = req.body || {};
      const displayName = u.esc(String(body.displayName ?? user.display_name).trim()).slice(0, 40);
      const bio = u.esc(String(body.bio ?? user.bio)).slice(0, 200);
      const country = u.esc(String(body.country ?? user.country).trim()).slice(0, 60);
      let avatar = body.avatar ?? user.avatar;
      if (!u.AVATAR_ALLOWLIST.includes(avatar)) avatar = user.avatar;
      if (!displayName) return u.send(res, 400, { error: 'display name is required' });
      const { error } = await sb.from('users')
        .update({ display_name: displayName, bio, avatar, country }).eq('id', user.id);
      if (error) throw error;
      const { data: fresh } = await sb.from('users').select('*').eq('id', user.id).single();
      return u.send(res, 200, { user: u.userShape(fresh) });
    }

    return u.methodNotAllowed(res, ['GET', 'PUT']);
  } catch (e) {
    console.error('profile error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

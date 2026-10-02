// GET /api/users/:id/public  (404 if banned or block either way)
const u = require('../../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const id = Number((req.query || {}).id);
    if (!Number.isInteger(id)) return u.send(res, 404, { error: 'not found' });
    const sb = u.supabase();
    const { data: target } = await sb.from('users').select('*').eq('id', id).maybeSingle();
    if (!target || target.is_banned === 1) return u.send(res, 404, { error: 'not found' });

    const me = await u.getUser(req);
    if (me) {
      if (await u.blockEitherWay(me.id, id)) return u.send(res, 404, { error: 'not found' });
    }
    return u.send(res, 200, {
      displayName: target.display_name,
      avatar: target.avatar,
      bio: target.bio,
      country: target.country,
      level: target.level,
      xp: target.xp,
      streak: target.streak_count,
    });
  } catch (e) {
    console.error('public profile error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

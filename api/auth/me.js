// GET /api/auth/me
const u = require('../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const user = await u.requireAuth(req, res);
    if (!user) return;
    const { data: fresh } = await u.supabase().from('users').select('*').eq('id', user.id).single();
    return u.send(res, 200, { user: u.userShape(fresh) });
  } catch (e) {
    console.error('me error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

// GET /api/admin/contact — public admin contact card so any user can DM the admin
const u = require('./../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const { data: admin } = await u.supabase().from('users')
      .select('id, display_name, avatar').eq('is_admin', 1).limit(1).maybeSingle();
    if (!admin) return u.send(res, 404, { error: 'admin not found' });
    return u.send(res, 200, {
      userId: admin.id,
      displayName: admin.display_name,
      avatar: admin.avatar || '🧠',
    });
  } catch (e) {
    console.error('admin contact error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

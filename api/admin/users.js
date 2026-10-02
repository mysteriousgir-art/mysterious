// GET /api/admin/users?q=  (admin only; user list, max 200)
const u = require('../../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const admin = await u.requireAdmin(req, res);
    if (!admin) return;
    const q = String((req.query || {}).q || '').trim().replace(/[%_,()]/g, '');
    let query = u.supabase().from('users')
      .select('id, email, display_name, country, xp, level, streak_count, is_banned, is_admin, created_at')
      .order('id', { ascending: false }).limit(200);
    if (q) query = query.or(`email.ilike.%${q}%,display_name.ilike.%${q}%`);
    const { data, error } = await query;
    if (error) throw error;
    return u.send(res, 200, (data || []).map((x) => ({
      id: x.id, email: x.email, displayName: x.display_name, country: x.country,
      xp: x.xp, level: x.level, streak: x.streak_count,
      isBanned: x.is_banned === 1, isAdmin: x.is_admin === 1, createdAt: x.created_at,
    })));
  } catch (e) {
    console.error('admin users error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

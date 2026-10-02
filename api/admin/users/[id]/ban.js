// POST /api/admin/users/:id/ban  (admin only; also drops their sessions)
const u = require('../../../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return u.methodNotAllowed(res, ['POST']);
  try {
    const admin = await u.requireAdmin(req, res);
    if (!admin) return;
    const id = Number((req.query || {}).id);
    const sb = u.supabase();
    const { data: target } = await sb.from('users').select('id, is_admin').eq('id', id).maybeSingle();
    if (!target) return u.send(res, 404, { error: 'not found' });
    if (id === admin.id || target.is_admin === 1) {
      return u.send(res, 400, { error: 'cannot ban yourself or another admin' });
    }
    await sb.from('users').update({ is_banned: 1 }).eq('id', id);
    await sb.from('sessions').delete().eq('user_id', id);
    return u.send(res, 200, { ok: true });
  } catch (e) {
    console.error('admin ban error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

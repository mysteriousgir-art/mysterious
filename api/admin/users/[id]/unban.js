// POST /api/admin/users/:id/unban  (admin only)
const u = require('../../../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return u.methodNotAllowed(res, ['POST']);
  try {
    const admin = await u.requireAdmin(req, res);
    if (!admin) return;
    const id = Number((req.query || {}).id);
    const sb = u.supabase();
    const { data: target } = await sb.from('users').select('id').eq('id', id).maybeSingle();
    if (!target) return u.send(res, 404, { error: 'not found' });
    await sb.from('users').update({ is_banned: 0 }).eq('id', id);
    return u.send(res, 200, { ok: true });
  } catch (e) {
    console.error('admin unban error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

// POST /api/admin/reports/:id/resolve  (admin only)
const u = require('../../../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return u.methodNotAllowed(res, ['POST']);
  try {
    const admin = await u.requireAdmin(req, res);
    if (!admin) return;
    const id = Number((req.query || {}).id);
    await u.supabase().from('reports').update({ status: 'done' }).eq('id', id);
    return u.send(res, 200, { ok: true });
  } catch (e) {
    console.error('admin resolve error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

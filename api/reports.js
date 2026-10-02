// POST /api/reports  (auth required; report a user)
const u = require('../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return u.methodNotAllowed(res, ['POST']);
  try {
    const user = await u.requireAuth(req, res);
    if (!user) return;
    const body = req.body || {};
    const targetId = Number(body.userId);
    const reason = u.esc(String(body.reason || '').trim());
    if (!Number.isInteger(targetId) || targetId === user.id) return u.send(res, 400, { error: 'invalid userId' });
    if (!reason) return u.send(res, 400, { error: 'reason is required' });
    if (reason.length > 300) return u.send(res, 400, { error: 'reason too long (max 300)' });

    const sb = u.supabase();
    const { data: target } = await sb.from('users').select('id, is_banned').eq('id', targetId).maybeSingle();
    if (!target || target.is_banned === 1) return u.send(res, 404, { error: 'not found' });

    const { data: ins, error } = await sb.from('reports')
      .insert({ reporter_id: user.id, reported_id: targetId, reason })
      .select('id').single();
    if (error) throw error;
    return u.send(res, 201, { id: ins.id });
  } catch (e) {
    console.error('report error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

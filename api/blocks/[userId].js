// DELETE /api/blocks/:userId  (auth required; unblock)
const u = require('../../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'DELETE') return u.methodNotAllowed(res, ['DELETE']);
  try {
    const user = await u.requireAuth(req, res);
    if (!user) return;
    const targetId = Number((req.query || {}).userId);
    if (!Number.isInteger(targetId)) return u.send(res, 400, { error: 'invalid userId' });
    await u.supabase().from('blocks').delete().eq('blocker_id', user.id).eq('blocked_id', targetId);
    return u.send(res, 200, { ok: true });
  } catch (e) {
    console.error('unblock error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

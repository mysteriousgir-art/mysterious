// DELETE /api/follows/:userId — unfollow a user. Auth required.
const u = require('./../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'DELETE') return u.methodNotAllowed(res, ['DELETE']);
  try {
    const me = await u.requireAuth(req, res);
    if (!me) return;
    const targetId = Number((req.query || {}).userId);
    if (!Number.isInteger(targetId)) return u.send(res, 400, { error: 'invalid userId' });
    const { error } = await u.supabase().from('follows')
      .delete().eq('follower_id', me.id).eq('followed_id', targetId);
    if (error) throw error;
    return u.send(res, 200, { ok: true });
  } catch (e) {
    console.error('unfollow error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

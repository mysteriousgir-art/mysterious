// /api/blocks — GET (list my blocks) / POST (block a user). Auth required.
const u = require('./_lib/util');

module.exports = async function handler(req, res) {
  try {
    const user = await u.requireAuth(req, res);
    if (!user) return;
    const sb = u.supabase();

    if (req.method === 'GET') {
      const { data, error } = await sb.from('blocks').select('blocked_id').eq('blocker_id', user.id).order('id', { ascending: false });
      if (error) throw error;
      const ids = (data || []).map((b) => b.blocked_id);
      let users = [];
      if (ids.length) {
        const { data: us } = await sb.from('users').select('id, display_name, avatar').in('id', ids);
        users = us || [];
      }
      return u.send(res, 200, users.map((x) => ({ userId: x.id, displayName: x.display_name, avatar: x.avatar })));
    }

    if (req.method === 'POST') {
      const targetId = Number((req.body || {}).userId);
      if (!Number.isInteger(targetId)) return u.send(res, 400, { error: 'invalid userId' });
      if (targetId === user.id) return u.send(res, 400, { error: 'cannot block yourself' });
      const { data: target } = await sb.from('users').select('id, is_banned, is_admin').eq('id', targetId).maybeSingle();
      if (!target || target.is_banned === 1) return u.send(res, 404, { error: 'not found' });
      if (target.is_admin === 1) return u.send(res, 400, { error: 'cannot block an admin' });
      const { error } = await sb.from('blocks').upsert(
        { blocker_id: user.id, blocked_id: targetId },
        { onConflict: 'blocker_id,blocked_id', ignoreDuplicates: true }
      );
      if (error) throw error;
      return u.send(res, 201, { ok: true });
    }

    return u.methodNotAllowed(res, ['GET', 'POST']);
  } catch (e) {
    console.error('blocks error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

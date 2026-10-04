// POST /api/reports  (auth required; report a user, or a post via {postId, reason})
const u = require('./_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return u.methodNotAllowed(res, ['POST']);
  try {
    const user = await u.requireAuth(req, res);
    if (!user) return;
    const body = req.body || {};
    const reason = u.esc(String(body.reason || '').trim());
    if (!reason) return u.send(res, 400, { error: 'reason is required' });
    if (reason.length > 300) return u.send(res, 400, { error: 'reason too long (max 300)' });

    const sb = u.supabase();
    let targetId;
    let postId = null;

    if (body.postId !== undefined && body.postId !== null && body.postId !== '') {
      postId = Number(body.postId);
      if (!Number.isInteger(postId)) return u.send(res, 400, { error: 'invalid postId' });
      const { data: post } = await sb.from('posts').select('id, user_id').eq('id', postId).maybeSingle();
      if (!post) return u.send(res, 404, { error: 'post not found' });
      if (post.user_id === user.id) return u.send(res, 400, { error: 'cannot report your own post' });
      targetId = post.user_id;
    } else {
      targetId = Number(body.userId);
      if (!Number.isInteger(targetId) || targetId === user.id) return u.send(res, 400, { error: 'invalid userId' });
    }

    const { data: target } = await sb.from('users').select('id, is_banned').eq('id', targetId).maybeSingle();
    if (!target || target.is_banned === 1) return u.send(res, 404, { error: 'not found' });

    const row = { reporter_id: user.id, reported_id: targetId, reason };
    if (postId !== null) row.post_id = postId; // column added by migrate-social.sql
    const { data: ins, error } = await sb.from('reports')
      .insert(row)
      .select('id').single();
    if (error) throw error;
    return u.send(res, 201, { id: ins.id });
  } catch (e) {
    console.error('report error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

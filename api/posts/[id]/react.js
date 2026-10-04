// /api/posts/:id/react — POST {kind} / DELETE. Auth required.
const u = require('./../../_lib/util');
const s = require('./../../_lib/social');

module.exports = async function handler(req, res) {
  try {
    const me = await u.requireAuth(req, res);
    if (!me) return;
    const sb = u.supabase();
    const id = Number((req.query || {}).id);
    if (!Number.isInteger(id)) return u.send(res, 404, { error: 'not found' });

    const { data: post } = await sb.from('posts').select('*').eq('id', id).maybeSingle();
    if (!post || !(await s.canSeePost(sb, post, me.id))) {
      return u.send(res, 404, { error: 'not found' });
    }

    if (req.method === 'POST') {
      const kind = String((req.body || {}).kind || 'like');
      if (!s.REACTION_KINDS.includes(kind)) return u.send(res, 400, { error: 'invalid kind' });
      const { error } = await sb.from('post_reactions').upsert(
        { post_id: id, user_id: me.id, kind },
        { onConflict: 'post_id,user_id' }
      );
      if (error) throw error;
      const likeCount = await s.recount(sb, 'post_reactions', id, 'like_count');
      return u.send(res, 200, { ok: true, kind, likeCount });
    }

    if (req.method === 'DELETE') {
      const { error } = await sb.from('post_reactions').delete().eq('post_id', id).eq('user_id', me.id);
      if (error) throw error;
      const likeCount = await s.recount(sb, 'post_reactions', id, 'like_count');
      return u.send(res, 200, { ok: true, likeCount });
    }

    return u.methodNotAllowed(res, ['POST', 'DELETE']);
  } catch (e) {
    console.error('react error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

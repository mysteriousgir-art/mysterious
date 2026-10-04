// /api/posts/:id — GET (single post) / DELETE (owner or admin). Auth required.
const u = require('./../_lib/util');
const s = require('./../_lib/social');

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

    if (req.method === 'GET') {
      return u.send(res, 200, await s.serializePost(sb, post, me.id));
    }

    if (req.method === 'DELETE') {
      const isAdmin = me.is_admin === 1;
      if (post.user_id !== me.id && !isAdmin) return u.send(res, 403, { error: 'forbidden' });
      // keep share counts consistent when a repost is removed
      if (post.shared_post_id) {
        const { data: orig } = await sb.from('posts').select('share_count').eq('id', post.shared_post_id).maybeSingle();
        if (orig) await sb.from('posts').update({ share_count: Math.max(0, (orig.share_count || 1) - 1) }).eq('id', post.shared_post_id);
      }
      const { error } = await sb.from('posts').delete().eq('id', id);
      if (error) throw error;
      return u.send(res, 200, { ok: true });
    }

    return u.methodNotAllowed(res, ['GET', 'DELETE']);
  } catch (e) {
    console.error('post detail error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

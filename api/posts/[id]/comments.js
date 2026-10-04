// /api/posts/:id/comments — GET (list) / POST (add). Auth required.
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

    if (req.method === 'GET') {
      const { data: rows } = await sb.from('post_comments').select('*')
        .eq('post_id', id).order('id', { ascending: true }).limit(100);
      const ids = [...new Set((rows || []).map((c) => c.user_id))];
      const authors = new Map();
      if (ids.length) {
        const { data: us } = await sb.from('users').select('id, display_name, avatar').in('id', ids);
        (us || []).forEach((x) => authors.set(x.id, s.authorShape(x)));
      }
      return u.send(res, 200, (rows || []).map((c) => ({
        id: c.id, body: c.body, createdAt: c.created_at,
        author: authors.get(c.user_id) || null,
        mine: c.user_id === me.id,
      })));
    }

    if (req.method === 'POST') {
      const text = u.filterProfanity(u.esc(String((req.body || {}).body || '').trim()));
      if (!text) return u.send(res, 400, { error: 'comment is empty' });
      if (text.length > 300) return u.send(res, 400, { error: 'comment too long (max 300)' });
      const { data: ins, error } = await sb.from('post_comments')
        .insert({ post_id: id, user_id: me.id, body: text })
        .select('*').single();
      if (error) throw error;
      await s.recount(sb, 'post_comments', id, 'comment_count');
      return u.send(res, 201, {
        id: ins.id, body: ins.body, createdAt: ins.created_at, mine: true,
        author: { userId: me.id, displayName: me.display_name, avatar: me.avatar },
      });
    }

    return u.methodNotAllowed(res, ['GET', 'POST']);
  } catch (e) {
    console.error('comments error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

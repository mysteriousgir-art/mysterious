// POST /api/posts/:id/share — repost with optional note. Auth required.
const u = require('./../../_lib/util');
const s = require('./../../_lib/social');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return u.methodNotAllowed(res, ['POST']);
  try {
    const me = await u.requireAuth(req, res);
    if (!me) return;
    const sb = u.supabase();
    const id = Number((req.query || {}).id);
    if (!Number.isInteger(id)) return u.send(res, 404, { error: 'not found' });

    const { data: orig } = await sb.from('posts').select('*').eq('id', id).maybeSingle();
    if (!orig || !(await s.canSeePost(sb, orig, me.id))) {
      return u.send(res, 404, { error: 'not found' });
    }

    const text = u.filterProfanity(u.esc(String((req.body || {}).body || '').trim()));
    if (text.length > 500) return u.send(res, 400, { error: 'note too long (max 500)' });

    const { data: ins, error } = await sb.from('posts').insert({
      user_id: me.id, body: text, image_url: '',
      visibility: orig.visibility === 'followers' ? 'followers' : 'public',
      shared_post_id: orig.id,
    }).select('*').single();
    if (error) throw error;
    await sb.from('posts').update({ share_count: (orig.share_count || 0) + 1 }).eq('id', orig.id);
    await u.addXp(me.id, 2);
    return u.send(res, 201, await s.serializePost(sb, ins, me.id));
  } catch (e) {
    console.error('share error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

// /api/follows — GET (followers/following lists + counts) / POST (follow a user). Auth required.
const u = require('./_lib/util');
const s = require('./_lib/social');

async function userList(sb, ids) {
  if (!ids.length) return [];
  const { data } = await sb.from('users').select('id, display_name, avatar').in('id', ids);
  return (data || []).map(s.authorShape);
}

module.exports = async function handler(req, res) {
  try {
    const me = await u.requireAuth(req, res);
    if (!me) return;
    const sb = u.supabase();

    if (req.method === 'GET') {
      const q = req.query || {};
      const targetId = q.userId ? Number(q.userId) : me.id;
      if (!Number.isInteger(targetId)) return u.send(res, 400, { error: 'invalid userId' });
      const type = q.type === 'followers' ? 'followers' : 'following';
      if (targetId !== me.id) {
        const { data: t } = await sb.from('users').select('id, is_banned').eq('id', targetId).maybeSingle();
        if (!t || t.is_banned === 1) return u.send(res, 404, { error: 'not found' });
        if (await u.blockEitherWay(me.id, targetId)) return u.send(res, 404, { error: 'not found' });
      }
      const col = type === 'followers' ? 'follower_id' : 'followed_id';
      const other = type === 'followers' ? 'follower_id' : 'followed_id';
      const { data: rows } = await sb.from('follows').select(other).eq(col, targetId).order('created_at', { ascending: false }).limit(100);
      const ids = (rows || []).map((r) => r[other]);
      const [{ count: followerCount }, { count: followingCount }] = await Promise.all([
        sb.from('follows').select('follower_id', { count: 'exact', head: true }).eq('followed_id', targetId),
        sb.from('follows').select('followed_id', { count: 'exact', head: true }).eq('follower_id', targetId),
      ]);
      const users = await userList(sb, ids);
      const out = {
        userId: targetId, type, users,
        followerCount: followerCount || 0,
        followingCount: followingCount || 0,
      };
      if (targetId !== me.id) out.isFollowing = await s.isFollowing(sb, me.id, targetId);
      return u.send(res, 200, out);
    }

    if (req.method === 'POST') {
      const targetId = Number((req.body || {}).userId);
      if (!Number.isInteger(targetId)) return u.send(res, 400, { error: 'invalid userId' });
      if (targetId === me.id) return u.send(res, 400, { error: 'cannot follow yourself' });
      const { data: target } = await sb.from('users').select('id, is_banned').eq('id', targetId).maybeSingle();
      if (!target || target.is_banned === 1) return u.send(res, 404, { error: 'not found' });
      if (await u.blockEitherWay(me.id, targetId)) return u.send(res, 404, { error: 'not found' });
      const { error } = await sb.from('follows').upsert(
        { follower_id: me.id, followed_id: targetId },
        { onConflict: 'follower_id,followed_id', ignoreDuplicates: true }
      );
      if (error) throw error;
      return u.send(res, 201, { ok: true });
    }

    return u.methodNotAllowed(res, ['GET', 'POST']);
  } catch (e) {
    console.error('follows error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

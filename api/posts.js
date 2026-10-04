// /api/posts — GET (feed) / POST (create a post). Auth required for both.
const u = require('./_lib/util');
const s = require('./_lib/social');

const MAX_BODY = 500;
const MAX_IMAGE_BYTES = 1500 * 1024; // 1.5 MB
const IMAGE_TYPES = { 'image/jpeg': 'jpg', 'image/png': 'png', 'image/webp': 'webp', 'image/gif': 'gif' };
const BUCKET = 'post-images';

function parseImageData(raw) {
  if (!raw || typeof raw !== 'string') return null;
  const m = raw.match(/^data:(image\/[a-z+]+);base64,([A-Za-z0-9+/=]+)$/);
  if (m) return { mime: m[1], b64: m[2] };
  if (/^[A-Za-z0-9+/=]+$/.test(raw)) return { mime: null, b64: raw };
  return null;
}

async function uploadImage(sb, userId, parsed, hintType) {
  const mime = parsed.mime || hintType;
  const ext = IMAGE_TYPES[mime];
  if (!ext) return { error: 'unsupported image type (jpeg, png, webp or gif only)' };
  const buf = Buffer.from(parsed.b64, 'base64');
  if (buf.length > MAX_IMAGE_BYTES) return { error: 'image too large (max 1.5 MB)' };
  if (buf.length < 100) return { error: 'invalid image data' };
  const path = userId + '/' + Date.now() + '-' + Math.random().toString(36).slice(2, 8) + '.' + ext;
  const { error } = await sb.storage.from(BUCKET).upload(path, buf, { contentType: mime, upsert: false });
  if (error) return { error: 'image upload failed' };
  const { data } = sb.storage.from(BUCKET).getPublicUrl(path);
  return { url: data.publicUrl };
}

module.exports = async function handler(req, res) {
  try {
    const me = await u.requireAuth(req, res);
    if (!me) return;
    const sb = u.supabase();

    // ---------------- GET: feed ----------------
    if (req.method === 'GET') {
      const q = req.query || {};
      const feed = ['all', 'following', 'mine'].includes(q.feed) ? q.feed : 'all';
      const limit = Math.min(Math.max(Number(q.limit) || 20, 1), 50);
      const before = Number(q.before) || 0;
      const onlyUserId = q.userId ? Number(q.userId) : 0;

      let query = sb.from('posts').select('*').order('id', { ascending: false }).limit(limit);
      if (before > 0) query = query.lt('id', before);

      if (onlyUserId) {
        if (!Number.isInteger(onlyUserId)) return u.send(res, 400, { error: 'invalid userId' });
        if (onlyUserId !== me.id && await u.blockEitherWay(me.id, onlyUserId)) {
          return u.send(res, 200, { posts: [], nextBefore: 0 });
        }
        query = query.eq('user_id', onlyUserId);
      } else if (feed === 'mine') {
        query = query.eq('user_id', me.id);
      } else if (feed === 'following') {
        const { data: frows } = await sb.from('follows').select('followed_id').eq('follower_id', me.id).limit(2000);
        const ids = [me.id].concat((frows || []).map((r) => r.followed_id));
        query = query.in('user_id', ids);
      }

      const { data: rows, error } = await query;
      if (error) throw error;

      const out = [];
      for (const p of rows || []) {
        if (await s.canSeePost(sb, p, me.id)) out.push(await s.serializePost(sb, p, me.id));
      }
      const lastId = (rows || []).length ? rows[rows.length - 1].id : 0;
      return u.send(res, 200, { posts: out, nextBefore: (rows || []).length === limit ? lastId : 0 });
    }

    // ---------------- POST: create ----------------
    if (req.method === 'POST') {
      const body = req.body || {};
      let text = u.filterProfanity(u.esc(String(body.body || '').trim()));
      const visibility = s.VISIBILITIES.includes(body.visibility) ? body.visibility : 'public';
      const sharedPostId = body.sharedPostId ? Number(body.sharedPostId) : 0;

      let sharedOf = null;
      if (sharedPostId) {
        if (!Number.isInteger(sharedPostId)) return u.send(res, 400, { error: 'invalid sharedPostId' });
        const { data: sp } = await sb.from('posts').select('*').eq('id', sharedPostId).maybeSingle();
        if (!sp || !(await s.canSeePost(sb, sp, me.id))) return u.send(res, 404, { error: 'shared post not found' });
        sharedOf = sp;
      }

      if (!text && !body.imageData && !sharedPostId) {
        return u.send(res, 400, { error: 'post needs text, an image, or a shared post' });
      }
      if (text.length > MAX_BODY) return u.send(res, 400, { error: 'post too long (max 500)' });

      let imageUrl = '';
      if (body.imageData) {
        const parsed = parseImageData(body.imageData);
        if (!parsed) return u.send(res, 400, { error: 'invalid image data' });
        const up = await uploadImage(sb, me.id, parsed, body.imageType);
        if (up.error) return u.send(res, 400, { error: up.error });
        imageUrl = up.url;
      }

      const { data: ins, error } = await sb.from('posts').insert({
        user_id: me.id, body: text, image_url: imageUrl,
        visibility, shared_post_id: sharedOf ? sharedOf.id : null,
      }).select('*').single();
      if (error) throw error;

      if (sharedOf) {
        await sb.from('posts').update({ share_count: (sharedOf.share_count || 0) + 1 }).eq('id', sharedOf.id);
      }
      await u.addXp(me.id, 2);
      return u.send(res, 201, await s.serializePost(sb, ins, me.id));
    }

    return u.methodNotAllowed(res, ['GET', 'POST']);
  } catch (e) {
    console.error('posts error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

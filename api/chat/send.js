// POST /api/chat/send  {type:'room'|'dm', id, body}  (auth required)
// Polling replacement for socket.io "message". Same validation as before.
const u = require('./../_lib/util');

// Best-effort per-instance rate limit: ~20 messages per rolling minute per user
// (serverless instances don't share memory, so this is approximate).
const msgTimestamps = new Map(); // userId -> [epochMs]
function rateLimited(userId) {
  const now = Date.now();
  const arr = (msgTimestamps.get(userId) || []).filter((t) => now - t < 60 * 1000);
  if (arr.length >= 20) return true;
  arr.push(now);
  msgTimestamps.set(userId, arr);
  return false;
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return u.methodNotAllowed(res, ['POST']);
  try {
    const me = await u.requireAuth(req, res);
    if (!me) return;
    if (rateLimited(me.id)) return u.send(res, 429, { error: 'slow down — too many messages' });
    const body0 = req.body || {};
    const type = String(body0.type || '');
    const id = body0.id;
    const body = u.filterProfanity(u.esc(String(body0.body || '').trim()).slice(0, 1000));
    if (!body) return u.send(res, 400, { error: 'empty message' });

    const sb = u.supabase();
    // Re-check bans on every message.
    const { data: fresh } = await sb.from('users').select('id, is_banned, display_name, avatar').eq('id', me.id).maybeSingle();
    if (!fresh || fresh.is_banned === 1) return u.send(res, 403, { error: 'banned' });

    if (type === 'room') {
      const slug = String(id || '');
      const { data: room } = await sb.from('rooms').select('slug, requires_approval').eq('slug', slug).maybeSingle();
      if (!room) return u.send(res, 404, { error: 'room not found' });
      if (room.requires_approval === 1 && fresh.is_admin !== 1) {
        const { data: mem } = await sb.from('room_members').select('approved').eq('room_slug', slug).eq('user_id', me.id).maybeSingle();
        if (!mem || mem.approved !== 1) {
          // Trial: unapproved members get 5 messages, then wait for admin approval
          const { count } = await sb.from('messages').select('id', { count: 'exact', head: true })
            .eq('kind', 'room').eq('room_slug', slug).eq('from_id', me.id);
          if ((count || 0) >= 5) {
            return u.send(res, 403, { error: 'trial over — waiting for admin approval to send more messages' });
          }
        }
      }
      const { data: ins, error } = await sb.from('messages')
        .insert({ kind: 'room', room_slug: slug, from_id: me.id, body })
        .select('id, created_at').single();
      if (error) throw error;
      return u.send(res, 201, { message: {
        id: ins.id, fromId: me.id, fromName: fresh.display_name, avatar: fresh.avatar, body, at: ins.created_at,
      }});
    }

    if (type === 'dm') {
      const otherId = Number(id);
      const { data: other } = await sb.from('users').select('id, is_banned').eq('id', otherId).maybeSingle();
      if (!other || other.is_banned === 1) return u.send(res, 404, { error: 'user not found' });
      if (await u.blockEitherWay(me.id, otherId)) return u.send(res, 403, { error: 'blocked' });
      const { data: ins, error } = await sb.from('messages')
        .insert({ kind: 'dm', to_id: otherId, from_id: me.id, body })
        .select('id, created_at').single();
      if (error) throw error;
      return u.send(res, 201, { message: {
        id: ins.id, fromId: me.id, fromName: fresh.display_name, avatar: fresh.avatar, body, at: ins.created_at,
      }});
    }

    return u.send(res, 400, { error: 'invalid message type' });
  } catch (e) {
    console.error('chat send error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

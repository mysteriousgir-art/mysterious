// GET /api/chat/messages?type=room&id=<slug>&since=<lastId>
//    /api/chat/messages?type=dm&id=<userId>&since=<lastId>
// Polling replacement for socket.io history. Auth required.
const u = require('../_lib/util');

const LIMIT = 50;

async function withNames(sb, rows) {
  if (!rows.length) return [];
  const ids = [...new Set(rows.map((r) => r.from_id))];
  const { data: users } = await sb.from('users').select('id, display_name, avatar').in('id', ids);
  const map = new Map((users || []).map((x) => [x.id, x]));
  return rows.map((r) => ({
    id: r.id,
    from_id: r.from_id,
    from_name: (map.get(r.from_id) || {}).display_name || 'Someone',
    avatar: (map.get(r.from_id) || {}).avatar || '🧠',
    body: r.body,
    created_at: r.created_at,
  }));
}

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const me = await u.requireAuth(req, res);
    if (!me) return;
    const q = req.query || {};
    const type = String(q.type || '');
    const id = q.id;
    const since = Number(q.since || 0);
    const sb = u.supabase();

    if (type === 'room') {
      const slug = String(id || '');
      const { data: room } = await sb.from('rooms').select('slug').eq('slug', slug).maybeSingle();
      if (!room) return u.send(res, 404, { error: 'room not found' });

      let query = sb.from('messages').select('id, from_id, body, created_at')
        .eq('kind', 'room').eq('room_slug', slug);
      if (since > 0) query = query.gt('id', since).order('id', { ascending: true });
      else query = query.order('id', { ascending: false }).limit(LIMIT);
      const { data: rows, error } = await query;
      if (error) throw error;

      // blocked users' messages never appear for the blocker
      const { data: blocks } = await sb.from('blocks').select('blocked_id').eq('blocker_id', me.id);
      const hidden = new Set((blocks || []).map((b) => b.blocked_id));
      let msgs = await withNames(sb, rows || []);
      msgs = msgs.filter((m) => !hidden.has(m.from_id));
      if (!(since > 0)) msgs = msgs.reverse();
      return u.send(res, 200, { messages: msgs.map(u.rowToMsg) });
    }

    if (type === 'dm') {
      const otherId = Number(id);
      if (!Number.isInteger(otherId) || otherId === me.id) return u.send(res, 400, { error: 'invalid user' });
      const { data: other } = await sb.from('users').select('id, is_banned').eq('id', otherId).maybeSingle();
      if (!other || other.is_banned === 1) return u.send(res, 404, { error: 'user not found' });
      if (await u.blockEitherWay(me.id, otherId)) return u.send(res, 403, { error: 'blocked' });

      let query = sb.from('messages').select('id, from_id, body, created_at').eq('kind', 'dm')
        .or(`and(from_id.eq.${me.id},to_id.eq.${otherId}),and(from_id.eq.${otherId},to_id.eq.${me.id})`);
      if (since > 0) query = query.gt('id', since).order('id', { ascending: true });
      else query = query.order('id', { ascending: false }).limit(LIMIT);
      const { data: rows, error } = await query;
      if (error) throw error;
      let msgs = await withNames(sb, rows || []);
      if (!(since > 0)) msgs = msgs.reverse();
      return u.send(res, 200, { messages: msgs.map(u.rowToMsg) });
    }

    return u.send(res, 400, { error: 'invalid type' });
  } catch (e) {
    console.error('chat messages error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

// /api/chat/rooms/join  (auth required)
// POST {slug} — request permission to send messages in a room.
//   If the room doesn't require approval, membership is auto-approved.
// GET ?slug= — my membership status: {approved: 1|0|null}
const u = require('./../../_lib/util');

module.exports = async function handler(req, res) {
  const sb = u.supabase();
  try {
    const me = await u.requireAuth(req, res);
    if (!me) return;

    if (req.method === 'GET') {
      const slug = String((req.query || {}).slug || '').trim();
      if (!slug) return u.send(res, 400, { error: 'slug is required' });
      const { data: room } = await sb.from('rooms').select('slug, requires_approval').eq('slug', slug).maybeSingle();
      if (!room) return u.send(res, 404, { error: 'room not found' });
      const { data: m } = await sb.from('room_members').select('approved').eq('room_slug', slug).eq('user_id', me.id).maybeSingle();
      const approved = m ? m.approved : null;
      // trial messages used (for unapproved members in approval rooms)
      let trial_used = 0;
      const TRIAL_LIMIT = 5;
      if (room.requires_approval === 1 && approved !== 1) {
        const { count } = await sb.from('messages').select('id', { count: 'exact', head: true })
          .eq('kind', 'room').eq('room_slug', slug).eq('from_id', me.id);
        trial_used = count || 0;
      }
      return u.send(res, 200, {
        requires_approval: room.requires_approval === 1 ? 1 : 0,
        approved,
        trial_used,
        trial_limit: TRIAL_LIMIT,
      });
    }

    if (req.method === 'POST') {
      const slug = String((req.body || {}).slug || '').trim();
      if (!slug) return u.send(res, 400, { error: 'slug is required' });
      const { data: room } = await sb.from('rooms').select('slug, requires_approval').eq('slug', slug).maybeSingle();
      if (!room) return u.send(res, 404, { error: 'room not found' });
      const approved = room.requires_approval === 1 ? 0 : 1;
      const { data, error } = await sb.from('room_members')
        .upsert({ room_slug: slug, user_id: me.id, approved }, { onConflict: 'room_slug,user_id' })
        .select('approved').single();
      if (error) throw error;
      return u.send(res, 200, { approved: data.approved });
    }

    return u.methodNotAllowed(res, ['GET', 'POST']);
  } catch (e) {
    console.error('room join error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

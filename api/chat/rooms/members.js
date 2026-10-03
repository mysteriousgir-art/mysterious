// /api/chat/rooms/members  (admin only)
// GET ?slug= — list members + pending requests for a room
// POST {slug, user_id, approved} — approve (1) or reject (0 = remove)
const u = require('./../../_lib/util');

module.exports = async function handler(req, res) {
  const sb = u.supabase();
  try {
    const admin = await u.requireAdmin(req, res);
    if (!admin) return;

    if (req.method === 'GET') {
      const slug = String((req.query || {}).slug || '').trim();
      if (!slug) return u.send(res, 400, { error: 'slug is required' });
      const { data: members, error } = await sb.from('room_members')
        .select('user_id, approved, requested_at')
        .eq('room_slug', slug).order('requested_at', { ascending: true });
      if (error) throw error;
      // attach user names
      const ids = (members || []).map(m => m.user_id);
      let usersById = {};
      if (ids.length) {
        const { data: users } = await sb.from('users').select('id, display_name, avatar').in('id', ids);
        (users || []).forEach(x => { usersById[x.id] = x; });
      }
      return u.send(res, 200, (members || []).map(m => ({
        user_id: m.user_id,
        displayName: (usersById[m.user_id] || {}).display_name || ('User ' + m.user_id),
        avatar: (usersById[m.user_id] || {}).avatar || '🧠',
        approved: m.approved,
        requested_at: m.requested_at,
      })));
    }

    if (req.method === 'POST') {
      const b = req.body || {};
      const slug = String(b.slug || '').trim();
      const user_id = Number(b.user_id);
      const approved = Number(b.approved) === 1 ? 1 : 0;
      if (!slug || !user_id) return u.send(res, 400, { error: 'slug and user_id are required' });
      if (approved === 1) {
        const { error } = await sb.from('room_members').update({ approved: 1 }).eq('room_slug', slug).eq('user_id', user_id);
        if (error) throw error;
      } else {
        const { error } = await sb.from('room_members').delete().eq('room_slug', slug).eq('user_id', user_id);
        if (error) throw error;
      }
      return u.send(res, 200, { ok: true });
    }

    return u.methodNotAllowed(res, ['GET', 'POST']);
  } catch (e) {
    console.error('room members error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

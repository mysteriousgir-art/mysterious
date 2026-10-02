// GET /api/chat/conversations  (auth required; latest DM per partner)
const u = require('./../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const me = await u.requireAuth(req, res);
    if (!me) return;
    const sb = u.supabase();
    const { data: rows, error } = await sb.from('messages')
      .select('id, from_id, to_id, body, created_at')
      .eq('kind', 'dm')
      .or(`from_id.eq.${me.id},to_id.eq.${me.id}`)
      .order('id', { ascending: false });
    if (error) throw error;

    const seen = new Set();
    const out = [];
    for (const r of (rows || [])) {
      const partnerId = r.from_id === me.id ? r.to_id : r.from_id;
      if (seen.has(partnerId)) continue;
      seen.add(partnerId);
      const { data: partner } = await sb.from('users').select('display_name, avatar').eq('id', partnerId).maybeSingle();
      out.push({
        userId: partnerId,
        displayName: partner ? partner.display_name : 'Someone',
        avatar: partner ? partner.avatar : '🧠',
        lastBody: r.body,
        at: r.created_at,
      });
    }
    return u.send(res, 200, out);
  } catch (e) {
    console.error('conversations error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

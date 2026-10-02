// POST /api/notes/:slug/read  (auth required, +20 XP first read)
const u = require('./../../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return u.methodNotAllowed(res, ['POST']);
  try {
    const user = await u.requireAuth(req, res);
    if (!user) return;
    const slug = String((req.query || {}).slug || '');
    const sb = u.supabase();
    const { data: n } = await sb.from('notes').select('id, read_count').eq('slug', slug).maybeSingle();
    if (!n) return u.send(res, 404, { error: 'not found' });

    const { data: already } = await sb.from('note_reads')
      .select('user_id').eq('user_id', user.id).eq('note_id', n.id).maybeSingle();
    if (already) {
      const { data: me } = await sb.from('users').select('xp, level').eq('id', user.id).single();
      return u.send(res, 200, { already: true, xp: me.xp, level: me.level, leveledUp: false });
    }

    const { error: insErr } = await sb.from('note_reads').insert({ user_id: user.id, note_id: n.id });
    if (insErr) throw insErr;
    await sb.from('notes').update({ read_count: (n.read_count || 0) + 1 }).eq('id', n.id);
    const xp = await u.addXp(user.id, 20);
    return u.send(res, 200, { already: false, xp: xp.xp, level: xp.level, leveledUp: xp.leveledUp });
  } catch (e) {
    console.error('note read error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

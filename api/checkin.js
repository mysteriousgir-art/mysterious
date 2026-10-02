// POST /api/checkin  (auth required; daily streak + 10 XP)
const u = require('../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return u.methodNotAllowed(res, ['POST']);
  try {
    const user = await u.requireAuth(req, res);
    if (!user) return;
    const sb = u.supabase();
    const today = u.todayUtc();

    const { data: existing } = await sb.from('checkins')
      .select('id').eq('user_id', user.id).eq('date', today).maybeSingle();
    if (existing) {
      const { data: me } = await sb.from('users').select('streak_count, xp, level').eq('id', user.id).single();
      return u.send(res, 200, { already: true, streak: me.streak_count, xp: me.xp, level: me.level });
    }

    const { data: me } = await sb.from('users').select('streak_count, last_checkin').eq('id', user.id).single();
    const streak = (me.last_checkin === u.yesterdayUtc()) ? me.streak_count + 1 : 1;
    const { error: insErr } = await sb.from('checkins').insert({ user_id: user.id, date: today });
    if (insErr) throw insErr;
    await sb.from('users').update({ streak_count: streak, last_checkin: today }).eq('id', user.id);
    const xp = await u.addXp(user.id, 10);
    return u.send(res, 200, { already: false, streak, xp: xp.xp, level: xp.level, leveledUp: xp.leveledUp });
  } catch (e) {
    console.error('checkin error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

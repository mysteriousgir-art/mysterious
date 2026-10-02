// GET /api/me/progress  (auth required; daily task checklist)
const u = require('./../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const user = await u.requireAuth(req, res);
    if (!user) return;
    const sb = u.supabase();
    const today = u.todayUtc();

    const [{ data: me }, { data: checkin }, { data: read }, { data: quiz }, { data: game }] = await Promise.all([
      sb.from('users').select('streak_count, xp, level, last_checkin').eq('id', user.id).single(),
      sb.from('checkins').select('id').eq('user_id', user.id).eq('date', today).maybeSingle(),
      sb.from('note_reads').select('user_id').eq('user_id', user.id).gte('at', today + 'T00:00:00Z').limit(1).maybeSingle(),
      sb.from('quiz_attempts').select('user_id').eq('user_id', user.id).gte('at', today + 'T00:00:00Z').limit(1).maybeSingle(),
      sb.from('game_plays').select('user_id').eq('user_id', user.id).gte('at', today + 'T00:00:00Z').limit(1).maybeSingle(),
    ]);

    return u.send(res, 200, {
      streak: me.streak_count,
      xp: me.xp,
      level: me.level,
      lastCheckin: me.last_checkin,
      tasks: [
        { id: 'checkin', label: 'Daily check-in', done: !!checkin },
        { id: 'read', label: 'Read a note today', done: !!read },
        { id: 'quiz', label: 'Finish a quiz today', done: !!quiz },
        { id: 'game', label: 'Play a game today', done: !!game },
      ],
    });
  } catch (e) {
    console.error('progress error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

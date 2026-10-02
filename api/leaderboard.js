// GET /api/leaderboard  (top 20 by XP)
const u = require('../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const { data, error } = await u.supabase().from('users')
      .select('display_name, avatar, country, xp, level, streak_count')
      .eq('is_banned', 0)
      .order('xp', { ascending: false })
      .order('id', { ascending: true })
      .limit(20);
    if (error) throw error;
    return u.send(res, 200, (data || []).map((r) => ({
      displayName: r.display_name, avatar: r.avatar, country: r.country,
      xp: r.xp, level: r.level, streak: r.streak_count,
    })));
  } catch (e) {
    console.error('leaderboard error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

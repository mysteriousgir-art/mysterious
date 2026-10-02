// POST /api/games/play  (auth required; +5 XP)
const u = require('../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return u.methodNotAllowed(res, ['POST']);
  try {
    const user = await u.requireAuth(req, res);
    if (!user) return;
    const body = req.body || {};
    const game = String(body.game || '');
    const score = Number(body.score);
    if (!['memory', 'theorist'].includes(game)) return u.send(res, 400, { error: 'unknown game' });
    if (!Number.isInteger(score) || score < 0 || score > 100) {
      return u.send(res, 400, { error: 'score must be an integer 0..100' });
    }
    const { error } = await u.supabase().from('game_plays').insert({ user_id: user.id, game, score });
    if (error) throw error;
    const xp = await u.addXp(user.id, 5);
    return u.send(res, 200, { xp: xp.xp, level: xp.level, leveledUp: xp.leveledUp });
  } catch (e) {
    console.error('game play error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

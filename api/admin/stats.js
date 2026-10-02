// GET /api/admin/stats  (admin only; dashboard metrics)
const u = require('../../_lib/util');

function daysAgo(n) {
  const d = new Date();
  d.setUTCDate(d.getUTCDate() - n);
  return d.toISOString().slice(0, 10);
}

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const admin = await u.requireAdmin(req, res);
    if (!admin) return;
    const sb = u.supabase();
    const today = u.todayUtc();
    const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString();
    const monthAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString();

    const count = async (table, filter) => {
      let q = sb.from(table).select('id', { count: 'exact', head: true });
      if (filter) q = filter(q);
      const { count: c, error } = await q;
      if (error) throw error;
      return c || 0;
    };

    const totalUsers = await count('users');
    const bannedUsers = await count('users', (q) => q.eq('is_banned', 1));
    const newUsers7d = await count('users', (q) => q.gte('created_at', weekAgo));
    const newUsers30d = await count('users', (q) => q.gte('created_at', monthAgo));
    const totalMessages = await count('messages');
    const openReports = await count('reports', (q) => q.eq('status', 'open'));

    // DAU: distinct users active today across checkins, messages, quiz attempts, game plays.
    const [ci, mg, qa, gp] = await Promise.all([
      sb.from('checkins').select('user_id').eq('date', today),
      sb.from('messages').select('from_id').gte('created_at', today + 'T00:00:00Z'),
      sb.from('quiz_attempts').select('user_id').gte('at', today + 'T00:00:00Z'),
      sb.from('game_plays').select('user_id').gte('at', today + 'T00:00:00Z'),
    ]);
    const dauSet = new Set();
    (ci.data || []).forEach((r) => dauSet.add('c' + r.user_id));
    (mg.data || []).forEach((r) => dauSet.add('m' + r.from_id));
    (qa.data || []).forEach((r) => dauSet.add('q' + r.user_id));
    (gp.data || []).forEach((r) => dauSet.add('g' + r.user_id));
    const dau = dauSet.size;

    // Signups per day, last 7 days.
    const signupsSeries7d = [];
    for (let i = 6; i >= 0; i--) {
      const date = daysAgo(i);
      const c = await count('users', (q) => q.gte('created_at', date + 'T00:00:00Z').lt('created_at', daysAgo(i - 1) + 'T00:00:00Z'));
      signupsSeries7d.push({ date, count: c });
    }

    const { data: countries } = await sb.from('users').select('country');
    const countryMap = new Map();
    (countries || []).forEach((r) => {
      if (r.country) countryMap.set(r.country, (countryMap.get(r.country) || 0) + 1);
    });
    const topCountries = [...countryMap.entries()]
      .map(([country, count]) => ({ country, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 8);

    const { data: topNotes } = await sb.from('notes').select('title, read_count').order('read_count', { ascending: false }).limit(5);
    const { data: topQuizzes } = await sb.from('quizzes').select('title, play_count').order('play_count', { ascending: false }).limit(5);

    return u.send(res, 200, {
      totalUsers, bannedUsers, newUsers7d, newUsers30d, dau, signupsSeries7d, topCountries,
      topNotes: (topNotes || []).map((n) => ({ title: n.title, readCount: n.read_count })),
      topQuizzes: (topQuizzes || []).map((x) => ({ title: x.title, playCount: x.play_count })),
      openReports, totalMessages,
    });
  } catch (e) {
    console.error('admin stats error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

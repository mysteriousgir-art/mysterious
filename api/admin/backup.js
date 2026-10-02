// GET /api/admin/backup  (admin only; full JSON data dump download)
// Serverless has no .db file, so this exports every table as JSON.
const u = require('./../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const admin = await u.requireAdmin(req, res);
    if (!admin) return;
    const sb = u.supabase();
    const tables = ['users', 'sessions', 'notes', 'note_reads', 'quizzes', 'quiz_attempts',
      'checkins', 'game_plays', 'rooms', 'messages', 'blocks', 'reports'];
    const dump = { exported_at: u.isoNow(), tables: {} };
    for (const t of tables) {
      // Users table: never export password hashes.
      const cols = t === 'users' ? 'id, email, display_name, avatar, bio, country, is_admin, is_banned, xp, level, streak_count, last_checkin, created_at' : '*';
      const { data, error } = await sb.from(t).select(cols).limit(100000);
      if (error) throw error;
      dump.tables[t] = data || [];
    }
    const stamp = u.todayUtc();
    const body = JSON.stringify(dump);
    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Content-Disposition', `attachment; filename="mysterious-backup-${stamp}.json"`);
    res.end(body);
  } catch (e) {
    console.error('admin backup error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

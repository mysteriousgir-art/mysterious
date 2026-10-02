// GET /api/admin/reports  (admin only; open reports)
const u = require('../../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const admin = await u.requireAdmin(req, res);
    if (!admin) return;
    const sb = u.supabase();
    const { data: rows, error } = await sb.from('reports')
      .select('id, reason, status, created_at, reporter_id, reported_id')
      .eq('status', 'open').order('id', { ascending: false });
    if (error) throw error;

    const ids = [...new Set((rows || []).flatMap((r) => [r.reporter_id, r.reported_id]))];
    const names = new Map();
    if (ids.length) {
      const { data: users } = await sb.from('users').select('id, display_name').in('id', ids);
      (users || []).forEach((x) => names.set(x.id, x.display_name));
    }
    return u.send(res, 200, (rows || []).map((r) => ({
      id: r.id, reason: r.reason, status: r.status, createdAt: r.created_at,
      reporterId: r.reporter_id, reporterName: names.get(r.reporter_id) || '?',
      reportedId: r.reported_id, reportedName: names.get(r.reported_id) || '?',
    })));
  } catch (e) {
    console.error('admin reports error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

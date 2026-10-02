// GET /api/notes/:slug
const u = require('../../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const slug = String((req.query || {}).slug || '');
    const { data: n } = await u.supabase().from('notes')
      .select('id, slug, title, category, summary, points_json, read_count')
      .eq('slug', slug).maybeSingle();
    if (!n) return u.send(res, 404, { error: 'not found' });
    const points = u.asJson(n.points_json, []);
    return u.send(res, 200, { note: {
      id: n.id, slug: n.slug, title: n.title, category: n.category,
      summary: n.summary, readCount: n.read_count, points,
    }});
  } catch (e) {
    console.error('note detail error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

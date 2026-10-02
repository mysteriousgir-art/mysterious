// GET /api/notes?category=&q=
const u = require('../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const { category, q } = req.query || {};
    let query = u.supabase().from('notes').select('id, slug, title, category, summary, read_count').order('id', { ascending: true });
    if (category) query = query.eq('category', String(category));
    if (q) {
      const term = String(q).replace(/[%_,()]/g, '');
      query = query.or(`title.ilike.%${term}%,summary.ilike.%${term}%`);
    }
    const { data, error } = await query;
    if (error) throw error;
    return u.send(res, 200, (data || []).map((n) => ({
      id: n.id, slug: n.slug, title: n.title, category: n.category,
      summary: n.summary, readCount: n.read_count,
    })));
  } catch (e) {
    console.error('notes list error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

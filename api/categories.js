// GET /api/categories
const u = require('../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const { data, error } = await u.supabase().from('notes').select('category').order('category', { ascending: true });
    if (error) throw error;
    const cats = [...new Set((data || []).map((r) => r.category))];
    return u.send(res, 200, cats);
  } catch (e) {
    console.error('categories error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

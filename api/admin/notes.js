// POST /api/admin/notes  (admin only; create note)
const u = require('../../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return u.methodNotAllowed(res, ['POST']);
  try {
    const admin = await u.requireAdmin(req, res);
    if (!admin) return;
    const v = u.validateNoteBody(req.body || {});
    if (!v || !Array.isArray(v.points)) {
      return u.send(res, 400, { error: 'slug, title and points[] are required' });
    }
    const { data, error } = await u.supabase().from('notes').insert({
      slug: v.slug, title: v.title, category: v.category, summary: v.summary, points_json: v.points,
    }).select('id').single();
    if (error) {
      if (error.code === '23505') return u.send(res, 400, { error: 'slug already exists' });
      throw error;
    }
    return u.send(res, 201, { id: data.id });
  } catch (e) {
    console.error('admin note create error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

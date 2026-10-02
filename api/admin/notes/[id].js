// /api/admin/notes/:id — PUT (update) / DELETE (remove). Admin only.
const u = require('../../../_lib/util');

module.exports = async function handler(req, res) {
  try {
    const admin = await u.requireAdmin(req, res);
    if (!admin) return;
    const id = Number((req.query || {}).id);
    const sb = u.supabase();

    if (req.method === 'PUT') {
      const { data: existing } = await sb.from('notes').select('id').eq('id', id).maybeSingle();
      if (!existing) return u.send(res, 404, { error: 'not found' });
      const v = u.validateNoteBody(req.body || {});
      if (!v || !Array.isArray(v.points)) {
        return u.send(res, 400, { error: 'slug, title and points[] are required' });
      }
      const { error } = await sb.from('notes').update({
        slug: v.slug, title: v.title, category: v.category, summary: v.summary, points_json: v.points,
      }).eq('id', id);
      if (error) {
        if (error.code === '23505') return u.send(res, 400, { error: 'slug already exists' });
        throw error;
      }
      return u.send(res, 200, { ok: true });
    }

    if (req.method === 'DELETE') {
      await sb.from('note_reads').delete().eq('note_id', id);
      await sb.from('notes').delete().eq('id', id);
      return u.send(res, 200, { ok: true });
    }

    return u.methodNotAllowed(res, ['PUT', 'DELETE']);
  } catch (e) {
    console.error('admin note edit error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

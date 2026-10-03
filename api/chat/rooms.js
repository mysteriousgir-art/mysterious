// /api/chat/rooms
// GET  — list rooms (anyone)
// POST — create room (admin only) {name, description}
// DELETE ?slug=xxx — delete room (admin only)
const u = require('./../_lib/util');

function slugify(name) {
  return String(name || '').toLowerCase().trim()
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/[\s_]+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 60) || 'room';
}

module.exports = async function handler(req, res) {
  const sb = u.supabase();
  try {
    if (req.method === 'GET') {
      const { data, error } = await sb.from('rooms').select('slug, name, description, requires_approval').order('slug', { ascending: true });
      if (error) throw error;
      return u.send(res, 200, data || []);
    }

    if (req.method === 'POST') {
      const admin = await u.requireAdmin(req, res);
      if (!admin) return;
      const name = String((req.body || {}).name || '').trim();
      const description = String((req.body || {}).description || '').trim();
      const requires_approval = (req.body || {}).requires_approval ? 1 : 0;
      if (!name) return u.send(res, 400, { error: 'name is required' });
      let slug = slugify(name);
      // ensure unique slug
      const { data: existing } = await sb.from('rooms').select('slug');
      const taken = new Set((existing || []).map(r => r.slug));
      let base = slug, i = 2;
      while (taken.has(slug)) slug = base + '-' + (i++);
      const { data, error } = await sb.from('rooms').insert({ slug, name, description, requires_approval }).select('slug, name, description, requires_approval').single();
      if (error) throw error;
      return u.send(res, 201, data);
    }

    if (req.method === 'DELETE') {
      const admin = await u.requireAdmin(req, res);
      if (!admin) return;
      const slug = String((req.query || {}).slug || '').trim();
      if (!slug) return u.send(res, 400, { error: 'slug is required' });
      // don't delete the seeded core rooms
      const { error } = await sb.from('rooms').delete().eq('slug', slug);
      if (error) throw error;
      return u.send(res, 200, { ok: true });
    }

    return u.methodNotAllowed(res, ['GET', 'POST', 'DELETE']);
  } catch (e) {
    console.error('chat rooms error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

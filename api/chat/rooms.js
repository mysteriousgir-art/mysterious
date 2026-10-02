// GET /api/chat/rooms
const u = require('../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const { data, error } = await u.supabase().from('rooms').select('slug, name, description').order('slug', { ascending: true });
    if (error) throw error;
    return u.send(res, 200, data || []);
  } catch (e) {
    console.error('chat rooms error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

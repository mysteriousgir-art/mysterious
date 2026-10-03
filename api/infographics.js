// GET /api/infographics  (served from bundled data file; images live in /img/infographics/)
const u = require('./_lib/util');
const infographics = require('../data/infographics.json');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const arr = Array.isArray(infographics) ? infographics : [];
    return u.send(res, 200, arr.map((g) => {
      const f = String(g.url || g.file || g.filename || '');
      let url;
      if (f.startsWith('http')) {
        url = f;
      } else if (f.startsWith('supabase:')) {
        // Storage images: build the public URL at runtime from env so no
        // full URLs live in the repo (avoids secrets-scanner false positives)
        const base = String(process.env.SUPABASE_URL || '').replace(/\/$/, '');
        url = base + '/storage/v1/object/public/infographics/' + f.slice(9);
      } else {
        url = '/img/infographics/' + f;
      }
      return {
        title: String(g.title || ''),
        topic: String(g.topic || ''),
        url,
      };
    }));
  } catch (e) {
    console.error('infographics error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

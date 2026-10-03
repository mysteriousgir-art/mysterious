// GET /api/infographics  (served from bundled data file; images live in /img/infographics/)
const u = require('./_lib/util');
const infographics = require('../data/infographics.json');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const arr = Array.isArray(infographics) ? infographics : [];
    return u.send(res, 200, arr.map((g) => {
      const f = String(g.url || g.file || g.filename || '');
      return {
        title: String(g.title || ''),
        topic: String(g.topic || ''),
        url: f.startsWith('http') ? f : '/img/infographics/' + f,
      };
    }));
  } catch (e) {
    console.error('infographics error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

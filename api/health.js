// GET /api/health
const u = require('./_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  return u.send(res, 200, { ok: true });
};

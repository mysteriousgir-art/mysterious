// POST /api/auth/logout
const u = require('./../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return u.methodNotAllowed(res, ['POST']);
  try {
    await u.destroySession(req, res);
    return u.send(res, 200, { ok: true });
  } catch (e) {
    console.error('logout error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

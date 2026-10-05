// GET /api/admin/visits  (admin only; visitor analytics)
const u = require('./../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const admin = await u.requireAdmin(req, res);
    if (!admin) return;
    const sb = u.supabase();
    const today = u.todayUtc() + 'T00:00:00Z';
    const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString();

    // Today's visitors (sessions active today) + today's page views.
    const { data: todayRows } = await sb.from('visits')
      .select('page_views').gte('last_seen_at', today);
    const visitsToday = (todayRows || []).length;
    const pageViewsToday = (todayRows || []).reduce((s, r) => s + (r.page_views || 0), 0);

    // Recent visits (latest 60).
    const { data: recent } = await sb.from('visits')
      .select('id, created_at, last_seen_at, page_views, entry_page, last_page, country, timezone, device, user_id')
      .order('last_seen_at', { ascending: false }).limit(60);

    // Attach display names for logged-in visitors.
    const userIds = [...new Set((recent || []).map((r) => r.user_id).filter(Boolean))];
    let names = {};
    if (userIds.length) {
      const { data: users } = await sb.from('users').select('id, display_name').in('id', userIds);
      (users || []).forEach((x) => { names[x.id] = x.display_name; });
    }

    // Top pages (7d) + by country (7d).
    const { data: weekRows } = await sb.from('visits')
      .select('last_page, country').gte('last_seen_at', weekAgo).limit(2000);
    const pageMap = new Map(), countryMap = new Map();
    (weekRows || []).forEach((r) => {
      const p = r.last_page || '/';
      pageMap.set(p, (pageMap.get(p) || 0) + 1);
      const c = r.country || 'Unknown';
      countryMap.set(c, (countryMap.get(c) || 0) + 1);
    });
    const topPages = [...pageMap.entries()]
      .map(([page, count]) => ({ page, count })).sort((a, b) => b.count - a.count).slice(0, 8);
    const byCountry = [...countryMap.entries()]
      .map(([country, count]) => ({ country, count })).sort((a, b) => b.count - a.count).slice(0, 8);

    return u.send(res, 200, {
      visitsToday, pageViewsToday,
      recent: (recent || []).map((r) => ({
        id: r.id,
        firstSeen: r.created_at,
        lastSeen: r.last_seen_at,
        pageViews: r.page_views,
        entryPage: r.entry_page,
        lastPage: r.last_page,
        country: r.country || (r.timezone || ''),
        device: r.device,
        visitor: r.user_id ? (names[r.user_id] || ('user #' + r.user_id)) : 'Guest',
      })),
      topPages, byCountry,
    });
  } catch (e) {
    console.error('admin visits error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

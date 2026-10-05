// POST /api/track  (public; anonymous visit tracking, one row per visitor per day)
const crypto = require('crypto');
const u = require('./_lib/util');

// Best-effort timezone -> country mapping (no external API calls).
const TZ_COUNTRY = {
  'Asia/Karachi': 'Pakistan',
  'Asia/Kolkata': 'India', 'Asia/Calcutta': 'India',
  'Asia/Dhaka': 'Bangladesh',
  'Asia/Dubai': 'UAE', 'Asia/Muscat': 'Oman', 'Asia/Riyadh': 'Saudi Arabia',
  'Asia/Qatar': 'Qatar', 'Asia/Kuwait': 'Kuwait', 'Asia/Bahrain': 'Bahrain',
  'Europe/London': 'UK', 'Europe/Paris': 'France', 'Europe/Berlin': 'Germany',
  'America/New_York': 'USA', 'America/Chicago': 'USA', 'America/Los_Angeles': 'USA',
  'America/Toronto': 'Canada', 'Australia/Sydney': 'Australia',
};
function countryFromTimezone(tz) {
  if (!tz) return '';
  if (TZ_COUNTRY[tz]) return TZ_COUNTRY[tz];
  const parts = tz.split('/');
  if (parts.length === 2) return parts[1].replace(/_/g, ' ');
  return tz;
}

function clientIp(headers) {
  const h = headers || {};
  const xff = h['x-forwarded-for'] || h['x-nf-client-connection-ip'] || h['x-real-ip'] || '';
  return String(xff).split(',')[0].trim().slice(0, 45);
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return u.methodNotAllowed(res, ['POST']);
  try {
    const body = req.body || {};
    const page = String(body.page || '').slice(0, 120) || '/';
    const timezone = String(body.timezone || '').slice(0, 60);
    const device = String(body.device || '').slice(0, 20) || 'unknown';
    const ua = String((req.headers && req.headers['user-agent']) || '').slice(0, 200);
    const ip = clientIp(req.headers);
    const day = u.todayUtc();
    const sessionKey = crypto.createHash('sha256')
      .update(ip + '|' + ua + '|' + day).digest('hex').slice(0, 48);
    const country = countryFromTimezone(timezone);

    // Optional: link to logged-in user (never fails the track).
    let userId = null;
    try {
      const me = await u.getUser(req);
      if (me) userId = me.id;
    } catch (e) { /* ignore */ }

    const sb = u.supabase();
    const { data: existing } = await sb.from('visits')
      .select('id, page_views').eq('session_key', sessionKey).maybeSingle();

    if (existing) {
      const upd = {
        last_seen_at: new Date().toISOString(),
        page_views: (existing.page_views || 0) + 1,
        last_page: page,
      };
      if (userId) upd.user_id = userId;
      const { error } = await sb.from('visits').update(upd).eq('id', existing.id);
      if (error) throw error;
    } else {
      const { error } = await sb.from('visits').insert({
        session_key: sessionKey,
        entry_page: page,
        last_page: page,
        country, timezone, device,
        user_id: userId,
      });
      if (error) throw error;
    }
    return u.send(res, 200, { ok: true });
  } catch (e) {
    console.error('track error:', e.message);
    // Never break the page for a tracking failure.
    return u.send(res, 200, { ok: false });
  }
};

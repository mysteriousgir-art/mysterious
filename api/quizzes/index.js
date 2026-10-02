// GET /api/quizzes  (list; answers never exposed)
const u = require('./../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const { data, error } = await u.supabase().from('quizzes')
      .select('id, slug, title, note_slug, questions_json, play_count')
      .order('id', { ascending: true });
    if (error) throw error;
    return u.send(res, 200, (data || []).map((r) => ({
      id: r.id, slug: r.slug, title: r.title, noteSlug: r.note_slug,
      questionCount: u.asJson(r.questions_json, []).length,
      playCount: r.play_count,
    })));
  } catch (e) {
    console.error('quizzes list error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

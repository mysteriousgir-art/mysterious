// GET /api/quizzes/:slug  (public questions only — NEVER answers/explanations)
const u = require('./../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'GET') return u.methodNotAllowed(res, ['GET']);
  try {
    const slug = String((req.query || {}).slug || '');
    const { data: q } = await u.supabase().from('quizzes')
      .select('id, slug, title, questions_json').eq('slug', slug).maybeSingle();
    if (!q) return u.send(res, 404, { error: 'not found' });
    const questions = u.asJson(q.questions_json, []);
    const publicQuestions = questions.map((x) => ({ q: x.q, options: x.options }));
    return u.send(res, 200, { quiz: { id: q.id, slug: q.slug, title: q.title, questions: publicQuestions } });
  } catch (e) {
    console.error('quiz detail error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

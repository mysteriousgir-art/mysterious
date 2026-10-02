// POST /api/admin/quizzes  (admin only; create quiz)
const u = require('./../_lib/util');

function validQuiz(v) {
  return v && Array.isArray(v.questions) &&
    v.questions.every((x) => x.options.length === 4 && Number.isInteger(x.answer) && x.answer >= 0 && x.answer < 4);
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return u.methodNotAllowed(res, ['POST']);
  try {
    const admin = await u.requireAdmin(req, res);
    if (!admin) return;
    const v = u.validateQuizBody(req.body || {});
    if (!validQuiz(v)) {
      return u.send(res, 400, { error: 'slug, title and questions[{q,options[4],answer,explanation}] are required' });
    }
    const { data, error } = await u.supabase().from('quizzes').insert({
      slug: v.slug, title: v.title, note_slug: v.noteSlug, questions_json: v.questions,
    }).select('id').single();
    if (error) {
      if (error.code === '23505') return u.send(res, 400, { error: 'slug already exists' });
      throw error;
    }
    return u.send(res, 201, { id: data.id });
  } catch (e) {
    console.error('admin quiz create error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

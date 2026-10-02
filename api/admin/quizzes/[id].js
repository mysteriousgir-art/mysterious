// /api/admin/quizzes/:id — PUT (update) / DELETE (remove). Admin only.
const u = require('../../../_lib/util');

function validQuiz(v) {
  return v && Array.isArray(v.questions) &&
    v.questions.every((x) => x.options.length === 4 && Number.isInteger(x.answer) && x.answer >= 0 && x.answer < 4);
}

module.exports = async function handler(req, res) {
  try {
    const admin = await u.requireAdmin(req, res);
    if (!admin) return;
    const id = Number((req.query || {}).id);
    const sb = u.supabase();

    if (req.method === 'PUT') {
      const { data: existing } = await sb.from('quizzes').select('id').eq('id', id).maybeSingle();
      if (!existing) return u.send(res, 404, { error: 'not found' });
      const v = u.validateQuizBody(req.body || {});
      if (!validQuiz(v)) {
        return u.send(res, 400, { error: 'slug, title and questions[{q,options[4],answer,explanation}] are required' });
      }
      const { error } = await sb.from('quizzes').update({
        slug: v.slug, title: v.title, note_slug: v.noteSlug, questions_json: v.questions,
      }).eq('id', id);
      if (error) {
        if (error.code === '23505') return u.send(res, 400, { error: 'slug already exists' });
        throw error;
      }
      return u.send(res, 200, { ok: true });
    }

    if (req.method === 'DELETE') {
      await sb.from('quiz_attempts').delete().eq('quiz_id', id);
      await sb.from('quizzes').delete().eq('id', id);
      return u.send(res, 200, { ok: true });
    }

    return u.methodNotAllowed(res, ['PUT', 'DELETE']);
  } catch (e) {
    console.error('admin quiz edit error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

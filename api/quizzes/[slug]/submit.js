// POST /api/quizzes/:slug/submit  (auth required; grades server-side, +XP)
const u = require('../../_lib/util');

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return u.methodNotAllowed(res, ['POST']);
  try {
    const user = await u.requireAuth(req, res);
    if (!user) return;
    const slug = String((req.query || {}).slug || '');
    const sb = u.supabase();
    const { data: q } = await sb.from('quizzes')
      .select('id, questions_json, play_count').eq('slug', slug).maybeSingle();
    if (!q) return u.send(res, 404, { error: 'not found' });

    const questions = u.asJson(q.questions_json, []);
    const answers = (req.body || {}).answers;
    if (!Array.isArray(answers) || answers.length !== questions.length) {
      return u.send(res, 400, { error: 'answers array must match question count' });
    }
    const results = questions.map((quest, i) => {
      const correct = Number(answers[i]) === Number(quest.answer);
      return { correct, correctIndex: Number(quest.answer), explanation: quest.explanation || '' };
    });
    const score = results.filter((r) => r.correct).length;

    const { error: insErr } = await sb.from('quiz_attempts').insert({
      user_id: user.id, quiz_id: q.id, score, total: questions.length,
    });
    if (insErr) throw insErr;
    await sb.from('quizzes').update({ play_count: (q.play_count || 0) + 1 }).eq('id', q.id);

    const xp = await u.addXp(user.id, Math.max(5, score * 5));
    return u.send(res, 200, { score, total: questions.length, xp: xp.xp, leveledUp: xp.leveledUp, results });
  } catch (e) {
    console.error('quiz submit error:', e.message);
    return u.send(res, 500, { error: 'server error' });
  }
};

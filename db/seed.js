// db/seed.js — idempotent content seeder for Mysterious.
// Reads data/notes.json, data/quizzes.json, data/infographics.json and
// inserts notes/quizzes with INSERT OR IGNORE by slug. Also seeds chat rooms.
// Safe to run any number of times. Run with: npm run seed

require('dotenv').config();
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const DB_PATH = path.resolve(ROOT, process.env.DATABASE_PATH || './data/zehen.db');

let Database;
try {
  Database = require('better-sqlite3');
} catch (e) {
  console.error('better-sqlite3 is not installed. Run `npm install` first.');
  process.exit(1);
}

fs.mkdirSync(path.dirname(DB_PATH), { recursive: true });

const db = new Database(DB_PATH);
db.pragma('journal_mode = WAL');
db.exec(fs.readFileSync(path.join(__dirname, 'schema.sql'), 'utf8'));

function readJson(file) {
  const p = path.join(ROOT, 'data', file);
  try {
    const raw = fs.readFileSync(p, 'utf8');
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) {
      console.warn(`seed: ${file} is not an array — skipped`);
      return null;
    }
    return parsed;
  } catch (e) {
    console.warn(`seed: ${file} missing or invalid (${e.message}) — skipped`);
    return null;
  }
}

// --- rooms ---
const seedRooms = db.prepare('INSERT OR IGNORE INTO rooms(slug, name, description) VALUES (?, ?, ?)');
const roomTxn = db.transaction(() => {
  seedRooms.run('general', 'General Lounge', 'Hang out, chat and connect with fellow psychology learners.');
  seedRooms.run('exam-prep', 'Exam Prep', 'Study together, share tips and prep for psychology exams.');
  seedRooms.run('research-methods', 'Research Methods', 'Discuss research designs, statistics and methodology.');
});
roomTxn();
console.log('seed: rooms seeded');

// --- notes ---
const notes = readJson('notes.json');
if (notes) {
  const insNote = db.prepare(
    'INSERT OR IGNORE INTO notes(slug, title, category, summary, points_json) VALUES (?, ?, ?, ?, ?)'
  );
  let inserted = 0;
  const txn = db.transaction((rows) => {
    for (const n of rows) {
      if (!n || typeof n.slug !== 'string' || typeof n.title !== 'string') {
        console.warn('seed: skipping note with missing slug/title');
        continue;
      }
      const points = Array.isArray(n.points)
        ? n.points.map((p) =>
            typeof p === 'string' ? { point: p, example: '' } : { point: String(p.point || ''), example: String(p.example || '') }
          )
        : [];
      const r = insNote.run(n.slug, n.title, String(n.category || 'General'), String(n.summary || ''), JSON.stringify(points));
      inserted += r.changes;
    }
  });
  txn(notes);
  console.log(`seed: notes done (${inserted} inserted, ${notes.length} total in file)`);
}

// --- quizzes ---
const quizzes = readJson('quizzes.json');
if (quizzes) {
  const insQuiz = db.prepare(
    'INSERT OR IGNORE INTO quizzes(slug, title, note_slug, questions_json) VALUES (?, ?, ?, ?)'
  );
  let inserted = 0;
  const txn = db.transaction((rows) => {
    for (const q of rows) {
      if (!q || typeof q.slug !== 'string' || typeof q.title !== 'string') {
        console.warn('seed: skipping quiz with missing slug/title');
        continue;
      }
      const questions = Array.isArray(q.questions) ? q.questions : [];
      const r = insQuiz.run(q.slug, q.title, q.noteSlug || q.note_slug || null, JSON.stringify(questions));
      inserted += r.changes;
    }
  });
  txn(quizzes);
  console.log(`seed: quizzes done (${inserted} inserted, ${quizzes.length} total in file)`);
}

// --- infographics (no DB table; just validate the file parses) ---
const infographics = readJson('infographics.json');
if (infographics) {
  console.log(`seed: infographics.json ok (${infographics.length} entries)`);
}

console.log('seed: complete');
db.close();

# Mysterious — The Psychology Learning Universe

A warm, beautiful, full-stack psychology learning + community website. Notes library, infographics, daily streaks, XP & levels, quizzes, games, and a safe study community with 1:1 chat, study rooms, blocking and reporting — plus an owner-only admin dashboard.

**Owner:** Attiya Batool (Founder & Admin)

## Tech stack (Vercel edition)

- **Backend:** Vercel Serverless Functions (`api/**`, Node 24) — no always-on server
- **Database:** Supabase Postgres (free tier, Singapore region)
- **Frontend:** Multi-page app in `public/` — hand-crafted CSS + vanilla JS (no build step)
- **Auth:** email + password (bcrypt, 12 rounds), httpOnly cookie sessions (`mysterious_session`)
- **Chat:** REST polling (`GET /api/chat/messages` every 3s) — no websockets needed
- **Safety:** HTML-escaping + profanity filter, `is_admin` checked server-side on every admin request

## Project layout

```
~/workspace/zehen/
├── api/                 # serverless functions (one file per endpoint)
│   ├── _lib/util.js     # supabase client, auth, validators, chat helpers
│   ├── auth/            # signup, login, logout, me
│   ├── chat/            # rooms, conversations, messages (poll), send
│   ├── admin/           # stats, users, ban/unban, notes & quizzes CRUD, reports, backup
│   └── ...              # notes, quizzes, checkin, games, leaderboard, profile, blocks
├── supabase/
│   └── schema.sql       # Postgres DDL + seed data (paste into Supabase SQL Editor)
├── data/
│   ├── notes.json       # 10 psychology notes (points + everyday examples)
│   ├── quizzes.json     # 5 MCQ quizzes (44 questions, explanations)
│   └── infographics.json# gallery manifest
├── public/              # frontend (10 pages, css/, js/, img/infographics/)
├── test/
│   └── harness.js       # node test/harness.js — unit + live-API tests
├── vercel.json          # static + functions routing config
├── package.json         # name: "mysterious"
├── .env.example         # env var template (copy values into Vercel, never commit)
└── README.md
```

## One-time setup: Supabase

1. Supabase dashboard → your `mysterious` project → **SQL Editor** → New query.
2. Paste the **entire** `supabase/schema.sql` file → **Run**.
3. Verify: `SELECT count(*) FROM notes;` → 10, `SELECT count(*) FROM quizzes;` → 5, `SELECT count(*) FROM rooms;` → 3.

## Deploy free: Vercel

1. Push the `vercel-rework` branch to GitHub.
2. Vercel → Add New → Project → import the repo → select branch **`vercel-rework`**.
3. Environment variables (Project → Settings → Environment Variables):
   - `SUPABASE_URL` = your project URL (`https://….supabase.co`)
   - `SUPABASE_SECRET_KEY` = the **secret** key (`sb_secret_…`) — server-side only
   - `ADMIN_EMAIL` = your own email address (the owner's)
   - `SESSION_SECRET` = any long random string
4. Deploy. Open the URL and **sign up with your `ADMIN_EMAIL`** → you become admin.

## The admin account (important)

There is **exactly one way** to become admin, and no API, button, or page can grant it:

1. Set `ADMIN_EMAIL` in Vercel env vars to **your own email address** (the owner's).
2. Sign up on the site with that exact email.
3. On signup/login the API marks that account `is_admin = 1`.

Every `/api/admin/*` function re-reads `is_admin` from the database and returns **403** for anyone else. Never share your admin login, and never set `ADMIN_EMAIL` to an address you don't control.

## Custom domain (your own branded URL)

1. Buy a domain from any registrar.
2. Vercel → your project → Settings → Domains → add the domain. Vercel shows the DNS records.
3. Add those records at your registrar. Vercel provisions free HTTPS automatically.

## Data & backups

- All data lives in **Supabase Postgres** — it survives redeploys (unlike server-local SQLite).
- Free Supabase projects **pause after 7 days of zero activity**; any real visit wakes them. Keep the site visited at least weekly.
- **Backup:** the admin panel has a "Download database backup" button → exports every table as JSON (password hashes are never included).

## Run the tests

```bash
cd ~/workspace/zehen
# .env.supabase must exist (SUPABASE_URL + SUPABASE_SECRET_KEY) — schema.sql must be loaded first
node test/harness.js
```

The harness runs pure-logic unit tests always, then (only if the Supabase schema exists) full live-API tests: signup/login/sessions, notes, quizzes + grading, streaks, XP, chat send/poll/DM, block/report, admin guards (403 for non-admins), and the JSON backup — cleaning up its test rows afterwards.

## Features checklist

- Auth & profiles (avatar picker, bio, country), notes library (search + categories), 8 HD infographics, daily streaks + XP/levels + daily tasks, 5 quizzes with instant scoring & explanations, memory-match + guess-the-theorist games + leaderboard, study rooms & 1:1 chat (polling), blocking, user reports, profanity filter, admin dashboard (users, DAU, signups chart, top countries, popular content, user ban, content CRUD, report review, JSON backup).

## Notes on the old version

The original `main` branch runs Express + SQLite + Socket.io on one server (see git history). The `vercel-rework` branch is a full port: same UI, same API shapes, same rules — new transport (serverless + Postgres + polling chat).

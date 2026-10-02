# Mysterious — The Psychology Learning Universe

A warm, beautiful, full-stack psychology learning + community website. Notes library, infographics, daily streaks, XP & levels, quizzes, games, and a safe study community with 1:1 chat, study rooms, blocking and reporting — plus an owner-only admin dashboard.

**Owner:** Attiya Batool (Founder & Admin)

## Tech stack

- **Backend:** Node.js + Express + better-sqlite3 + Socket.io (one single service)
- **Frontend:** Multi-page app in `public/` — hand-crafted CSS + vanilla JS (no build step)
- **Auth:** email + password (bcrypt, 12 rounds), httpOnly cookie sessions (`mysterious_session`)
- **Safety:** rate-limited auth/chat endpoints, HTML-escaping + profanity filter, `is_admin` checked server-side on every admin request

## Project layout

```
~/workspace/zehen/
├── server.js            # Express + Socket.io app (API, chat, admin)
├── db/
│   ├── schema.sql       # SQLite schema (13 tables)
│   └── seed.js          # idempotent seeder (rooms, notes, quizzes)
├── data/
│   ├── notes.json       # 10 psychology notes (points + everyday examples)
│   ├── quizzes.json     # 5 MCQ quizzes (44 questions, explanations)
│   └── infographics.json# gallery manifest
├── public/              # frontend (10 pages, css/, js/, img/infographics/)
├── package.json         # name: "mysterious"
├── .env.example         # copy to .env and fill in
└── README.md
```

## Run locally

```bash
cd ~/workspace/zehen
cp .env.example .env
# Edit .env: set a long random SESSION_SECRET and your ADMIN_EMAIL
npm install
node db/seed.js        # seeds notes/quizzes/rooms (safe to re-run)
npm start              # → http://localhost:3000
```

## The admin account (important)

There is **exactly one way** to become admin, and no API, button, or page can grant it:

1. Set `ADMIN_EMAIL` in `.env` to **your own email address** (the owner's).
2. Sign up on the site with that exact email.
3. On signup/login the server marks that account `is_admin = 1`.

Every `/api/admin/*` endpoint re-reads `is_admin` from the database and returns **403** for anyone else. Never share your admin login, and never set `ADMIN_EMAIL` to an address you don't control.

## Deploy free (one service)

**Render (recommended):**
1. Push this folder to a GitHub repo.
2. Render → New → Web Service → connect the repo.
3. Build command: `npm install` · Start command: `npm start`.
4. Environment: `NODE_VERSION=24`, `SESSION_SECRET=<long random string>`, `ADMIN_EMAIL=<your email>`.
5. Add a **persistent disk** mounted at `/opt/render/project/src/data` (this is where `zehen.db` lives — without a disk, the database is wiped on every deploy/restart).
6. Deploy, open the URL, sign up with your `ADMIN_EMAIL` → you're admin.

**Railway:** same idea — new service from repo, add a Volume mounted at the `data/` path, set the same env vars.

## Custom domain (your own branded URL, not AI-generated)

1. Buy a domain (e.g. `mysteriouslearn.com`) from any registrar (Namecheap, Cloudflare, GoDaddy…).
2. In Render: Service → Settings → Custom Domains → add your domain. Render shows you the DNS records to create.
3. In your registrar's DNS: add the records Render gives you (usually a CNAME for `www` and an A/ALIAS for the root).
4. Wait for DNS to propagate (minutes to a few hours), Render provisions free HTTPS automatically.

## Data persistence notes

- The app uses **SQLite** (`data/zehen.db`) — simple, free, and plenty for a community site. On hosts with ephemeral filesystems (Render/Railway free tiers) you **must** attach a persistent disk/volume or the database resets on redeploy.
- **Optional Postgres path:** if you outgrow SQLite, swap `better-sqlite3` for `pg` + a small query wrapper, move the schema to Postgres dialect, and point `DATABASE_URL` at a free Postgres (Supabase, Neon, Render Postgres). The API layer is the only place that touches SQL.
- Backups: download `data/zehen.db` periodically from your host's disk/volume panel.

## Features checklist

- Auth & profiles (avatar picker, bio, country), notes library (search + categories), 8 HD infographics, daily streaks + XP/levels + daily tasks, 5 quizzes with instant scoring & explanations, memory-match + guess-the-theorist games + leaderboard, Socket.io study rooms & 1:1 chat, blocking, user reports, profanity filter, admin dashboard (users, DAU, signups chart, top countries, popular content, user ban, content CRUD, report review).

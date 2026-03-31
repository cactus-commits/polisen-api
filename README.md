# polisen-api

A simple sync script that pulls the 500 latest events from the Swedish Police API and stores them in a Supabase database. Runs automatically every day via GitHub Actions.

---

## Why this exists

I wanted an easy way to collect and query Swedish police events over time, since the official API only returns the latest 500.

---

## Set it up yourself

**1. Clone the repo**
```bash
git clone https://github.com/your-username/polisen-api.git
cd polisen-api
```

**2. Install dependencies**
```bash
uv sync
```

**3. Set up environment**
```bash
cp .env.example .env
# Fill in your Supabase URL and key
```

**4. Create the database table**

Run this in your Supabase SQL editor:
```sql
CREATE TABLE police_events (
  id INTEGER PRIMARY KEY,
  datetime TIMESTAMPTZ NOT NULL,
  name TEXT NOT NULL,
  summary TEXT,
  url TEXT,
  type TEXT,
  location_name TEXT,
  location_gps TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**5. Run manually**
```bash
uv run sync.py
```

---

## Automate with GitHub Actions

1. Push the repo to GitHub
2. Go to **Settings → Secrets and variables → Actions**
3. Add two secrets: `SUPABASE_URL` and `SUPABASE_KEY`

The workflow in `.github/workflows/sync.yml` will then run every day at 06:00 UTC.

---

## Built with

- [Python](https://python-poetry.org/) — scripting
- [httpx](https://www.python-httpx.org/) — HTTP requests
- [Supabase](https://supabase.com/) — database
- [uv](https://github.com/astral-sh/uv) — package management
- [GitHub Actions](https://github.com/features/actions) — scheduling

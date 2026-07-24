# snip — a URL shortener

Full-stack starter: FastAPI + SQLite backend, React (Vite) frontend.

## Run the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at http://localhost:8000. Interactive API docs at http://localhost:8000/docs — useful for testing endpoints before the frontend is wired up. A `shortener.db` SQLite file is created automatically on first run.

## Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173 and talks to the backend at localhost:8000 (see `src/api.js` — CORS is already configured on the backend for this origin).

## How it works

- `POST /api/links` creates a short code (random 6-char, or your custom one) for a URL.
- `GET /{code}` redirects to the original URL and increments `click_count`.
- `GET /api/links` lists everything, powering the dashboard table.

## Suggested build order (good if this is your first full-stack project)

1. Get the backend running, create a link via `/docs`, confirm the redirect works in a browser tab.
2. Get the frontend rendering with a hardcoded links list (no API calls yet) — get the UI right first.
3. Wire up `ShortenForm` to `POST /api/links`.
4. Wire up `LinkList` to `GET /api/links`.
5. Deploy: frontend to Vercel/Netlify, backend to Railway/Render/Fly.io. Swap SQLite for a Postgres URL in `database.py` once you deploy (SQLite files don't persist well on most hosting platforms).

## Stretch goals (once the core works)

- **Link expiry**: add an `expires_at` column, return 410 Gone past expiry.
- **QR codes**: generate one per link (the `qrcode` Python package is a one-liner).
- **Per-user accounts**: add auth so links belong to a user, not a shared pool.
- **Click analytics**: log each redirect (timestamp, referrer) in a separate table instead of just a counter — gives you a chart to build on the dashboard.
- **Rate limiting**: prevent someone from mass-creating links.

Any one of these is a good "what did you add beyond the basics" talking point for interviews.

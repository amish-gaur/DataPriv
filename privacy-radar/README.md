# Student Privacy Radar

Chrome extension + FastAPI backend + Next.js dashboard to summarize any site's Privacy Policy/ToS and assign a risk score.

## Quickstart (docker)
1. `cp .env.example .env` and fill variables as needed.
2. `docker compose up --build`
3. Load the extension:
   - go to `chrome://extensions` → Developer Mode → Load unpacked → select `extension/`
4. Visit any site → click the extension → see summary & score.
5. Dashboard at `http://localhost:3000`.

## Dev (no docker)
- Backend: `cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --reload`
- Dashboard: `cd dashboard && npm i && npm run dev`

## Env
- `OPENAI_API_KEY` optional (uses heuristic/extractive summary if unset).
- Backend swagger: `http://localhost:8000/docs`

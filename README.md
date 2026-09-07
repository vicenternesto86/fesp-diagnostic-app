# FESP Diagnostic App

Assessment platform for the **Essential Public Health Functions (EPHF/FESP)**
at state and health-district level. Health authorities score each function
against a consolidated rapid-diagnostic instrument; the system aggregates the
results into comparable indicators and reports.

**Live demo: [fesp-dx.vercel.app](https://fesp-dx.vercel.app)**

*Versión en español: [README.es.md](README.es.md)*

## Why

The Essential Public Health Functions framework is the standard way of asking
whether a health authority can actually do its job — surveillance, response,
regulation, workforce, access. The assessment is normally run on paper or in a
spreadsheet, once, and then the result is hard to compare across districts or
across years. This turns it into a system: role-based capture, automatic
scoring, and a dashboard that holds the comparison.

## Features

- Structured capture of the consolidated FESP instrument, by state and by health district
- Role-based access: administrators, and writers scoped to their own territory
- Automatic scoring and indicator computation (`app/utils/calculations.py`)
- Dashboard with aggregate results and per-district comparison
- Report generation

## Stack

FastAPI · SQLAlchemy · JWT auth · React + Vite · deployed on Vercel

## Run locally

**Backend**

```bash
cd backend
python -m venv venv
venv\Scripts\activate            # Windows
# source venv/bin/activate       # Linux/macOS

pip install -r requirements.txt
python seed_data.py              # loads reference data and demo users
uvicorn app.main:app --reload
```

Backend at http://localhost:8000 — interactive API docs at http://localhost:8000/docs

**Frontend**

```bash
cd frontend
npm install
npm run dev                      # http://localhost:5173
```

Windows users can run `INSTALAR.bat` once and `INICIAR_APP.bat` thereafter.

## Demo accounts

Created by `seed_data.py` for local and demo use only. Change them before any
real deployment.

| Email | Password | Role |
|---|---|---|
| admin@fesp.gob.mx | admin123 | Administrator |
| captura.tam@fesp.gob.mx | captura123 | Writer, state level |

## Layout

```
backend/app/
  models/      SQLAlchemy: state, jurisdiction, assessment, user
  routers/     auth, states, jurisdictions, assessments, dashboard, reports, users
  schemas/     Pydantic contracts
  utils/       auth, scoring calculations
  fesp_items.py  the instrument itself
frontend/      React + Vite
```

Built by [Vicente Ernesto González-Aramayo, PhD](https://github.com/vicenternesto86),
epidemiologist (INSP Mexico), for public health use.

## License

MIT

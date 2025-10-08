# Compass Risk Scanner API

FastAPI service to upload an Excel knowledge base and query it by sections and technologies, with JWT auth. Swagger UI is enabled by default.

## Requirements
- Python 3.11+
- pip

## Setup
```bash
python -m venv .venv
. .venv/Scripts/activate  # on Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run
```bash
uvicorn app.main:app --reload
```

Open Swagger UI at: http://127.0.0.1:8000/docs

### Auth
- Click "Authorize" in Swagger.
- Username: `admin`
- Password: `admin`

### Endpoints
- `POST /auth/login` – obtain JWT access token
- `GET /auth/me` – current user profile
- `POST /upload/excel` – upload `.xlsx` knowledge base; columns for section/technology are inferred
- `GET /upload/status` – simple count of indexed rows
- `POST /query/search` – query with `sections`, `technologies`, and `top_k`

Notes:
- Excel format is flexible. First row is treated as headers; all columns are indexed.
- Column names are heuristically mapped to logical `section` and `technology` using hints in `app/config.py`.
- Data is stored in-memory for now (resets on server restart).

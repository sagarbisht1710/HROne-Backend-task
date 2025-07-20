# FastAPI E-Commerce Backend

Implements product & order endpoints with MongoDB (Motor). See main project documentation for details.

## Quick Start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
or
python -m uvicorn app.main:app --reload --port 8008
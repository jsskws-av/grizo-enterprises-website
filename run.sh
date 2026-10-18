#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -r requirements.txt
fi

echo "Initializing database..."
PYTHONPATH=. .venv/bin/python database/seed_data.py

echo "Starting AI E-Commerce Automation Platform..."
echo "Web Dashboard: http://localhost:8000"
echo "API Docs:      http://localhost:8000/docs"
PYTHONPATH=. .venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --reload

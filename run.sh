#!/usr/bin/env bash
set -e
export $(grep -v '^#' .env | xargs -d '\n')
uvicorn app.main:app --host 0.0.0.0 --port $PORT

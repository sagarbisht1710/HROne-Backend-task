#!/usr/bin/env bash
set -e
export $(grep -v '^#' .env | xargs -d '\n')
uvicorn app.main:app --reload --port 8000
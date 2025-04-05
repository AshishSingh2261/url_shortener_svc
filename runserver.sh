#!/bin/bash

export PYTHONPATH=/app
export PORT=5000

echo "Starting DEVELOPMENT Service"
PYTHONDONTWRITEBYTECODE=1 uvicorn src.server:app --host 0.0.0.0 --port $PORT --reload --no-server-header


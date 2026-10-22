#!/bin/sh
set -e

echo "Starting DocumentReady production container..."

# Port handling for Render (Render dynamically assigns $PORT, default 10000)
PORT="${PORT:-10000}"
WORKERS="${WEB_CONCURRENCY:-2}"
TIMEOUT="${GUNICORN_TIMEOUT:-120}"

echo "Configuring Gunicorn on port ${PORT} with ${WORKERS} workers..."

# Execute Gunicorn as the main container process
exec gunicorn \
    --bind "0.0.0.0:${PORT}" \
    --workers "${WORKERS}" \
    --threads 4 \
    --timeout "${TIMEOUT}" \
    --access-logfile "-" \
    --error-logfile "-" \
    --log-level "info" \
    "run:app"

#!/bin/sh
set -e

# small Python-based wait-for-db that retries until DB is ready
python - <<'PY'
import os, time
from sqlalchemy import create_engine
url = os.environ.get("DATABASE_URL")
if not url:
    print("DATABASE_URL not set; aborting")
    raise SystemExit(1)

# try to connect repeatedly
for i in range(60):
    try:
        engine = create_engine(url)
        conn = engine.connect()
        conn.close()
        print("Database is ready")
        break
    except Exception as e:
        print("Waiting for database... attempt", i+1, "error:", str(e))
        time.sleep(1)
else:
    print("Database did not become ready in time")
    raise SystemExit(1)
PY

# Run migrations
echo "Running migrations..."
poetry run alembic upgrade head

# Start the app
echo "Starting uvicorn..."
exec poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000

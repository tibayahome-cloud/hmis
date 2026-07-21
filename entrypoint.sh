#!/bin/sh
set -e

echo "Waiting for database..."
until python -c "
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings

async def check():
    engine = create_async_engine(settings.DATABASE_URL)
    async with engine.connect():
        pass
    await engine.dispose()

asyncio.run(check())
" 2>/dev/null; do
  sleep 1
done
echo "Database is up."

echo "Running migrations..."
alembic upgrade head

echo "Starting app..."
exec "$@"

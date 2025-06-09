#!/bin/sh

alembic upgrade head # убрать перед продакшеном

gunicorn src.api.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

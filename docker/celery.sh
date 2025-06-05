#!/bin/sh

celery --app=src.api.background_tasks.celery_task:celery_app worker -l INFO

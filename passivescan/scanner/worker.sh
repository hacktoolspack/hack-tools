export C_FORCE_ROOT=1
celery -A scan_tasks worker --loglevel=info
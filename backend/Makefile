# VARIABLES
#------------------------------------------
MANAGE = python manage.py

# BASE COMMANDS
# ------------------------------------------------------------------------------
run:
	uvicorn config_fastapi.app:app_fastapi --reload

socketio:
	uvicorn config_socketio.app:app_socketio --port 8001 --host localhost --reload

run-local:
	$(MANAGE) migrate
	$(MANAGE) collectstatic --noinput
	$(MANAGE) init_project
	uvicorn config_fastapi.app:app_fastapi --port 8000 --host 0.0.0.0 --reload

socketio-local:
	uvicorn config_socketio.app:app_socketio --port 8001 --host 0.0.0.0

django-local:
	cat 'todo'
	#gunicorn config.asgi:fastapp --workers 4 --worker-class uvicorn.workers.UvicornWorker

# DB
# ------------------------------------------------------------------------------
migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

reset:
	python manage.py reset_db

# CELERY
# ------------------------------------------------------------------------------

beat:
	celery -A config_celery.app:app_celery beat -l info

worker:
	# --pool=gevent --concurrency=500
	celery -A config_celery.app:app_celery worker -l info --concurrency=4

purge:
	celery -A config_celery.app:app_celery purge

flower:
	celery flower --app=config_celery.app:app_celery --address=localhost --port=5555

flower-container:
	celery flower \
		--app=config_celery.app:app_celery \
		--broker="${CELERY_BROKER_URL}" \
		--basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}" \
		--address=0.0.0.0 \
		--port=5555

# LINTING
# ------------------------------------------------------------------------------
flake8:
	flake8

black:
	black .

isort:
	isort .

# LOAD TEST
# ------------------------------------------------------------------------------
locust:
	locust

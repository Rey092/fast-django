# BASE COMMANDS
# ------------------------------------------------------------------------------
run:
	uvicorn config.asgi:fastapp --reload

gunicorn:
	gunicorn config.asgi:fastapp --workers 4 --worker-class uvicorn.workers.UvicornWorker

# DB
# ------------------------------------------------------------------------------
migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

# TEST
# ------------------------------------------------------------------------------
locust:
	locust

locust-swarm:
	locust --master & locust --worker & locust --worker & locust --worker & locust --worker & locust --worker

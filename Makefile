
up:
	sudo docker compose up --build

vue-install:
	npm install --prefix ./backend_vue

vue-watch:
	npm run watch --prefix ./backend_vue

dev-up:
	npm install --prefix ./backend_vue
	npm run build --prefix ./backend_vue
	sudo docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build

dev-down:
	sudo docker compose -f docker-compose.yaml -f docker-compose.dev.yaml down

prod-up:
	npm install --prefix ./backend_vue
	npm run build --prefix ./backend_vue
	sudo docker compose -f docker-compose.yaml -f docker-compose.prod.yaml up --build

prod-down:
	sudo docker compose -f docker-compose.yaml -f docker-compose.prod.yaml down

clean-db:
	sudo docker container rm local_postgres_data

docker-dbexport:
	sudo docker exec -it backend_postgres_db pg_dump -U backend_admin -d backend_db > export_backend.psql

docker-logs:
	sudo docker logs backend_backend

docker-shell:
	sudo docker exec -it backend_backend poetry run python manage.py shell

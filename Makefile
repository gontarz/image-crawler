PROJECT_NAME=semantive_crawler


all: run

run:
	@docker-compose up

stop:
	@docker-compose stop

down:
	@docker-compose down

migrations:
	@docker exec -it image_crawler alembic revision --autogenerate;

migrate:
	@docker exec -it image_crawler alembic upgrade head;

psql:
	@docker exec -it image_crawler_postgres psql -U postgres

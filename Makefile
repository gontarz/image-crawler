PROJECT_NAME=semantive_crawler


all: run

run:
	@docker-compose up

stop:
	@docker-compose stop

down:
	@docker-compose down

migrations:
	@docker exec -it semantive_crawler alembic revision --autogenerate;

migrate:
	@docker exec -it semantive_crawler alembic upgrade head;

psql:
	@docker exec -it semantive_crawler_postgres psql -U postgres

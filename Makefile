init-db:
	python scripts/init_db.py

seed-default:
	python scripts/seed_faq.py --file data/faq_seed.json

seed:
	python scripts/seed_faq.py --file $(FILE)

update-embeddings:
	python scripts/update_null_embeddings.py

update-all-embeddings:
	python scripts/update_all_embeddings.py

build:
	docker compose -f infra/docker-compose.yaml build --no-cache api worker redis db

up:
	docker compose -f infra/docker-compose.yaml up -d

down:
	docker compose -f infra/docker-compose.yaml down

erase:
	docker compose -f infra/docker-compose.yaml down -v

up-db:
	docker compose -f infra/docker-compose.yaml up -d db

down-db:
	docker compose -f infra/docker-compose.yaml down db

erase-db:
	docker compose -f infra/docker-compose.yaml down -v db

logs-all:
	docker compose -f infra/docker-compose.yaml logs -f api worker redis db

logs-api:
	docker compose -f infra/docker-compose.yaml logs -f api

health:
	curl -s http://localhost:8000/health

test-it:
	curl -s http://localhost:8000/ask-question -H "Authorization: Bearer dev-token" -H "Content-Type: application/json" -d '{"user_question":"Can i change my email?"}'

test-non-it:
	curl -s http://localhost:8000/ask-question -H "Authorization: Bearer dev-token" -H "Content-Type: application/json" -d '{"user_question":"Can i get a day off?"}'

test-openai:
	curl -s http://localhost:8000/ask-question -H "Authorization: Bearer dev-token" -H "Content-Type: application/json" -d '{"user_question":"How to add another mail adress?"}'

init-db:
	docker compose -f infra/docker-compose.yaml exec api python scripts/init_db.py

seed:
	docker compose -f infra/docker-compose.yaml exec api python scripts/seed_faq.py

build:
	docker compose -f infra/docker-compose.yaml build --no-cache api db

up:
	docker compose -f infra/docker-compose.yaml up -d

down:
	docker compose -f infra/docker-compose.yaml down

logs:
	docker compose -f infra/docker-compose.yaml logs -f api db

logs-api:
	docker compose -f infra/docker-compose.yaml logs -f api

health:
	curl -s http://localhost:8000/health curl -s http://localhost:8000/health

test-good:
	curl -s http://localhost:8000/ask-question -H "Authorization: Bearer dev-token" -H "Content-Type: application/json" -d '{"user_question":"How to change 2fa?"}'

test-bad:
	curl -s http://localhost:8000/ask-question -H "Authorization: Bearer dev-token" -H "Content-Type: application/json" -d '{"user_question":"Can i set up 2fa?"}'

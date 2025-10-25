.PHONY: run lint type test

run:
	uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

lint:
	ruff check .

type:
	mypy src

test:
	pytest -q

run: 
	../.venv/bin/python -m app.main

test: 
	pytest

lint:
	ruff check --fix .
	black .

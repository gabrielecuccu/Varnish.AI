run: 
	../.venv/bin/python -m app.main

test: 
	pytest --cov=app --cov-report=html tests/

report:
	open htmlcov/index.html 	

lint:
	ruff check --fix .
	black .

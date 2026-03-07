install:
	pip install -r requirements.txt

run: 
	python3 -m app.main

test: 
	pytest --cov=app --cov-report=html tests/

report:
	open htmlcov/index.html 	

lint:
	ruff check --fix .
	black .

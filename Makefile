install:
	pip install -r requirements.txt

lint:
	pylint *.py

test:
	python -m pytest
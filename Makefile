
pylint:
	pylint main.py

run:
	python main.py

test:
	coverage run -m pytest
	coverage report main.py

db:
	alembic revision --autogenerate

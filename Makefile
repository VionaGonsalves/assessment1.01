
pylint:
	pylint main.py

run:
	python main.py

test:
	coverage run -m pytest
	coverage report main.py

db:
	alembic upgrade 2edb6d0fc975



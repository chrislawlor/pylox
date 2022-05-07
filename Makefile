ast:
	python src/generate_ast.py
	black src/pylox/expr.py

test:
	pytest -n 4 --cov-report term-missing --cov-report xml --cov=pylox  tests

POETRY_ENV_NAME := reportgen

.PHONY: env-create env-remove format lint test check type-checking

env-create:
	@poetry install

env-remove:
	@poetry env remove $(POETRY_ENV_NAME)

format:
	@poetry run ruff format .

lint:
	@poetry run ruff check --fix .

type-checking:
	@poetry run mypy .

check: format lint type-checking

test: 
	@poetry run python -m pytest -vv

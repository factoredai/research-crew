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

# TODO: A lot of typing issues here, need to work on them later
type-checking:
	@poetry run mypy .

check: format lint type-checking

# TODO: Tests are not implemented yet
test: 
	@poetry run python -m pytest -vv

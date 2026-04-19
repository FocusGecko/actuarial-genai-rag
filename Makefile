<<<<<<< HEAD
.PHONY: install install-dev test lint format typecheck clean
=======
.PHONY: install install-dev test lint format typecheck pre-commit clean
>>>>>>> 86ade3d (feat: add pre commit)

install:
	uv sync

install-dev:
	uv sync --extra dev

test:
	uv run pytest tests/ -v --cov=src

lint:
	uv run ruff check src/ tests/

format:
	uv run ruff format src/ tests/

typecheck:
	uv run mypy src/

<<<<<<< HEAD
=======
pre-commit:
	uv run pre-commit install
	uv run pre-commit run --all-files

>>>>>>> 86ade3d (feat: add pre commit)
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .mypy_cache -exec rm -rf {} +
	find . -name "*.pyc" -delete

.PHONY: install test lint build clean publish-test publish

# Installation
install:
	uv sync --all-extras

# Testing
test:
	uv run pytest tests/ -v

test-cov:
	uv run pytest tests/ --cov=src/ --cov-report=html --cov-report=term

# Code quality
lint:
	uv run black --check src/
	uv run isort --check-only src/
	uv run flake8 src/

format:
	uv run black src/
	uv run isort src/

# Building
build:
	uv build

# Cleanup
clean:
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

# Publishing
check:
	uv run twine check dist/*

publish-test: build check
	uv run twine upload --repository testpypi dist/*

publish: build check
	uv run twine upload dist/*

# Development workflow
dev-setup: install
	@echo "Development environment setup complete!"
	@echo "Run 'make test' to run tests"
	@echo "Run 'make lint' to check code quality"

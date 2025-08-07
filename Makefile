.PHONY: help install test lint format clean dev-install

# Default target
help:
	@echo "Claude Code Session Automation - Development Commands"
	@echo ""
	@echo "Available targets:"
	@echo "  install      Install the package"
	@echo "  dev-install  Install with development dependencies"
	@echo "  test         Run test suite"
	@echo "  lint         Run code linting"
	@echo "  format       Format code with black and isort"
	@echo "  clean        Clean build artifacts"
	@echo "  ci           Run full CI pipeline locally"
	@echo ""

# Installation targets
install:
	pip install -e .

dev-install:
	pip install -e ".[dev]"

# Testing
test:
	python -m pytest test/ -v --cov=src --cov-report=html --cov-report=term

test-quick:
	python -m pytest test/ -x

# Code quality
lint:
	flake8 src/ test/
	black --check src/ test/
	isort --check-only src/ test/

format:
	black src/ test/
	isort src/ test/

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .coverage
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# CI pipeline
ci: lint test
	@echo "✓ All CI checks passed!"

# Development workflow
dev-setup: dev-install setup-hooks
	@echo "Development environment ready!"
	@echo "Try: make test"

setup-hooks:
	@python scripts/auto-setup-hooks.py

# Local integration testing
test-local:
	@python -m pytest test/test_local_integration.py -v -s

# Homebrew testing
brew-test:
	brew install --build-from-source homebrew-formula/claude-code-automation.rb

# Release preparation
release-prep: clean format lint test
	@echo "Release preparation complete!"
	@echo "Ready for git commit and release."
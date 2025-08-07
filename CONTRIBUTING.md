# Contributing to Claude Code Session Automation

We love your input! We want to make contributing to Claude Code Session Automation as easy and transparent as possible.

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code follows the existing style.
6. Issue that pull request!

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/claude-code-automation.git
cd claude-code-automation

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .

# Test your changes
claude-code-automation help
```

## Testing

```bash
# Run the CLI tests
python -m pytest test/

# Test manual installation
python test/manual_test.py
```

## Code Style

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Add docstrings for all public functions
- Keep functions focused and small

## Issue Reporting

We use GitHub issues to track public bugs. Please ensure your description is
clear and has sufficient instructions to be able to reproduce the issue.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
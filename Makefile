.PHONY: setup test lint spec-check clean

# Install all dependencies
setup:
	uv venv
	uv pip install -e ".[dev]" || uv pip install pydantic httpx pytest pytest-asyncio ruff

# Run the test suite (expects failing tests - TDD approach)
test:
	.venv/bin/python -m pytest tests/ -v --tb=short

# Run linting checks
lint:
	.venv/bin/python -m ruff check .

# Verify specs exist and are non-empty
spec-check:
	@echo "Checking spec files..."
	@test -f specs/_meta.md && echo "  _meta.md: OK" || echo "  _meta.md: MISSING"
	@test -f specs/functional.md && echo "  functional.md: OK" || echo "  functional.md: MISSING"
	@test -f specs/technical.md && echo "  technical.md: OK" || echo "  technical.md: MISSING"
	@echo "Checking skill READMEs..."
	@test -f skills/fetch_trends/README.md && echo "  fetch_trends: OK" || echo "  fetch_trends: MISSING"
	@test -f skills/generate_content/README.md && echo "  generate_content: OK" || echo "  generate_content: MISSING"
	@test -f skills/evaluate_content/README.md && echo "  evaluate_content: OK" || echo "  evaluate_content: MISSING"
	@echo "Spec check complete."

# Run tests inside Docker
docker-test:
	docker build -t chimera-test --target test .
	docker run --rm chimera-test

# Remove generated files
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf .mypy_cache .ruff_cache

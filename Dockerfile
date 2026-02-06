# Multi-stage Dockerfile for Project Chimera
#
# Stage 1 (base): Install dependencies
# Stage 2 (test): Run tests and linting
#
# Usage:
#   docker build -t chimera-test --target test .
#   docker run --rm chimera-test

# --- Stage 1: Base image with dependencies ---
FROM python:3.12-slim AS base

WORKDIR /app

# Install uv for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency definition first (Docker caches this layer)
COPY pyproject.toml README.md ./

# Install dependencies
RUN uv pip install --system --no-cache -e ".[dev]" || \
    uv pip install --system --no-cache pydantic httpx pytest pytest-asyncio ruff

# Copy project code
COPY . .

# --- Stage 2: Test runner ---
FROM base AS test

# Default command: run tests
CMD ["python", "-m", "pytest", "tests/", "-v", "--tb=short"]

# Chimera Agentic Infrastructure

Infrastructure foundation for **Project Chimera** - an Autonomous Influencer Network.

## Overview

This repository contains the architectural foundation, specifications, and tooling required to build autonomous AI influencer agents. It follows Spec-Driven Development (SDD) principles.

## Structure

```
├── specs/          # Project specifications (the source of truth)
├── skills/         # Agent skill definitions
├── tests/          # Test suite (TDD approach)
├── research/       # Architecture decisions and research notes
├── .github/        # CI/CD workflows
└── CLAUDE.md       # AI assistant context rules
```

## Setup

```bash
# Create virtual environment
uv venv

# Install dependencies
uv pip install -e ".[dev]"

# Activate environment
source .venv/bin/activate
```

## Development

```bash
make setup    # Install dependencies
make test     # Run tests
make lint     # Run linting
```

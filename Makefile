verify-virtualenv:
	@if [ -z "${VIRTUAL_ENV}" ]; then \
		echo "Error: This command must be run inside a virtual environment."; \
		exit 1; \
	fi
.PHONY: verify-virtualenv

install-dependencies: verify-virtualenv
	uv sync
.PHONY: install-dependencies

install-dependencies-dev: install-dependencies
	uv sync --dev
.PHONY: install-dependencies-dev

install-pre-commit: verify-virtualenv
	@echo "Setting up pre-commit hooks..."
	uv run pre-commit install --install-hooks --hook-type pre-commit
	uv run pre-commit install --install-hooks --hook-type pre-push
	@echo "Pre-commit successfully installed and configured!"
.PHONY: install-pre-commit


# Test targets
test: test-python test-e2e
.PHONY: test

test-python:
	uv run pytest test/unit/
.PHONY: test-python

test-e2e:
	uv run pytest test/e2e/
.PHONY: test-e2e

t: test

TEST_ONLY_FILTER?="."

test-only:
	git status --porcelain | grep -E "${TEST_ONLY_FILTER}" | awk '{print $$2}' | xargs uv run pytest 
.PHONY: test-only

#alias
to: test-only

mypy:
	uv run mypy .
.PHONY: mypy


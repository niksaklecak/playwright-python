# Makefile for playwright-python project

.PHONY: test codegen codegen-no-auth

# Default target: run tests
test:
	pytest

# Run Codegen, assuming storage_state.json exists (run 'make test' first if needed)
codegen:
	playwright codegen https://qabuddy.ai/ --load-storage=tests/e2e/storage_state.json --viewport-size=1280,720 --lang=en-GB --timezone=Europe/Berlin --ignore-https-errors

# Run Codegen without attempting to load authentication state
codegen-no-auth:
	playwright codegen https://qabuddy.ai/ --viewport-size=1280,720 --lang=en-GB --timezone=Europe/Berlin --ignore-https-errors 
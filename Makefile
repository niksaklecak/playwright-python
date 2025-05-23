# Makefile for playwright-python project

.PHONY: test codegen-no-auth

# Default target: run tests
test:
	pytest

# Run tests headed
test-headed:
	pytest --headed

# Run Codegen without attempting to load authentication state
codegen-no-auth:
	playwright codegen https://app.weinfuse.com/ --viewport-size=1280,720 --lang=en-GB --timezone=Europe/Berlin --ignore-https-errors 

codegen-with-auth:
	playwright codegen https://app.weinfuse.com/ --viewport-size=1280,720 --lang=en-GB --timezone=Europe/Berlin --ignore-https-errors --load-state=./auth_state.json

.PHONY: lint fmt test docs clean package

VENV_NAME?=venv

default:
	@echo "Makefile for $(PACKAGE_NAME)"
	@echo
	@echo 'Usage:'
	@echo
	@echo '    make venv       setup virtual environment for development'
	@echo '    make lint       check lint output with black'
	@echo '    make fmt        auto format code with black'
	@echo '    make clean      cleanup all temporary files'
	@echo

venv: . $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: requirements-dev.txt
	pip install --upgrade pip virtualenv
	@test -d $(VENV_NAME) || python -m virtualenv --clear $(VENV_NAME)
	$(VENV_NAME)/bin/pip install -Ur requirements-dev.txt
	@touch $(VENV_NAME)/bin/activate

lint: venv
	${VENV_NAME}/bin/black . --check --diff

fmt: venv
	${VENV_NAME}/bin/black .

clean:
	@rm -rf $(VENV_NAME) build/ dist/ docs/build/
	find . -name \*.pyc -delete

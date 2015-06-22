NODE_ENV ?= development

VENV_PATH ?= venv

VENV_BIN = $(VENV_PATH)/bin
PYTHON = $(VENV_BIN)/python3


.PHONY: build install package lint test devserver


build: install test package

package:
	@NODE_ENV=production npm run build
	@$(PYTHON) setup.py sdist

install: venv node_modules

venv: requirements.txt
ifeq (,$(wildcard $(VENV_PATH)))
	@pyvenv $(VENV_PATH)
endif
	@$(VENV_BIN)/pip install -U -r $<

node_modules: package.json
	@npm install


lint:
	@$(VENV_BIN)/flake8 server/ --statistics
	@$(shell npm bin)/eslint client

test:
	@$(VENV_BIN)/nosetests gomoku/


devserver:
	$(PYTHON) -m gomoku --debug

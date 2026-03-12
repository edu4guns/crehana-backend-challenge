PYTHON ?= python
PIP ?= pip

.PHONY: install run test lint format docker-up docker-down

install:
	$(PIP) install -e .[dev]

run:
	$(PYTHON) -m uvicorn app.main:app --reload

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m flake8 app tests

format:
	$(PYTHON) -m isort app tests
	$(PYTHON) -m black app tests

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down


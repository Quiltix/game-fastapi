
PYTHON = .venv/bin/python
PIP = .venv/bin/pip
UVICORN = .venv/bin/uvicorn
ALEMBIC = .venv/bin/alembic

.PHONY: install run-app db-migrate db-upgrade help


default: help


install: .venv/bin/activate
	@echo "Installing dependencies from requirements.txt..."
	@$(PIP) install -r requirements.txt
	@echo "Dependencies installed."


.venv/bin/activate:
	@echo "Creating virtual environment..."
	@python3 -m venv .venv
	@echo "Virtual environment created at ./.venv/"

run-app:
	@echo "Starting application with Uvicorn..."
	@$(UVICORN) src.main:app --reload --host 0.0.0.0 --port 8000
	@echo "Application stopped."

# Создание новой миграции базы данных
db-migrate:
	@echo "Creating database migration..."
	@$(ALEMBIC) revision --autogenerate -m "$(msg)"
	@echo "Database migration created."

# Применение миграций к базе данных
db-upgrade:
	@echo "Upgrading database to the latest version..."
	@$(ALEMBIC) upgrade head
	@echo "Database upgraded."
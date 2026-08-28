VENV = .venv
PYTHON = $(VENV)/bin/python
PYTEST = $(VENV)/bin/pytest
UVICORN = $(VENV)/bin/uvicorn
ALEMBIC = $(VENV)/bin/alembic

.PHONY: help up down restart start dev test check migrate migration db-create db-reset logs clean

help:
	@echo ""
	@echo "Gestor Nutricional"
	@echo ""
	@echo "Comandos disponibles:"
	@echo ""
	@echo "  make start       Arranca el entorno completo"
	@echo "  make dev         Arranca FastAPI en modo desarrollo"
	@echo "  make test        Ejecuta todos los tests"
	@echo "  make check       Comprueba que todo funciona"
	@echo ""
	@echo "  make up          Levanta PostgreSQL"
	@echo "  make down        Detiene PostgreSQL"
	@echo "  make restart     Reinicia PostgreSQL"
	@echo ""
	@echo "  make migrate     Aplica las migraciones pendientes"
	@echo "  make migration   Crea una nueva migración"
	@echo "  make db-create   Crea las tablas directamente"
	@echo "  make db-reset    Reinicia la base de datos y aplica migraciones"
	@echo ""
	@echo "  make logs        Muestra los logs de Docker"
	@echo "  make clean       Elimina contenedores y volumen"
	@echo ""

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose down
	docker compose up -d

migrate: up
	$(ALEMBIC) upgrade head

migration:
	@read -p "Nombre de la migración: " name; \
	$(ALEMBIC) revision --autogenerate -m "$$name"

start: up migrate
	$(UVICORN) app.main:app

dev: up migrate
	$(UVICORN) app.main:app --reload

test: up
	$(PYTEST)

check: up
	$(PYTEST)
	$(ALEMBIC) check

db-create: up
	$(PYTHON) -c "from app.db.database import create_tables; create_tables()"

db-reset:
	docker compose down -v
	docker compose up -d
	$(ALEMBIC) upgrade head

logs:
	docker compose logs -f

clean:
	docker compose down -v

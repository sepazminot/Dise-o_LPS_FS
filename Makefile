# === Educational DevOps - Makefile ===
# Uso: make <target>
# Ver targets: make help

.PHONY: help up down logs test lint proto contract health db-migrate db-seed clean

# Colores
GREEN  := \033[0;32m
YELLOW := \033[1;33m
RED    := \033[0;31m
NC     := \033[0m

help:
	@echo "$(GREEN)Educational DevOps - Comandos disponibles$(NC)"
	@echo ""
	@echo "  $(YELLOW)Desarrollo Local$(NC)"
	@echo "    make up           - Levantar stack completo (Docker Compose)"
	@echo "    make down         - Bajar stack"
	@echo "    make logs         - Ver logs agregados (-f para follow)"
	@echo "    make health       - Verificar health checks de todos los servicios"
	@echo ""
	@echo "  $(YELLOW)Testing & Calidad$(NC)"
	@echo "    make test         - Ejecutar tests backend + frontend"
	@echo "    make test-backend - Tests solo backend (pytest)"
	@echo "    make test-frontend - Tests solo frontend (Pest + Playwright)"
	@echo "    make lint         - Lint + type-check (ruff, mypy, pint, phpstan)"
	@echo "    make proto        - Generar código desde .proto (buf generate)"
	@echo "    make proto-lint   - Validar .proto (buf lint)"
	@echo "    make contract     - Contract tests (Pact)"
	@echo ""
	@echo "  $(YELLOW)Base de Datos$(NC)"
	@echo "    make db-migrate   - Ejecutar migraciones (Alembic + Laravel)"
	@echo "    make db-seed      - Cargar seeds de desarrollo"
	@echo "    make db-reset     - Reset DB + migraciones + seeds"
	@echo ""
	@echo "  $(YELLOW)Utilidades$(NC)"
	@echo "    make clean        - Limpiar artefactos build/cache"
	@echo "    make deps         - Instalar dependencias (poetry, composer, pnpm)"

# === Docker Compose ===
COMPOSE_FILE := infra/docker/docker-compose.yml
COMPOSE := docker compose -f $(COMPOSE_FILE)

up:
	@echo "$(GREEN)Levantando stack local...$(NC)"
	$(COMPOSE) up -d --build
	@echo "$(GREEN)Stack levantado. Verificando salud...$(NC)"
	@sleep 5
	@$(MAKE) health

down:
	@echo "$(YELLOW)Bajando stack...$(NC)"
	$(COMPOSE) down -v

logs:
	$(COMPOSE) logs -f

health:
	@echo "$(GREEN)Verificando health checks...$(NC)"
	@curl -sf http://localhost:8000/health/live >/dev/null && echo "  ✅ Backend (8000)" || echo "  ❌ Backend (8000)"
	@curl -sf http://localhost:8080/health/live >/dev/null && echo "  ✅ Frontend (8080)" || echo "  ❌ Frontend (8080)"
	@curl -sf http://localhost:9090/-/healthy >/dev/null && echo "  ✅ Prometheus (9090)" || echo "  ❌ Prometheus (9090)"
	@curl -sf http://localhost:3000/api/health >/dev/null && echo "  ✅ Grafana (3000)" || echo "  ❌ Grafana (3000)"

# === Testing ===
test: test-backend test-frontend

test-backend:
	@echo "$(GREEN)Tests Backend...$(NC)"
	cd backend && poetry run pytest -xvs --cov=app --cov-report=term-missing

test-frontend:
	@echo "$(GREEN)Tests Frontend...$(NC)"
	cd frontend && ./vendor/bin/pest --parallel --coverage --min=70

# === Linting ===
lint: lint-backend lint-frontend

lint-backend:
	@echo "$(GREEN)Lint Backend...$(NC)"
	cd backend && poetry run ruff check . && poetry run mypy app/

lint-frontend:
	@echo "$(GREEN)Lint Frontend...$(NC)"
	cd frontend && ./vendor/bin/pint --test && ./vendor/bin/phpstan analyse --memory-limit=512M

# === Protobuf ===
proto:
	@echo "$(GREEN)Generando código desde .proto...$(NC)"
	buf generate

proto-lint:
	@echo "$(GREEN)Validando .proto...$(NC)"
	buf lint

# === Contract Tests ===
contract:
	@echo "$(GREEN)Contract Tests (Pact)...$(NC)"
	# TODO: Implementar cuando exista Pact Broker
	@echo "  ℹ️  Pendiente: configurar Pact Broker y provider verification"

# === Database ===
db-migrate:
	@echo "$(GREEN)Ejecutando migraciones...$(NC)"
	cd backend && poetry run alembic upgrade head
	cd frontend && php artisan migrate --force

db-seed:
	@echo "$(GREEN)Cargando seeds...$(NC)"
	cd backend && poetry run python -m scripts.seed
	cd frontend && php artisan db:seed --force

db-reset:
	@echo "$(RED)Reset completo DB...$(NC)"
	$(COMPOSE) restart postgres
	@sleep 3
	$(MAKE) db-migrate
	$(MAKE) db-seed

# === Dependencies ===
deps:
	@echo "$(GREEN)Instalando dependencias...$(NC)"
	cd backend && poetry install
	cd frontend && composer install
	cd frontend && pnpm install

# === Clean ===
clean:
	@echo "$(YELLOW)Limpiando artefactos...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "vendor" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	@echo "$(GREEN)Limpieza completada$(NC)"

# Educational DevOps - Producto Educativo MVP

> **Grupo 6** | Sprint 1-3 | Stack: FastAPI/gRPC + Laravel 11/Octane + PostgreSQL 15 + Kubernetes + GitHub Actions

## 🏗️ Arquitectura General

```
┌─────────────────┐     gRPC/REST      ┌──────────────────┐
│   Frontend      │ ◄─────────────────► │    Backend       │
│  (Laravel 11)   │   Protobuf v1      │   (FastAPI)      │
│   + Octane      │                    │  Clean Arch      │
└────────┬────────┘                    └────────┬─────────┘
         │                                      │
         ▼                                      ▼
┌─────────────────┐                    ┌──────────────────┐
│   API Gateway   │                    │  PostgreSQL 15   │
│    (Kong)       │                    │  + Redis 7       │
│   Sprint 2+     │                    │                  │
└─────────────────┘                    └──────────────────┘
         │
         ▼
┌─────────────────┐
│  Observability  │
│ Prometheus +    │
│ Grafana +       │
│ AlertManager    │
└─────────────────┘
```

## 🚀 Quick Start (Desarrollo Local)

```bash
# 1. Clonar e iniciar
git clone https://github.com/Grupo6/educational-devops.git
cd educational-devops

# 2. Levantar stack completo (PostgreSQL, Redis, Backend, Frontend, Prometheus, Grafana)
make up
# o: docker compose -f infra/docker/docker-compose.yml up -d

# 3. Verificar salud
make health
# Backend:  http://localhost:8000/health/live
# Frontend: http://localhost:8080/health/live
# Grafana:  http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9090
```

## 📦 Stack por Sprint

| Componente | Sprint 1 | Sprint 2 | Sprint 3 |
|------------|----------|----------|----------|
| **Auth (JWT RS256)** | ✅ Core | ✅ | ✅ |
| **Health/Readiness** | ✅ Core | ✅ | ✅ |
| **Domain gRPC (Student/Course/Grade)** | ✅ Core | ✅ | ✅ |
| **Infra Base (Docker, K8s, CI/CD)** | ✅ | ✅ | ✅ |
| **CRUD Académico UI** | | ✅ Core | ✅ |
| **API Gateway (Kong)** | | ✅ Core | ✅ |
| **Contract Tests (Pact)** | | ✅ Core | ✅ |
| **Reportes PDF/Excel** | | ✅ Core | ✅ |
| **Multi-tenancy (RLS)** | | | ✅ Core |
| **Notificaciones (Email/Push/WS)** | | | ✅ Core |
| **Performance (k6)** | | | ✅ Core |
| **Release Candidate + Docs** | | | ✅ Core |

## 🛠️ Comandos Principales (Makefile)

```bash
make up           # Levantar stack local completo
make down         # Bajar stack
make logs         # Ver logs agregados
make test         # Tests backend + frontend
make lint         # Lint + type-check
make proto        # Generar código desde .proto
make contract     # Contract tests (Pact)
make db-migrate   # Ejecutar migraciones
make db-seed      # Cargar seeds
make health       # Verificar health checks
```

## 📁 Estructura del Monorepo

```
educational-devops/
├── backend/                 # FastAPI Clean Architecture
│   ├── app/
│   │   ├── domain/          # Entidades, VOs, Eventos, Excepciones
│   │   ├── application/     # Casos de uso, DTOs, Puertos
│   │   ├── infrastructure/  # Adaptadores: DB, gRPC, Auth, Cache
│   │   └── interfaces/      # gRPC Services, REST Controllers
│   ├── tests/
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/                # Laravel 11 Modular
│   ├── app/Modules/
│   │   ├── Auth/
│   │   └── Academic/
│   ├── tests/ (Pest + Playwright)
│   ├── composer.json
│   └── Dockerfile
├── contracts/               # .proto compartidos (buf)
│   ├── auth.proto
│   ├── student.proto
│   ├── course.proto
│   └── grade.proto
├── infra/
│   ├── docker/
│   │   └── docker-compose.yml
│   ├── k8s/
│   │   ├── base/
│   │   └── overlays/{dev,staging}
│   └── monitoring/
│       ├── prometheus/
│       └── grafana/dashboards/
├── docs/
├── .github/workflows/
└── Makefile
```

## 🔧 Prerequisitos

- Python 3.11+ (Poetry/uv)
- Node.js 20+ (pnpm)
- PHP 8.3+ (Composer)
- Go 1.22+ (buf, protoc plugins)
- Docker Desktop / Colima
- kubectl, helm, k3d
- protoc, buf
- Terraform, Ansible (Sprint 2+)
- GitHub CLI (`gh`)

## 📋 Sprint Goals

- **Sprint 1 (17/06–01/07)**: Fundamentos DevOps + Core Assets (Auth + Health + Dominio) + Infra Base
- **Sprint 2 (02/07–15/07)**: CRUD Académico + API Gateway + Contract Tests + Reportes MVP
- **Sprint 3 (16/07–29/07)**: MVP Release - Módulo Avanzado + Multi-tenancy + Notificaciones + Performance + RC

## 📄 Licencia

MIT - Proyecto académico Grupo 6

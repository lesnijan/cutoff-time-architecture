# Cutoff Time API

Dynamic warehouse capacity and cutoff time calculation system for SAP S/4HANA environments.

## 📋 Overview

This API provides real-time capacity checks and dynamic cutoff time calculations for warehouse operations. Based on current workload, available resources, and order characteristics, it determines whether orders can be shipped same-day.

**Key Features:**
- Real-time capacity checking (< 500ms response time)
- Dynamic cutoff time calculation
- VIP priority handling
- What-if simulation
- Prometheus metrics
- Structured logging
- Redis caching

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌────────────┐
│   Client    │────▶│  FastAPI     │────▶│  SAP HANA  │
│  (Fiori)    │     │  Cutoff API  │     │  CDS Views │
└─────────────┘     └──────────────┘     └────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  Redis Cache │
                    └──────────────┘
```

See [docs/02-architecture.md](../docs/02-architecture.md) for detailed architecture.

## 🎮 Try the Demo (No Setup Required!)

**Want to see it in action immediately?**

```bash
poetry install
poetry run uvicorn app.main:app --reload --port 8080
```

Then open: **http://localhost:8080/static/demo.html**

✅ **Works out of the box** - No HANA, no Redis, no configuration!
📊 **Interactive dashboard** with 4 demo scenarios
🧪 **Test all API endpoints** visually

See [DEMO.md](DEMO.md) for complete demo guide.

---

## 🚀 Quick Start (Full Setup)

### Prerequisites

- Python 3.11+
- Poetry
- SAP HANA access (optional for demo)
- Redis (optional for demo)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd cutoff-api
```

2. Install dependencies:
```bash
poetry install
```

3. Copy environment configuration:
```bash
cp .env.example .env
```

4. Configure `.env` with your settings:
```bash
# Edit HANA connection settings
HANA_HOST=your-hana-host
HANA_USER=your-username
HANA_PASSWORD=your-password
```

5. Run the application:
```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8080`

## 🐳 Docker

### Build and run with Docker Compose:

```bash
docker-compose up --build
```

Services started:
- API: `http://localhost:8080`
- Redis: `localhost:6379`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`

### Build Docker image:

```bash
docker build -t cutoff-api:latest .
```

## 📚 API Documentation

### Interactive Documentation

Once running, access the interactive API docs:
- **Swagger UI**: http://localhost:8080/api/v1/docs
- **ReDoc**: http://localhost:8080/api/v1/redoc

### Main Endpoints

#### POST /api/v1/capacity/check
Check if an order can ship today.

**Request:**
```json
{
  "order_id": "SO-2024-001234",
  "customer_id": "CUST-5678",
  "priority": "STANDARD",
  "warehouse_id": "WH-MAIN",
  "items": [
    {"product_id": "MAT-001", "quantity": 10},
    {"product_id": "MAT-002", "quantity": 5}
  ]
}
```

**Response:**
```json
{
  "can_ship_today": true,
  "confidence": 0.92,
  "estimated_completion": "2024-01-15T15:30:00Z",
  "current_utilization": 0.72,
  "message": "Wysyłka dziś możliwa ✓",
  "decision_factors": {
    "workload_impact": 12.5,
    "remaining_capacity": 45.2,
    "time_buffer_minutes": 30,
    "bottleneck_resource": "PACKERS"
  },
  "metadata": {
    "calculated_at": "2024-01-15T12:00:00Z",
    "cache_hit": false,
    "calculation_time_ms": 45
  }
}
```

#### GET /api/v1/cutoff/current
Get current dynamic cutoff time.

**Response:**
```json
{
  "cutoff_time": "2024-01-15T14:30:00Z",
  "hard_deadline": "2024-01-15T16:00:00Z",
  "current_utilization": 0.78,
  "status": "WARNING",
  "time_remaining_minutes": 150
}
```

#### GET /api/v1/status
Get comprehensive warehouse status.

#### POST /api/v1/simulate
Simulate capacity impact (what-if analysis).

#### GET /api/v1/health
Health check (no authentication required).

## 🧪 Testing

### Run all tests:
```bash
poetry run pytest
```

### Run with coverage:
```bash
poetry run pytest --cov=app --cov-report=html
```

### Run specific test file:
```bash
poetry run pytest tests/unit/test_decision_engine.py -v
```

## 🔧 Development

### Setup pre-commit hooks:
```bash
poetry run pre-commit install
```

### Code formatting:
```bash
poetry run black app tests
```

### Linting:
```bash
poetry run ruff check app tests
```

### Type checking:
```bash
poetry run mypy app
```

## 📊 Monitoring

### Prometheus Metrics

Metrics available at `/metrics`:

- `cutoff_api_requests_total` - Total HTTP requests
- `cutoff_api_request_duration_seconds` - Request latency
- `cutoff_capacity_checks_total` - Capacity check decisions
- `cutoff_warehouse_utilization` - Current utilization
- `cutoff_cache_hits_total` / `cutoff_cache_misses_total` - Cache performance

### Grafana Dashboard

Import dashboard from `monitoring/grafana-dashboards/cutoff-api.json`

## 🔐 Authentication

API uses JWT tokens with OAuth 2.0 Bearer scheme.

Required scopes:
- `cutoff.read` - Read operations (GET endpoints)
- `cutoff.write` - Write operations (POST /capacity/check)
- `cutoff.admin` - Admin operations (POST /simulate)

**Example:**
```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  http://localhost:8080/api/v1/cutoff/current
```

## ⚙️ Configuration

All configuration via environment variables (see `.env.example`):

### Key Settings

| Variable | Default | Description |
|----------|---------|-------------|
| `MAX_UTILIZATION` | 0.85 | Maximum utilization threshold |
| `SAFETY_BUFFER_MINUTES` | 30 | Safety buffer before deadline |
| `VIP_RESERVE_PERCENT` | 0.10 | VIP capacity reserve (10%) |
| `CONGESTION_ALPHA` | 1.2 | Congestion factor coefficient |
| `REDIS_TTL` | 60 | Cache TTL in seconds |

## 🚀 Deployment to SAP BTP

### Cloud Foundry Deployment

1. Login to Cloud Foundry:
```bash
cf login -a https://api.cf.eu10.hana.ondemand.com
```

2. Push application:
```bash
cf push
```

The `manifest.yml` contains deployment configuration.

### Required Services

Create services in BTP:
```bash
cf create-service hana hdi-shared cutoff-hana
cf create-service redis cache-small cutoff-redis
cf create-service xsuaa application cutoff-xsuaa
```

## 📖 Documentation

- [Executive Summary](../docs/01-executive-summary.md)
- [Architecture](../docs/02-architecture.md)
- [Algorithm Specification](../docs/03-algorithm.md)
- [Data Model](../docs/04-data-model.md)
- [API Specification](../docs/05-api-specification.md)
- [Implementation Plan](../docs/06-implementation-plan.md)

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes and commit: `git commit -am 'Add new feature'`
3. Push to branch: `git push origin feature/my-feature`
4. Create Pull Request

## 📝 License

Copyright © 2024 LR Systems

## 🆘 Support

For issues and questions:
- Create an issue in the repository
- Contact: support@lrsystems.pl

---

**Version:** 1.0.0
**Status:** PoC Implementation
**Last Updated:** 2024-01-15

# 🎮 Cutoff Time API - Demo Guide

## 🚀 Quick Start (5 Minutes)

### 1. Install Dependencies

```bash
cd cutoff-time-architecture/cutoff-api
poetry install
```

### 2. Run the Demo

```bash
# No configuration needed! Works out of the box
poetry run uvicorn app.main:app --reload --port 8080
```

### 3. Open Demo Dashboard

Open your browser: **http://localhost:8080/static/demo.html**

---

## 🎯 What's Included in the Demo

### ✅ Fully Working Features

1. **Real-time Capacity Checks** - Test different order scenarios
2. **Dynamic Cutoff Time Calculation** - See cutoff time adjust based on load
3. **4 Demo Scenarios** - Switch between different warehouse states
4. **Interactive Dashboard** - Visual representation of warehouse status
5. **Complete API** - All 5 endpoints fully functional

### 📊 Demo Scenarios

| Scenario | Description | Utilization | Status |
|----------|-------------|-------------|--------|
| **Normal** | Standard operations | 70% | WARNING |
| **Low** | Light workload | 30% | ACCEPTING |
| **High** | Heavy workload | 90% | CRITICAL |
| **Overload** | At maximum capacity | 97.5% | CLOSED |

---

## 🎬 Demo Walkthrough

### Scenario 1: Normal Operations

1. Open demo dashboard: http://localhost:8080/static/demo.html
2. You'll see:
   - Current utilization: ~70%
   - Status: WARNING (yellow)
   - Orders in queue: 47
   - Cutoff time calculated dynamically

### Scenario 2: Test Capacity Check

1. Select product: **MAT-002 (Heavy Equipment)**
2. Set quantity: **50**
3. Priority: **STANDARD**
4. Click "Check Capacity"
5. **Result**: ❌ Order rejected (would exceed capacity)

### Scenario 3: VIP Override

1. Same order as above
2. Change priority to: **VIP**
3. Click "Check Capacity"
4. **Result**: ✓ Order accepted (VIP reserve used)

### Scenario 4: Switch to Low Utilization

1. Click "Low Utilization" button
2. Watch metrics update automatically
3. Try the same heavy order again
4. **Result**: ✓ Order accepted (plenty of capacity)

### Scenario 5: Overload State

1. Click "Overloaded" button
2. Utilization jumps to 97.5%
3. Status changes to CLOSED (red)
4. Try any order
5. **Result**: ❌ All orders rejected

---

## 🧪 Testing Different Products

Each product has different characteristics:

### MAT-001: Standard Box (Small)
- Weight factor: 1.0
- Location factor: 1.0
- **Use case**: Baseline testing

### MAT-002: Heavy Equipment
- Weight factor: 2.5
- Location factor: 1.5
- **Use case**: High workload testing

### MAT-003: High Shelf Item
- Weight factor: 1.0
- Location factor: 1.8
- **Use case**: Complex picking testing

### MAT-004: Bulk Material
- Weight factor: 3.0
- Location factor: 1.0
- **Use case**: Maximum workload testing

### MAT-005: Lightweight Package
- Weight factor: 0.5
- Location factor: 1.0
- **Use case**: Low workload testing

---

## 📡 API Endpoints Demo

### 1. Health Check
```bash
curl http://localhost:8080/api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "checks": {
    "hana": "ok",
    "redis": "ok",
    "api": "ok"
  }
}
```

### 2. Capacity Check
```bash
curl -X POST http://localhost:8080/api/v1/capacity/check \
  -H "Content-Type: application/json" \
  -d '{
    "priority": "STANDARD",
    "warehouse_id": "WH-MAIN",
    "items": [
      {"product_id": "MAT-001", "quantity": 10}
    ]
  }'
```

**Response:**
```json
{
  "can_ship_today": true,
  "confidence": 0.92,
  "current_utilization": 0.72,
  "message": "Wysyłka dziś możliwa ✓",
  "decision_factors": {
    "workload_impact": 12.5,
    "remaining_capacity": 45.2,
    "bottleneck_resource": "PACKER"
  }
}
```

### 3. Current Cutoff Time
```bash
curl http://localhost:8080/api/v1/cutoff/current
```

### 4. Warehouse Status (Full Dashboard Data)
```bash
curl http://localhost:8080/api/v1/status
```

### 5. What-If Simulation
```bash
curl -X POST http://localhost:8080/api/v1/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "scenario_name": "Flash Sale",
    "orders": [
      {"product_id": "MAT-001", "quantity": 100}
    ],
    "time_horizon_minutes": 60
  }'
```

### 6. Switch Demo Scenario
```bash
curl -X POST http://localhost:8080/api/v1/demo/scenario/high
```

---

## 🎨 Demo Dashboard Features

### Real-Time Updates
- Dashboard auto-refreshes every 30 seconds
- Instant updates after scenario changes
- Live utilization progress bar

### Interactive Elements
- Click scenario buttons to switch states
- Test different products and quantities
- View detailed JSON responses

### Visual Indicators
- **Green** (ACCEPTING): < 70% utilization
- **Yellow** (WARNING): 70-85% utilization
- **Orange** (CRITICAL): 85-95% utilization
- **Red** (CLOSED): > 95% utilization

---

## 🔍 Behind the Scenes

### Mock Data Architecture

The demo uses **realistic mock data** that simulates HANA responses:

```python
# Mock warehouse with realistic resources
"WH-MAIN": {
    "pickers": 8,
    "packers": 5,  # Bottleneck!
    "loaders": 3,
}

# Mock scenario states
"normal": {
    "current_workload": 280.5 minutes,
    "total_capacity": 400.0 minutes,
    "utilization": 70.1%,
}
```

### Decision Engine Logic

```
1. Calculate order workload: W = Σ(qty × weight × location) + overhead
2. Get current warehouse state from "HANA"
3. Check utilization: U = (Current + New) / Capacity
4. Apply thresholds:
   - U < 85% → Accept
   - U ≥ 85% → Reject (unless VIP)
5. Calculate confidence score
6. Return decision with factors
```

---

## 📊 Demo Metrics

The demo tracks:
- **API Response Time**: < 50ms (cached) or < 200ms (computed)
- **Cache Hit Rate**: Visible in logs
- **Decision Count**: Tracked per scenario
- **Utilization Trends**: Shown in dashboard

---

## 🎓 Learning Scenarios

### 1. Understanding Capacity Thresholds
- Switch to "Low" → Try adding orders → See when it switches to "Warning"
- Observe the 70% threshold trigger

### 2. VIP Priority System
- Fill warehouse to 90% (High scenario)
- Try STANDARD order → Rejected
- Try VIP order → Accepted (uses 10% reserve)

### 3. Congestion Factor
- At low utilization: Processing time is linear
- At high utilization: Processing time grows exponentially
- Compare estimated completion times

### 4. Product Characteristics
- Order 10x MAT-001 (light) → Low impact
- Order 10x MAT-004 (bulk) → High impact
- See workload difference in response

---

## 🚀 Next Steps After Demo

### For Development:
1. **Connect Real HANA**: Replace mock repository with actual queries
2. **Add Authentication**: Uncomment auth in endpoints
3. **Deploy to QAS**: Use manifest.yml for SAP BTP

### For Testing:
1. **Unit Tests**: `poetry run pytest`
2. **Load Testing**: Use Locust (see tests/performance/)
3. **Integration Tests**: Connect to test HANA instance

### For Production:
1. **Create CDS Views**: See [docs/04-data-model.md](../docs/04-data-model.md)
2. **Configure Monitoring**: Grafana dashboards
3. **Setup Alerts**: Based on utilization thresholds

---

## 🐛 Troubleshooting

### Demo doesn't start?
```bash
# Check Poetry is installed
poetry --version

# Reinstall dependencies
poetry install --no-cache

# Try with Python directly
python -m app.main
```

### Dashboard not loading?
- Check console for errors (F12)
- Verify API is running: http://localhost:8080/api/v1/health
- Try clearing browser cache

### API errors?
- Check logs in terminal
- Most errors are intentional (for demo purposes)
- Try switching to "normal" scenario

---

## 📝 Demo Checklist

Use this for presentations:

- [ ] Start API server
- [ ] Open demo dashboard
- [ ] Show "Normal" scenario
- [ ] Test capacity check with standard order
- [ ] Switch to "High" scenario
- [ ] Demonstrate order rejection
- [ ] Show VIP override
- [ ] Switch to "Low" scenario
- [ ] Show simulation endpoint
- [ ] Open API docs (Swagger UI)

---

## 🎯 Key Demo Talking Points

1. **Real-Time Decision Making**: Sub-second response times
2. **Business Rules**: Utilization thresholds, VIP handling
3. **Transparency**: All factors visible in response
4. **Scalability**: Designed for high-volume operations
5. **Integration**: Ready for SAP S/4HANA + BTP

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8080/api/v1/docs
- **Algorithm Specification**: [docs/03-algorithm.md](../docs/03-algorithm.md)
- **Architecture**: [docs/02-architecture.md](../docs/02-architecture.md)
- **Implementation Plan**: [docs/06-implementation-plan.md](../docs/06-implementation-plan.md)

---

**Demo Version**: 1.0.0
**Last Updated**: 2024-12-02
**Status**: ✅ Fully Functional

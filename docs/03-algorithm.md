# 🧮 Algorithm Specification

> Decision Logic & Mathematical Model

[← Architecture](02-architecture.md) | [Next: Data Model →](04-data-model.md)

---

## 📋 Algorithm Overview

System podejmuje decyzję w 3 krokach:

1. **OBLICZ** pracochłonność zlecenia
2. **PORÓWNAJ** z dostępną przepustowością
3. **ZDECYDUJ** czy wysyłka dziś jest możliwa

---

## 🔀 Decision Flowchart

```mermaid
flowchart TD
    START([🆕 Nowe Zlecenie]) --> CALC_WORK["Oblicz pracochłonność<br/>zlecenia W_new"]
    
    CALC_WORK --> GET_STATE["Pobierz aktualny stan:<br/>• Obciążenie W_current<br/>• Capacity C<br/>• Czas do deadline"]
    
    GET_STATE --> CALC_UTIL["Oblicz Utilization:<br/>U = (W_current + W_new) / C"]
    
    CALC_UTIL --> CHECK_UTIL{"U < 85%?"}
    
    CHECK_UTIL -->|"TAK ✓"| CALC_TIME["Oblicz czas ukończenia<br/>T_completion"]
    CHECK_UTIL -->|"NIE ✗"| CHECK_VIP{"Zlecenie VIP?"}
    
    CALC_TIME --> CHECK_TIME{"T_completion<br/>< Deadline?"}
    
    CHECK_TIME -->|"TAK ✓"| APPROVE["✅ WYSYŁKA DZIŚ<br/>Confidence: 92%"]
    CHECK_TIME -->|"NIE ✗"| REJECT["❌ WYSYŁKA JUTRO<br/>Reason: TIME_EXCEEDED"]
    
    CHECK_VIP -->|"TAK"| CHECK_VIP_CAP{"Rezerwa VIP<br/>dostępna?"}
    CHECK_VIP -->|"NIE"| REJECT2["❌ WYSYŁKA JUTRO<br/>Reason: CAPACITY_EXCEEDED"]
    
    CHECK_VIP_CAP -->|"TAK ✓"| APPROVE_VIP["✅ WYSYŁKA DZIŚ<br/>VIP Priority"]
    CHECK_VIP_CAP -->|"NIE ✗"| REJECT3["❌ WYSYŁKA JUTRO<br/>VIP capacity exhausted"]
    
    APPROVE --> LOG["📝 Log Decision"]
    APPROVE_VIP --> LOG
    REJECT --> LOG
    REJECT2 --> LOG
    REJECT3 --> LOG
    
    LOG --> RESPOND([📤 Return Response])
    
    style APPROVE fill:#22c55e,stroke:#16a34a,stroke-width:2px
    style APPROVE_VIP fill:#22c55e,stroke:#16a34a,stroke-width:2px
    style REJECT fill:#ef4444,stroke:#dc2626,stroke-width:2px
    style REJECT2 fill:#ef4444,stroke:#dc2626,stroke-width:2px
    style REJECT3 fill:#ef4444,stroke:#dc2626,stroke-width:2px
    style CHECK_UTIL fill:#f59e0b,stroke:#d97706,stroke-width:2px
    style CHECK_TIME fill:#f59e0b,stroke:#d97706,stroke-width:2px
```

---

## 📐 Mathematical Model

### Core Equations

#### 1. Order Workload (Pracochłonność zlecenia)

```
W_order = Σ(quantity × weight_factor × location_factor) + S + P + L
```

Gdzie:
- `quantity` - ilość produktu
- `weight_factor` - współczynnik pracochłonności produktu (1.0 - 3.0)
- `location_factor` - współczynnik lokalizacji (1.0 = standard, 1.8 = wysoki regał)
- `S` - setup time (stały, ~2 min)
- `P` - packing time (3 min + 0.5 min/item)
- `L` - loading time (~1.5 min)

#### 2. Total Workload (Całkowite obciążenie)

```
WORKLOAD(t) = Σ W_i × progress_factor_i
```

Gdzie `progress_factor`:
| Status | Factor | Opis |
|--------|--------|------|
| NEW | 1.00 | Nierozpoczęte |
| ALLOCATED | 0.95 | Zarezerwowane |
| PICKING | 0.60 | W trakcie kompletacji |
| PACKING | 0.25 | Do pakowania |
| LOADING | 0.08 | Do załadunku |
| SHIPPED | 0.00 | Wysłane |

#### 3. Capacity (Przepustowość)

```
CAPACITY(t) = MIN(picker_cap, packer_cap, loader_cap) × efficiency(t) × (1 - VIP_reserve)
```

Gdzie:
- `picker_cap = pickers × 1.2 units/min`
- `packer_cap = packers × 0.8 units/min`
- `loader_cap = loaders × 2.0 units/min`
- `efficiency(t)` - współczynnik wydajności (zmienny w ciągu dnia)
- `VIP_reserve = 0.10` (10% rezerwacji dla VIP)

#### 4. Time Efficiency Profile

```mermaid
xychart-beta
    title "Efficiency Profile (Daily)"
    x-axis ["06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00"]
    y-axis "Efficiency %" 0 --> 100
    line [70, 100, 98, 75, 92, 82, 65]
```

| Godzina | Efficiency | Powód |
|---------|------------|-------|
| 06:00 | 70% | Rozruch zmiany |
| 08:00 | 100% | Pełna wydajność |
| 12:00 | 75% | Przerwa obiadowa |
| 14:00 | 92% | Po przerwie |
| 16:00 | 82% | Zmęczenie |
| 18:00 | 65% | Koniec zmiany |

#### 5. Utilization

```
UTILIZATION = WORKLOAD / CAPACITY
```

**Krytyczne progi:**
- `< 70%` - ACCEPTING (zielony)
- `70-85%` - WARNING (żółty)
- `85-95%` - CRITICAL (pomarańczowy)
- `> 95%` - CLOSED (czerwony)

#### 6. Congestion Factor (Teoria Kolejek)

```
CONGESTION_FACTOR = 1 + α × UTILIZATION²
```

Gdzie `α = 1.2` (współczynnik empiryczny)

**Wyjaśnienie:** Przy wysokim wykorzystaniu czas obsługi rośnie nieliniowo z powodu:
- Kolizji pickerów w alejkach
- Kolejek przy stanowiskach pakowania
- Efektu zmęczenia

#### 7. Processing Time

```
PROC_TIME = (WORKLOAD / CAPACITY) × CONGESTION_FACTOR
```

#### 8. Decision Rule

```
IF (UTILIZATION < 0.85) AND (current_time + PROC_TIME < deadline - buffer)
THEN → "Ship Today" ✓
ELSE → "Ship Tomorrow" ✗
```

---

## 🔄 State Machine

System operacyjny magazynu przechodzi przez stany:

```mermaid
stateDiagram-v2
    [*] --> OPENING: 06:00 Start
    
    OPENING --> ACCEPTING: Resources ready
    
    ACCEPTING --> WARNING: Utilization > 70%
    WARNING --> ACCEPTING: Utilization < 65%
    
    WARNING --> CRITICAL: Utilization > 85%
    CRITICAL --> WARNING: Utilization < 80%
    
    CRITICAL --> CUTOFF_IMMINENT: < 30 min to deadline
    CUTOFF_IMMINENT --> CLOSED: Cutoff reached
    
    ACCEPTING --> CLOSED: Hard deadline
    WARNING --> CLOSED: Hard deadline
    
    CLOSED --> [*]: End of day
    
    note right of ACCEPTING
        ✅ Przyjmujemy zlecenia
        Alert: NONE
    end note
    
    note right of WARNING
        ⚠️ Ograniczona pojemność
        Alert: SLACK
    end note
    
    note right of CRITICAL
        🔴 Prawie pełne
        Alert: PAGERDUTY
    end note
```

### State Descriptions

| State | Utilization | Actions | Alerts |
|-------|-------------|---------|--------|
| **ACCEPTING** | < 70% | All orders accepted | None |
| **WARNING** | 70-85% | Monitor closely | Slack notification |
| **CRITICAL** | 85-95% | VIP only | PagerDuty alert |
| **CUTOFF_IMMINENT** | Any, < 30min | Prepare closure | Email to sales |
| **CLOSED** | N/A | Reject all | Dashboard update |

---

## 🎲 Edge Cases

### Case 1: "Whale Order" (Mega-zlecenie)

```mermaid
flowchart LR
    ORDER["Order: 500 items"] --> CHECK{"Workload > 20%<br/>of daily capacity?"}
    CHECK -->|"YES"| SPLIT["Split into<br/>sub-orders"]
    CHECK -->|"NO"| PROCESS["Process normally"]
    SPLIT --> ALERT["Alert manager"]
```

**Handling:** Orders exceeding 20% of daily capacity are flagged for manual review or automatic splitting.

### Case 2: "Flash Flood" (Nagły zalew)

```mermaid
flowchart LR
    RATE["Order rate<br/>> 50/5min"] --> PREDICT["Predict capacity<br/>exhaustion"]
    PREDICT --> ALERT["Proactive alert<br/>to sales team"]
    ALERT --> BUFFER["Increase safety<br/>buffer temporarily"]
```

**Handling:** Rate limiting and predictive alerting when order velocity spikes.

### Case 3: "Race Condition" (Równoczesne zapytania)

```mermaid
sequenceDiagram
    participant A as Sales Rep A
    participant B as Sales Rep B
    participant API as Cutoff API
    participant LOCK as Redis Lock
    
    A->>API: Check capacity
    B->>API: Check capacity
    API->>LOCK: Acquire lock (5s TTL)
    LOCK-->>API: Lock acquired (A)
    API-->>A: Capacity: YES (soft reserve)
    Note over LOCK: Lock held by A
    API->>LOCK: Wait for lock
    Note over A: A submits order
    A->>API: Submit order
    API->>LOCK: Release lock
    LOCK-->>API: Lock acquired (B)
    API-->>B: Capacity: YES
```

**Handling:** Optimistic locking with soft reservation (5 min TTL).

---

## 📊 Algorithm Performance

### Expected Metrics

| Metric | Target | Notes |
|--------|--------|-------|
| Decision Time | < 50ms | Excluding network |
| Cache Hit Rate | > 80% | For repeated queries |
| Accuracy | ±10% | Predicted vs actual completion |
| False Positive Rate | < 5% | "Ship today" but didn't |
| False Negative Rate | < 10% | "Ship tomorrow" but could have |

### Tuning Parameters

| Parameter | Default | Range | Impact |
|-----------|---------|-------|--------|
| `MAX_UTILIZATION` | 0.85 | 0.80-0.95 | Higher = more risk |
| `SAFETY_BUFFER` | 30 min | 15-60 min | Higher = more conservative |
| `VIP_RESERVE` | 0.10 | 0.05-0.20 | Higher = less standard capacity |
| `CONGESTION_ALPHA` | 1.2 | 0.5-2.0 | Higher = more pessimistic |
| `CACHE_TTL` | 60s | 30-300s | Higher = less fresh |

---

[← Architecture](02-architecture.md) | [Next: Data Model →](04-data-model.md)

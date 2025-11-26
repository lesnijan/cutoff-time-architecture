# 🏗️ Architecture

> C4 Model - System Architecture Documentation

[← Executive Summary](01-executive-summary.md) | [Next: Algorithm →](03-algorithm.md)

---

## 📐 C4 Model Overview

C4 Model to hierarchiczny sposób opisu architektury na 4 poziomach:
1. **Context** - system i jego otoczenie
2. **Container** - komponenty wysokopoziomowe
3. **Component** - wewnętrzna struktura kontenerów
4. **Code** - szczegóły implementacji

---

## Level 1: System Context Diagram

Widok z lotu ptaka - system i jego interakcje z użytkownikami oraz zewnętrznymi systemami.

```mermaid
graph TB
    subgraph USERS["👥 UŻYTKOWNICY"]
        U1["🧑‍💼 Handlowiec<br/><i>Sprawdza dostępność wysyłki</i>"]
        U2["👷 Kierownik Magazynu<br/><i>Monitoruje obciążenie</i>"]
        U3["📊 Dyrektor Operacji<br/><i>Analizuje KPI</i>"]
    end
    
    SYSTEM["🎯 <b>CUTOFF TIME SYSTEM</b><br/><br/>• Oblicza obciążenie magazynu<br/>• Wyznacza dynamiczny Cutoff<br/>• Odpowiada na zapytania<br/>• Generuje alerty"]
    
    subgraph EXTERNAL["🔗 SYSTEMY ZEWNĘTRZNE"]
        E1["📦 SAP S/4HANA<br/><i>Źródło danych</i>"]
        E2["☁️ SAP BTP<br/><i>Platforma chmurowa</i>"]
        E3["📈 Grafana<br/><i>Monitoring</i>"]
        E4["📧 Notifications<br/><i>Email / SMS</i>"]
    end
    
    U1 -->|"Czy zdążymy wysłać?"| SYSTEM
    U2 -->|"Jaki jest stan?"| SYSTEM
    U3 -->|"Raport dzienny"| SYSTEM
    
    SYSTEM <-->|"Dane zleceń"| E1
    SYSTEM <-->|"Hosting API"| E2
    SYSTEM -->|"Metryki"| E3
    SYSTEM -->|"Alerty"| E4
    
    style SYSTEM fill:#0ea5e9,stroke:#0284c7,stroke-width:3px
```

### Actors Description

| Aktor | Rola | Interakcja |
|-------|------|------------|
| **Handlowiec** | Przyjmuje zamówienia od klientów | Sprawdza czy zamówienie zdąży na wysyłkę dziś |
| **Kierownik Magazynu** | Zarządza operacjami | Monitoruje obciążenie, reaguje na alerty |
| **Dyrektor Operacji** | Decyzje strategiczne | Analizuje trendy, KPI, planuje zasoby |

---

## Level 2: Container Diagram

Główne kontenery (deployable units) systemu i ich odpowiedzialności.

```mermaid
graph TB
    subgraph BTP["☁️ SAP BTP (Cloud Foundry)"]
        API["🐍 <b>Cutoff API</b><br/>Python / FastAPI<br/><br/>REST Endpoints:<br/>• POST /capacity/check<br/>• GET /cutoff/current<br/>• GET /status"]
        
        CACHE["⚡ <b>Redis Cache</b><br/>In-Memory Store<br/><br/>• Cached results<br/>• Rate limiting<br/>• Session data"]
    end
    
    subgraph HANA["💾 SAP HANA"]
        CDS1["📊 <b>V_ORDER_WORKLOAD</b><br/>CDS View"]
        CDS2["📊 <b>V_WAREHOUSE_CAPACITY</b><br/>CDS View"]
        CDS3["📊 <b>V_CUTOFF_CALCULATION</b><br/>CDS View"]
    end
    
    subgraph S4["📦 SAP S/4HANA"]
        VBAK["VBAK/VBAP<br/>Sales Orders"]
        LIKP["LIKP/LIPS<br/>Deliveries"]
        RES["Resources<br/>Workers"]
    end
    
    subgraph MON["📈 MONITORING"]
        GRAF["Grafana<br/>Dashboards"]
        ALERT["AlertManager<br/>Notifications"]
    end
    
    API <--> CACHE
    API <-->|SQL| CDS3
    CDS3 --> CDS1
    CDS3 --> CDS2
    
    VBAK -.->|"CDC/Replication"| CDS1
    LIKP -.->|"CDC/Replication"| CDS1
    RES -.->|"CDC/Replication"| CDS2
    
    API -->|"Prometheus metrics"| GRAF
    GRAF --> ALERT
    
    style API fill:#0ea5e9,stroke:#0284c7,stroke-width:2px
    style CDS3 fill:#8b5cf6,stroke:#7c3aed,stroke-width:2px
```

### Container Descriptions

| Container | Technology | Purpose |
|-----------|------------|---------|
| **Cutoff API** | Python, FastAPI | REST API serving decision endpoints |
| **Redis Cache** | Redis | Caching computed results, rate limiting |
| **V_ORDER_WORKLOAD** | HANA CDS View | Calculates workload per order |
| **V_WAREHOUSE_CAPACITY** | HANA CDS View | Calculates available capacity |
| **V_CUTOFF_CALCULATION** | HANA CDS View | Main calculation view |
| **Grafana** | Grafana OSS | Operational dashboards |

---

## 🛠️ Technology Stack

### Backend

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Runtime** | Python | 3.11+ | API implementation |
| **Framework** | FastAPI | 0.100+ | REST API framework |
| **Database** | SAP HANA | 2.0 | In-memory calculations |
| **Cache** | Redis | 7.x | Result caching |
| **Platform** | SAP BTP | - | Cloud hosting |

### Data Layer

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Views** | CDS (Core Data Services) | Declarative data models |
| **Integration** | SAP Event Mesh | Real-time events |
| **Replication** | SLT / CDC | Data synchronization |

### Observability

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Metrics** | Prometheus | Time-series metrics |
| **Dashboards** | Grafana | Visualization |
| **Logs** | OpenSearch | Log aggregation |
| **Tracing** | Jaeger | Distributed tracing |

---

## 🔀 Integration Patterns

### Data Flow Pattern

```mermaid
flowchart LR
    subgraph SOURCE["📥 Source Systems"]
        S4["SAP S/4HANA"]
    end
    
    subgraph INTEGRATION["🔄 Integration"]
        CDC["CDC / SLT"]
        EM["Event Mesh"]
    end
    
    subgraph TARGET["💾 Target"]
        HANA["HANA Cloud"]
    end
    
    subgraph API["🔌 API Layer"]
        REST["REST API"]
    end
    
    S4 -->|"Batch (every 5min)"| CDC
    S4 -->|"Events (real-time)"| EM
    CDC --> HANA
    EM --> REST
    HANA --> REST
    
    style CDC fill:#f59e0b,stroke:#d97706
    style EM fill:#22c55e,stroke:#16a34a
```

### API Integration Pattern

```mermaid
sequenceDiagram
    participant Client as 📱 SAP Fiori
    participant API as 🔌 Cutoff API
    participant Cache as ⚡ Redis
    participant HANA as 💾 SAP HANA
    
    Client->>API: POST /capacity/check
    API->>Cache: Check cache
    
    alt Cache HIT
        Cache-->>API: Cached result
    else Cache MISS
        API->>HANA: Query V_CUTOFF_CALCULATION
        HANA-->>API: Calculation result
        API->>Cache: Store (TTL: 60s)
    end
    
    API-->>Client: Decision response
```

---

## 🔐 Security Architecture

### Authentication & Authorization

```mermaid
graph LR
    subgraph CLIENT["Client"]
        APP["SAP Fiori App"]
    end
    
    subgraph AUTH["Authentication"]
        IAS["SAP IAS"]
        XSUAA["XSUAA"]
    end
    
    subgraph API["Protected API"]
        GW["API Gateway"]
        SVC["Cutoff Service"]
    end
    
    APP -->|"1. Login"| IAS
    IAS -->|"2. JWT Token"| APP
    APP -->|"3. Request + JWT"| GW
    GW -->|"4. Validate"| XSUAA
    XSUAA -->|"5. OK"| GW
    GW -->|"6. Forward"| SVC
    
    style GW fill:#f59e0b,stroke:#d97706
```

### Security Layers

| Layer | Mechanism | Purpose |
|-------|-----------|---------|
| **Transport** | TLS 1.3 | Encryption in transit |
| **Authentication** | OAuth 2.0 / JWT | Identity verification |
| **Authorization** | XSUAA Scopes | Role-based access |
| **Data** | HANA Security | Row-level security |

---

## 📦 Deployment Architecture

### SAP BTP Deployment

```mermaid
graph TB
    subgraph CF["Cloud Foundry Space"]
        subgraph APPS["Applications"]
            API1["cutoff-api<br/>Instance 1"]
            API2["cutoff-api<br/>Instance 2"]
        end
        
        subgraph SERVICES["Backing Services"]
            REDIS["Redis<br/>Service"]
            HANA_SVC["HANA Cloud<br/>Service"]
            XSUAA_SVC["XSUAA<br/>Service"]
        end
    end
    
    LB["Load Balancer"] --> API1
    LB --> API2
    API1 --> REDIS
    API2 --> REDIS
    API1 --> HANA_SVC
    API2 --> HANA_SVC
    API1 --> XSUAA_SVC
    API2 --> XSUAA_SVC
    
    style LB fill:#22c55e,stroke:#16a34a
```

### Environment Strategy

| Environment | Purpose | Data |
|-------------|---------|------|
| **DEV** | Development | Synthetic data |
| **QAS** | Testing & PoC | Anonymized production data |
| **PRD** | Production | Live data |

---

## Architecture Decision Records (ADR)

Key architectural decisions are documented in [ADR folder](../adr/):

- [ADR-001: Technology Choice](../adr/ADR-001-technology-choice.md)

---

[← Executive Summary](01-executive-summary.md) | [Next: Algorithm →](03-algorithm.md)

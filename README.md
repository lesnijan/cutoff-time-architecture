# 🚀 Warehouse Cutoff Time System

> **Real-time Decision Engine for Same-Day Shipping**  
> System Oceny Obciążenia Magazynu - Mechanizm Decyzyjny Real-Time

[![Architecture](https://img.shields.io/badge/Architecture-SAP%20BTP%20%2B%20HANA-blue)](docs/02-architecture.md)
[![Status](https://img.shields.io/badge/Status-Case%20Study-green)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## 🌐 Language / Język

- [English](#-english)
- [Polski](#-polski)

---

# 🇬🇧 English

## 📋 Overview

This repository contains the **complete architectural documentation** for a Real-Time Warehouse Capacity Management System. The system automatically determines the **Cutoff Time** - the latest moment when sales orders can be accepted for same-day shipping.

### 🎯 Problem Statement

| Challenge | Impact |
|-----------|--------|
| No visibility into warehouse load | 72% same-day delivery rate |
| Manual cutoff time decisions | 15 customer complaints/week |
| Reactive instead of proactive | 40h overtime/week |

### 💡 Solution

```mermaid
graph LR
    subgraph INPUT["📥 INPUT"]
        A[Sales Order]
        B[Warehouse State]
        C[Available Resources]
    end
    
    subgraph ENGINE["⚙️ CUTOFF ENGINE"]
        D[Real-Time Algorithm]
    end
    
    subgraph OUTPUT["📤 OUTPUT"]
        E{Decision}
        F[✅ Ship TODAY]
        G[❌ Ship TOMORROW]
    end
    
    A --> D
    B --> D
    C --> D
    D --> E
    E -->|capacity OK| F
    E -->|exceeded| G
    
    style D fill:#0ea5e9,stroke:#0284c7,stroke-width:2px
    style F fill:#22c55e,stroke:#16a34a
    style G fill:#ef4444,stroke:#dc2626
```

### 🏗️ Architecture Overview

```mermaid
graph TB
    subgraph USERS["👥 Users"]
        U1["Sales Rep"]
        U2["Warehouse Manager"]
    end
    
    subgraph BTP["☁️ SAP BTP"]
        API["Python API<br/>FastAPI"]
        CACHE["Redis Cache"]
    end
    
    subgraph HANA["💾 SAP HANA"]
        CDS["CDS Views<br/>Real-time Calculation"]
    end
    
    subgraph S4["📦 SAP S/4HANA"]
        DATA["Orders & Deliveries"]
    end
    
    subgraph MON["📈 Monitoring"]
        GRAF["Grafana"]
    end
    
    U1 --> API
    U2 --> GRAF
    API <--> CACHE
    API <--> CDS
    CDS <--> DATA
    API --> GRAF
    
    style API fill:#0ea5e9,stroke:#0284c7,stroke-width:2px
```

### 📊 Key Metrics (Expected Outcomes)

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Same-Day Delivery Rate | 72% | 85% | +18% |
| Promise Accuracy | 65% | 90% | +38% |
| Weekly Complaints | 15 | 5 | -67% |
| Overtime Hours | 40h | 20h | -50% |
| API Response Time | N/A | <500ms | - |

### 📁 Documentation Structure

```
📂 cutoff-time-architecture/
├── 📄 README.md                    ← You are here
├── 📂 docs/
│   ├── 01-executive-summary.md     ← Business overview
│   ├── 02-architecture.md          ← C4 diagrams, tech stack
│   ├── 03-algorithm.md             ← Decision logic, math model
│   ├── 04-data-model.md            ← ERD, SAP tables mapping
│   ├── 05-api-specification.md     ← REST API (OpenAPI)
│   └── 06-implementation-plan.md   ← Timeline, risks, KPIs
├── 📂 adr/
│   └── ADR-001-technology-choice.md
├── 📄 index.html                   ← Interactive visualization
└── 📄 LICENSE
```

### 🚀 Quick Links

| Document | Description |
|----------|-------------|
| [📊 Interactive Visualization](https://lesnijan.github.io/cutoff-time-architecture/) | Full interactive diagrams |
| [🏗️ Architecture](docs/02-architecture.md) | C4 Model, Container Diagram |
| [🧮 Algorithm](docs/03-algorithm.md) | Decision flowchart, math model |
| [🗄️ Data Model](docs/04-data-model.md) | ERD, SAP tables |
| [🔌 API Spec](docs/05-api-specification.md) | REST endpoints |

---

# 🇵🇱 Polski

## 📋 Przegląd

To repozytorium zawiera **kompletną dokumentację architektoniczną** Systemu Zarządzania Przepustowością Magazynu w czasie rzeczywistym. System automatycznie wyznacza **Cutoff Time** - ostatni moment, w którym można przyjąć zamówienia z wysyłką tego samego dnia.

### 🎯 Problem Biznesowy

| Wyzwanie | Skutek |
|----------|--------|
| Brak widoczności obciążenia magazynu | 72% wysyłek tego samego dnia |
| Ręczne ustalanie cutoff time | 15 reklamacji tygodniowo |
| Reakcyjne zamiast proaktywnego podejścia | 40h nadgodzin tygodniowo |

### 💡 Rozwiązanie

```mermaid
graph LR
    subgraph INPUT["📥 WEJŚCIE"]
        A[Zlecenie Sprzedaży]
        B[Stan Magazynu]
        C[Dostępne Zasoby]
    end
    
    subgraph ENGINE["⚙️ SILNIK CUTOFF"]
        D[Algorytm Real-Time]
    end
    
    subgraph OUTPUT["📤 WYJŚCIE"]
        E{Decyzja}
        F[✅ Wysyłka DZIŚ]
        G[❌ Wysyłka JUTRO]
    end
    
    A --> D
    B --> D
    C --> D
    D --> E
    E -->|capacity OK| F
    E -->|przekroczone| G
    
    style D fill:#0ea5e9,stroke:#0284c7,stroke-width:2px
    style F fill:#22c55e,stroke:#16a34a
    style G fill:#ef4444,stroke:#dc2626
```

### 🛠️ Stos Technologiczny

| Warstwa | Technologia | Rola |
|---------|-------------|------|
| **API** | Python + FastAPI | Mikroserwis decyzyjny |
| **Baza** | SAP HANA | CDS Views, In-Memory |
| **Hosting** | SAP BTP | Cloud Foundry |
| **Monitoring** | Grafana + OpenSearch | Dashboardy, alerty |
| **Integracja** | SAP Event Mesh | Event-driven |

### 📅 Fazy Projektu

```mermaid
gantt
    title Harmonogram Projektu
    dateFormat  YYYY-MM-DD
    
    section FAZA 1
    Discovery Workshop     :f1, 2024-01-08, 2w
    Analiza & Dokumentacja :f2, after f1, 4w
    Gate Decyzyjny         :milestone, m1, after f2, 0d
    
    section FAZA 2
    Development HANA       :f3, after m1, 4w
    Development API        :f4, after f3, 3w
    Testy PoC              :f5, after f4, 2w
    
    section FAZA 3
    Wdrożenie PROD         :f6, after f5, 3w
    Hypercare              :f7, after f6, 2w
```

### 💰 Budżet

| Faza | Czas | Koszt (netto) |
|------|------|---------------|
| **FAZA 1:** Discovery | 92h | 25 600 PLN |
| **FAZA 2:** PoC | 120-160h | 38 400 - 51 200 PLN |
| **FAZA 3:** PROD | T&M | Do wyceny |

### 📁 Struktura Dokumentacji

| Dokument | Opis |
|----------|------|
| [📊 Wizualizacja Interaktywna](https://lesnijan.github.io/cutoff-time-architecture/) | Pełne diagramy interaktywne |
| [🏗️ Architektura](docs/02-architecture.md) | Model C4, Container Diagram |
| [🧮 Algorytm](docs/03-algorithm.md) | Flowchart decyzyjny, model matematyczny |
| [🗄️ Model Danych](docs/04-data-model.md) | ERD, mapowanie tabel SAP |
| [🔌 Specyfikacja API](docs/05-api-specification.md) | Endpointy REST |

---

## 👤 Author / Autor

**Janusz Leśniewicz**  
Solution Architect | Data Engineer | 20+ lat doświadczenia

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Janusz%20Leśniewicz-blue?logo=linkedin)](https://www.linkedin.com/in/janusz-lesniewicz/)
[![GitHub](https://img.shields.io/badge/GitHub-lesnijan-black?logo=github)](https://github.com/lesnijan)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <i>Crafted with precision. From Concept to Production.</i>
</p>

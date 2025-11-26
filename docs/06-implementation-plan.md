# 📅 Implementation Plan

> Timeline, Risks, and KPIs

[← API Specification](05-api-specification.md) | [Back to README →](../README.md)

---

## 📊 Project Phases

```mermaid
gantt
    title Cutoff Time System - Implementation Timeline
    dateFormat  YYYY-MM-DD
    
    section PHASE 1: Discovery
    Discovery Workshop        :f1_1, 2024-01-08, 1w
    Post-workshop Analysis    :f1_2, after f1_1, 2w
    Algorithm Specification   :f1_3, after f1_2, 1w
    Architecture Design       :f1_4, after f1_2, 1w
    Documentation (RES 1-4)   :f1_5, after f1_3, 1w
    Decision Gate            :milestone, m1, after f1_5, 0d
    
    section PHASE 2: PoC
    HANA CDS Development     :f2_1, after m1, 3w
    API Development          :f2_2, after f2_1, 2w
    Integration (Event Mesh) :f2_3, after f2_2, 1w
    Testing in QAS           :f2_4, after f2_3, 2w
    PoC Acceptance           :milestone, m2, after f2_4, 0d
    
    section PHASE 3: Production
    PROD Deployment          :f3_1, after m2, 1w
    Monitoring Setup         :f3_2, after f3_1, 1w
    Dashboard Configuration  :f3_3, after f3_2, 1w
    Hypercare               :f3_4, after f3_3, 2w
    Go-Live                 :milestone, m3, after f3_4, 0d
```

---

## 📋 Phase Details

### PHASE 1: Discovery & Design (6 weeks)

| Week | Activity | Deliverable |
|------|----------|-------------|
| 1-2 | Discovery Workshop | Process map, requirements |
| 2-3 | Data Analysis | SAP tables mapping |
| 3-4 | Algorithm Design | Mathematical model |
| 4-5 | Architecture | C4 diagrams, ADR |
| 5-6 | Documentation | RES 1-4 package |

**Deliverables (RES 1-4):**
- RES 1: Algorithm Specification
- RES 2: Integration Architecture
- RES 3: Phase 2 Detailed Quote
- RES 4: BI Tools Assessment

**Gate Criteria:**
- [ ] Algorithm approved by business
- [ ] Data sources confirmed
- [ ] Environment access granted
- [ ] Phase 2 budget approved

---

### PHASE 2: Proof of Concept (9 weeks)

```mermaid
flowchart LR
    subgraph HANA["HANA Development (3w)"]
        H1["CDS Views"] --> H2["Unit Tests"] --> H3["Performance Tests"]
    end
    
    subgraph API["API Development (2w)"]
        A1["Endpoints"] --> A2["Business Logic"] --> A3["Integration"]
    end
    
    subgraph INT["Integration (1w)"]
        I1["Event Mesh"] --> I2["End-to-End"]
    end
    
    subgraph TEST["Testing (2w)"]
        T1["Integration Tests"] --> T2["UAT"] --> T3["Sign-off"]
    end
    
    HANA --> API --> INT --> TEST
```

| Week | Activity | Owner |
|------|----------|-------|
| 8-10 | CDS Views Development | LR Systems |
| 10 | Mid-PoC Review | Joint |
| 11-12 | Python API Development | LR Systems |
| 13 | Event Mesh Integration | Joint |
| 14-15 | QAS Testing | Joint |
| 15 | PoC Acceptance | Client |

**Deliverables:**
- RES 5: Working API in QAS
- RES 6: Source code & documentation

---

### PHASE 3: Production (5 weeks)

| Week | Activity | Responsibility |
|------|----------|----------------|
| 17 | PROD Deployment | Joint |
| 18 | Grafana Setup | LR Systems |
| 19 | Alerting Config | Joint |
| 20-21 | Hypercare | LR Systems |

**Go-Live Criteria:**
- [ ] All tests passed in PROD
- [ ] Dashboards operational
- [ ] Alerts configured
- [ ] Runbook documented
- [ ] Support handover complete

---

## 💰 Budget Summary

| Phase | Effort | Rate | Total (Net) |
|-------|--------|------|-------------|
| **PHASE 1** | 92h | 278 PLN/h | **25 600 PLN** |
| **PHASE 2** | 120-160h | 278 PLN/h | **38 400 - 51 200 PLN** |
| **PHASE 3** | T&M | 278 PLN/h | **~20 000 PLN** |
| **TOTAL** | ~300h | - | **~90 000 PLN** |

### Payment Schedule

```mermaid
timeline
    title Payment Milestones
    
    Phase 1 Start : 40% Advance (10 240 PLN)
    Phase 1 End : 60% on RES 1-4 (15 360 PLN)
    Mid-PoC : 50% Phase 2 (19 200 - 25 600 PLN)
    PoC End : 50% Phase 2 (19 200 - 25 600 PLN)
    Phase 3 : Monthly T&M invoicing
```

---

## ⚠️ Risk Assessment

### Risk Matrix

```mermaid
quadrantChart
    title Risk Assessment Matrix
    x-axis Low Impact --> High Impact
    y-axis Low Probability --> High Probability
    
    quadrant-1 CRITICAL
    quadrant-2 HIGH PRIORITY
    quadrant-3 MONITOR
    quadrant-4 MEDIUM
    
    R1: [0.75, 0.5]
    R2: [0.8, 0.5]
    R3: [0.5, 0.5]
    R4: [0.3, 0.5]
    R5: [0.5, 0.7]
```

### Risk Register

| ID | Risk | Prob. | Impact | Mitigation |
|----|------|-------|--------|------------|
| **R1** | Missing SAP documentation | Medium | High | Deep Dive in Discovery; RFI before start |
| **R2** | Undefined "workload" definition | Medium | High | Dedicated workshop; formal sign-off |
| **R3** | Environment access delays | Medium | Medium | RFI includes contact person; prerequisite |
| **R4** | Cognos lacks real-time | Medium | Low | Assessment in Phase 1; Grafana fallback |
| **R5** | Variable warehouse load | High | Medium | PoC with real data; iterative tuning |

### Risk Response Plan

#### R1: Missing SAP Documentation

```mermaid
flowchart LR
    TRIGGER["Documentation<br/>not available"] --> ASSESS["Assess gap<br/>in Discovery"]
    ASSESS --> DECIDE{Gap > 20h<br/>additional?}
    DECIDE -->|Yes| ESCALATE["Escalate to<br/>client sponsor"]
    DECIDE -->|No| ABSORB["Absorb in<br/>contingency"]
    ESCALATE --> REVISE["Revise quote<br/>or T&M"]
```

#### R2: Undefined Workload

```mermaid
flowchart LR
    TRIGGER["No formula<br/>after workshop"] --> SESSION["Dedicated<br/>2h session"]
    SESSION --> PROPOSE["LR proposes<br/>formula"]
    PROPOSE --> VALIDATE["Business<br/>validates"]
    VALIDATE --> SIGNOFF["Formal<br/>sign-off"]
    SIGNOFF --> PROCEED["Proceed to<br/>Phase 2"]
```

---

## 📊 Success Metrics (KPIs)

### Business KPIs

| Metric | Baseline | Target | Stretch | Measurement |
|--------|----------|--------|---------|-------------|
| Same-Day Delivery Rate | 72% | 85% | 92% | Orders shipped same day / total |
| Promise Accuracy | 65% | 90% | 95% | Shipped when promised / promised |
| Weekly Complaints | 15 | 5 | 2 | Shipping-related complaints |
| Overtime Hours | 40h/w | 20h/w | 10h/w | Unplanned overtime |
| Manual Overrides | 25% | 10% | 5% | Override decisions / total |

### Technical KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| API Response Time (p95) | < 500ms | 95th percentile latency |
| API Availability | 99.5% | Uptime percentage |
| Calculation Accuracy | ±10% | Predicted vs actual |
| Data Freshness | < 5 min | Lag from source |
| Error Rate | < 1% | Failed requests / total |

### Dashboard Preview

```
┌─────────────────────────────────────────────────────────────────┐
│                    CUTOFF TIME DASHBOARD                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  CUTOFF  │  │   UTIL   │  │  ORDERS  │  │  STATUS  │       │
│  │  14:30   │  │   78%    │  │    47    │  │ WARNING  │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                                 │
│  Utilization Trend                                             │
│  100% ─────────────────────────────── threshold                │
│   85% ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ warning                 │
│        ╱╲    ╱╲                                                 │
│       ╱  ╲  ╱  ╲    ╱╲                                          │
│      ╱    ╲╱    ╲  ╱  ╲                                         │
│     ╱            ╲╱    ╲  ← current                            │
│    ╱                                                            │
│   06:00   09:00   12:00   15:00   NOW                          │
│                                                                 │
│  Recent Decisions: ✓234 approved │ ✗51 rejected │ ⭐8 VIP     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 👥 Team & Responsibilities

### RACI Matrix

| Activity | LR Systems | Client IT | Client Business |
|----------|------------|-----------|-----------------|
| Algorithm Design | **R** | C | **A** |
| CDS Development | **R/A** | C | I |
| API Development | **R/A** | C | I |
| Testing | **R** | **R** | **A** |
| UAT | S | C | **R/A** |
| Deployment | **R** | **R** | A |
| Monitoring Setup | **R** | C | I |

**Legend:** R=Responsible, A=Accountable, C=Consulted, I=Informed

### Client Resources Required

| Role | Phase 1 | Phase 2 | Phase 3 |
|------|---------|---------|---------|
| Product Owner | 4h/w | 2h/w | 2h/w |
| Warehouse Manager | 8h total | 4h total | 2h total |
| SAP Basis Admin | 8h setup | 2h/w | 2h/w |
| SAP BTP Admin | - | 4h setup | 2h/w |
| BI Analyst | 2h | - | 4h |

---

## 📞 Escalation Path

```mermaid
flowchart TB
    ISSUE["Issue Identified"] --> ASSESS{"Severity?"}
    
    ASSESS -->|Low| L1["Project Manager<br/>Response: 24h"]
    ASSESS -->|Medium| L2["Technical Lead<br/>Response: 8h"]
    ASSESS -->|High| L3["Steering Committee<br/>Response: 4h"]
    ASSESS -->|Critical| L4["Executive Sponsor<br/>Response: 1h"]
    
    L1 --> RESOLVE["Resolution"]
    L2 --> RESOLVE
    L3 --> RESOLVE
    L4 --> RESOLVE
```

### Escalation Criteria

| Level | Criteria | Contact |
|-------|----------|---------|
| **Low** | Minor delays, clarifications | Project Manager |
| **Medium** | Scope questions, resource issues | Technical Lead |
| **High** | Budget impact, timeline risk | Steering Committee |
| **Critical** | Project at risk, blocker | Executive Sponsor |

---

## ✅ Next Steps

1. **Client:** Review and approve proposal
2. **Client:** Complete RFI questionnaire
3. **LR Systems:** Issue pro-forma invoice (40%)
4. **Joint:** Schedule Discovery Workshop
5. **Start:** Phase 1 begins

---

## 📎 Appendices

- [ADR-001: Technology Choice](../adr/ADR-001-technology-choice.md)
- [Interactive Visualization](../index.html)

---

[← API Specification](05-api-specification.md) | [Back to README →](../README.md)

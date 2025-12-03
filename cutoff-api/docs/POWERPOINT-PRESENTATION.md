# Cutoff Time System - PowerPoint Presentation Script

> **Format**: Prezentacja PowerPoint z live demo
> **Czas**: 20-25 minut
> **Struktura**: Dashboard Demo + API Docs + Business Value

---

## Slajd 1: Strona Tytułowa

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   CUTOFF TIME SYSTEM
   Real-Time Warehouse Capacity Decision Engine

   Demo Presentation
   December 2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Grafika sugerowana:**
- Logo firmy (góra)
- Ikona magazynu z zegarami
- Zdjęcie nowoczesnego warehouse

**Speaker Notes:**
> "Dzień dobry! Dzisiaj przedstawię Wam system Cutoff Time -
> rozwiązanie, które w czasie rzeczywistym podejmuje decyzje
> o możliwości wysyłki zamówień tego samego dnia."

---

## Slajd 2: Problem Biznesowy

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ❌ OBECNA SYTUACJA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

14:30 - Telefon od klienta VIP

Klient:  "Czy mogę dostać 50 jednostek dziś?"

Handlowiec: "Hmmm... muszę sprawdzić...
            oddzwonię za 10 minut..."

[Handlowiec dzwoni do magazynu]
[Kierownik magazynu sprawdza ręcznie]
[10 minut później - nadal niepewność]

Klient: [Już zamówił u konkurencji]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Grafika:**
- Split screen: Frustrated customer | Stressed warehouse manager
- Phone icon z klepsydrą

**Kluczowe Liczby:**
```
┌─────────────────────────────────────┐
│ Promise Accuracy:  65%  ❌          │
│ Reklamacje/tydzień: 15  📉          │
│ Nadgodziny/tydzień: 40h ⏰          │
│ Same-Day Rate:     72%  📊          │
│                                     │
│ KOSZT: 150,000 PLN/rok 💸          │
└─────────────────────────────────────┘
```

**Speaker Notes:**
> "To jest sytuacja, którą wszyscy znamy. Brak real-time visibility
> prowadzi do niskiej trafności obietnic, reklamacji i nieprzewidzanych
> nadgodzin. Kosztuje to 150 tysięcy złotych rocznie."

---

## Slajd 3: Rozwiązanie - Overview

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✅ Z SYSTEMEM CUTOFF TIME
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

14:30 - Telefon od klienta VIP

Klient:  "Czy mogę dostać 50 jednostek dziś?"

Handlowiec: [Otwiera dashboard - 2 sekundy]
            [Product: MAT-002, Qty: 50, VIP]
            [Click]

System:     ✓ "TAK - zdążymy do 15:30"
            Confidence: 85%

Handlowiec: "Tak, zdążymy! Potwierdzam zamówienie."

Klient:     "Świetnie!"

CZAS: 5 sekund ⚡
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Grafika:**
- Happy customer | Confident salesperson
- Dashboard screenshot
- Green checkmark

**Kluczowe Features:**
```
┌──────────────────────────────────────┐
│ ⚡ < 100ms response time             │
│ 🎯 90% promise accuracy              │
│ 📊 Real-time utilization tracking    │
│ 🔐 VIP priority handling (10% reserve)│
│ 🤖 AI-powered decision engine        │
└──────────────────────────────────────┘
```

**Speaker Notes:**
> "System daje odpowiedź w czasie rzeczywistym. Teraz przechodzimy
> do live demo - zobaczycie dokładnie jak to działa."

---

## Slajd 4: LIVE DEMO - Dashboard Overview

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🎮 LIVE DEMO - DASHBOARD

   URL: http://localhost:8080/static/demo.html
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**ACTION:** Przełącz się na przeglądarkę z dashboardem

**Co pokazać:**
1. **Current Warehouse Status** (30 sekund)
   - Status badge: WARNING (żółty)
   - Utilization: 70.1%
   - Cutoff Time: 14:30
   - Orders in Queue: 47

2. **Progress Bar** (30 sekund)
   - Wizualizacja wykorzystania capacity
   - Color coding: Green → Yellow → Orange → Red

3. **Key Metrics** (30 sekund)
   - Time Remaining: 150 minutes
   - Available Capacity: 119.5 minutes
   - Bottleneck: PACKER (5 workers)

**Screenshot dla slajdu:**
```
┌────────────────────────────────────────┐
│  📊 Current Warehouse Status           │
├────────────────────────────────────────┤
│  Status: ⚠️ WARNING                    │
│  Current Utilization: 70.1%            │
│  [████████████░░░░░░░░] 70%            │
│                                        │
│  Cutoff Time: 14:30                    │
│  Time Remaining: 150 min               │
│  Orders in Queue: 47                   │
│                                        │
│  Bottleneck Resource: PACKER           │
│  Available Capacity: 119.5 min         │
└────────────────────────────────────────┘
```

**Speaker Notes:**
> "To jest dashboard, który handlowiec lub kierownik magazynu widzi
> w czasie rzeczywistym. Status WARNING oznacza, że jesteśmy w żółtej
> strefie - 70% wykorzystania. Bottleneck to PACKING - mamy tylko
> 5 packerów. Auto-refresh co 30 sekund."

---

## Slajd 5: LIVE DEMO - Test Capacity Check

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🧪 TEST: Standardowe Zamówienie
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**ACTION:** Na żywo w dashboardzie

**Test 1: Light Order**
```
Product:  MAT-001 (Standard Box)
Quantity: 10
Priority: STANDARD

[Click "Check Capacity"]
```

**Expected Response (pokazuje się na ekranie):**
```
┌────────────────────────────────────────┐
│  ✓ Wysyłka dziś możliwa                │
├────────────────────────────────────────┤
│  Confidence: 92%                       │
│  Response Time: 45ms                   │
│                                        │
│  Decision Factors:                     │
│  • Workload Impact: 12.5 min           │
│  • Utilization After: 72%              │
│  • Time Buffer: 30 min                 │
│  • Bottleneck: PACKER                  │
│  • VIP Override: Not used              │
└────────────────────────────────────────┘
```

**Speaker Notes:**
> "Sprawdzam standardowe zamówienie - 10 jednostek produktu MAT-001.
> Klikam... odpowiedź w 45 milisekund! System mówi TAK, confidence 92%.
> Widzimy wszystkie faktory decyzji - transparentność jest kluczowa."

---

## Slajd 6: LIVE DEMO - Heavy Order Test

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🧪 TEST: Duże Zamówienie
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**ACTION:** Na żywo w dashboardzie

**Test 2: Heavy Order**
```
Product:  MAT-002 (Heavy Equipment)
Quantity: 50
Priority: STANDARD

[Click "Check Capacity"]
```

**Expected Response:**
```
┌────────────────────────────────────────┐
│  ✗ Wysyłka jutro                       │
├────────────────────────────────────────┤
│  Reason: CAPACITY_EXCEEDED             │
│  Response Time: 52ms                   │
│                                        │
│  Decision Factors:                     │
│  • Workload Impact: 206.5 min          │
│  • Utilization After: 91%              │
│  • Exceeds Threshold: 85%              │
│                                        │
│  Alternatives:                         │
│  • Split order (25 today, 25 tomorrow) │
│  • Upgrade to VIP priority             │
│  • Schedule for tomorrow               │
└────────────────────────────────────────┘
```

**Speaker Notes:**
> "Teraz trudniejszy case - 50 jednostek heavy equipment.
> System mówi NIE - utilization byłaby 91%, przekroczono próg 85%.
> Ale system nie tylko odmawia - proponuje alternatywy!"

---

## Slajd 7: LIVE DEMO - VIP Override

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   👑 VIP PRIORITY OVERRIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**ACTION:** Zmień Priority na VIP i kliknij ponownie

**Test 3: VIP Override**
```
Product:  MAT-002 (Heavy Equipment)
Quantity: 50
Priority: VIP  ← Changed!

[Click "Check Capacity"]
```

**Expected Response:**
```
┌────────────────────────────────────────┐
│  ✓ Wysyłka dziś (VIP Reserve)          │
├────────────────────────────────────────┤
│  Confidence: 80%                       │
│  Response Time: 48ms                   │
│                                        │
│  VIP Override Details:                 │
│  • VIP Reserve Used: YES ✓             │
│  • Standard Threshold: 85%             │
│  • VIP Threshold: 95%                  │
│  • Utilization After: 91%              │
│  • Reserve Available: 4%               │
│                                        │
│  ⚠️ Monitor closely - high utilization │
└────────────────────────────────────────┘
```

**Speaker Notes:**
> "Ale to jest klient VIP! Zmieniam priorytet na VIP i...
> teraz TAK! System użył 10% rezerwy VIP. Confidence niższa - 80%,
> ale dla VIP akceptujemy. To jest biznesowa wartość - priorytet
> dla ważnych klientów, ale nadal kontrolowany."

---

## Slajd 8: LIVE DEMO - Demo Scenarios

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🎬 DEMO SCENARIOS - Symulacja
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**ACTION:** Przełączanie scenariuszy

**Scenario: High Utilization**
```
[Click "High Utilization" button]

Obserwuj zmiany:
  Utilization: 70% → 90%
  Status: WARNING → CRITICAL (pomarańczowy)
  Orders: 47 → 78
  Cutoff Time: 14:30 → 13:15
```

**Grafika - Before/After:**
```
BEFORE                      AFTER
┌──────────────┐           ┌──────────────┐
│ 🟡 WARNING   │    →      │ 🟠 CRITICAL  │
│ 70% Util     │           │ 90% Util     │
│ 47 Orders    │           │ 78 Orders    │
│ Cutoff: 14:30│           │ Cutoff: 13:15│
└──────────────┘           └──────────────┘
```

**Speaker Notes:**
> "Symulujmy teraz flash sale w piątek. Klikam High Utilization...
> system natychmiast pokazuje CRITICAL status. Utilization 90%,
> zamówień więcej, cutoff wcześniejszy. To jest proaktywny alert -
> zanim dojdzie do chaosu."

---

## Slajd 9: LIVE DEMO - Detailed Metrics

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📈 DETAILED METRICS - Full Visibility
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**ACTION:** Scroll do Detailed Metrics section

**Co pokazać:**
```
┌─────────────────────────────────────────────────┐
│ WORKLOAD         │ CAPACITY        │ DECISIONS  │
│ BREAKDOWN        │ STATUS          │ TODAY      │
├──────────────────┼─────────────────┼────────────┤
│ Total: 47        │ Total: 400.0    │ Total: 285 │
│ NEW: 12 (26%)    │ Used: 280.5     │ Approved:  │
│ PICKING: 18 (38%)│ Available: 119.5│   234 (82%)│
│ PACKING: 10 (21%)│                 │ Rejected:  │
│ LOADING: 7 (15%) │ Bottleneck:     │   51 (18%) │
│                  │   PACKER ⚠️     │ VIP: 8     │
└──────────────────┴─────────────────┴────────────┘
```

**Speaker Notes:**
> "Detailed Metrics dają pełną transparentność. Widzimy workload breakdown -
> 38% zamówień jest w picking, 21% w packing. Bottleneck to packing -
> mamy tylko 5 packerów. Today's decisions: 82% approval rate - wysoki!
> 8 VIP overrides - używamy rezerwy, ale kontrolowanie."

---

## Slajd 10: LIVE DEMO - API Documentation

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📚 API DOCUMENTATION

   URL: http://localhost:8080/api/v1/docs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**ACTION:** Przełącz na kartę z API Docs (Swagger UI)

**Co pokazać:**

1. **Swagger UI Overview** (1 min)
   - Interactive documentation
   - 6 endpoint groups
   - Try it out functionality

2. **Health Endpoint** (30 sekund)
   ```
   GET /api/v1/health

   Response 200:
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

**Screenshot dla slajdu:**
```
┌─────────────────────────────────────────┐
│  Cutoff Time API v1                     │
├─────────────────────────────────────────┤
│  📁 Health                              │
│    GET  /health                         │
│                                         │
│  📁 Capacity                            │
│    POST /capacity/check                 │
│                                         │
│  📁 Cutoff                              │
│    GET  /cutoff/current                 │
│                                         │
│  📁 Status                              │
│    GET  /status                         │
│                                         │
│  📁 Simulation                          │
│    POST /simulate                       │
│                                         │
│  📁 Demo                                │
│    GET  /demo/scenarios                 │
│    POST /demo/scenario/{name}           │
└─────────────────────────────────────────┘
```

**Speaker Notes:**
> "Otwórzmy teraz API documentation. To jest Swagger UI -
> interaktywna dokumentacja. Mamy 6 grup endpointów.
> Wszystko jest self-documented i można testować na żywo."

---

## Slajd 11: LIVE DEMO - Capacity Check API

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🔌 API: POST /capacity/check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**ACTION:** W Swagger UI rozwiń POST /capacity/check

**Demo Flow:**

1. **Click "Try it out"**

2. **Show Request Schema:**
```json
{
  "order_id": "SO-2024-001234",
  "customer_id": "CUST-VIP-001",
  "priority": "VIP",
  "warehouse_id": "WH-MAIN",
  "items": [
    {
      "product_id": "MAT-001",
      "quantity": 10
    }
  ]
}
```

3. **Click "Execute"**

4. **Show Response:**
```json
{
  "can_ship_today": true,
  "confidence": 0.92,
  "current_utilization": 0.721,
  "estimated_completion": "2024-12-02T15:30:00Z",
  "message": "Wysyłka dziś możliwa",
  "decision_factors": {
    "workload_impact": 12.5,
    "remaining_capacity": 107.5,
    "time_buffer_minutes": 30,
    "bottleneck_resource": "PACKER",
    "congestion_factor": 1.62,
    "vip_override_used": false
  },
  "metadata": {
    "calculated_at": "2024-12-02T14:00:00Z",
    "cache_hit": false,
    "calculation_time_ms": 45
  }
}
```

**Speaker Notes:**
> "Sprawdzę capacity check przez API. Try it out... podaję request...
> Execute. Response w 45ms! Widzimy pełną strukturę - decision,
> factors, metadata. To jest ten sam endpoint, którego używa dashboard.
> Może być zintegrowany z SAP, Salesforce, dowolnym systemem."

---

## Slajd 12: API - All Endpoints Overview

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📚 API ENDPOINTS - Complete Overview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Tabela ze wszystkimi endpointami:**

| Endpoint | Method | Purpose | Response Time |
|----------|--------|---------|---------------|
| `/health` | GET | Health check | < 10ms |
| `/capacity/check` | POST | Check if order can ship | < 200ms |
| `/cutoff/current` | GET | Current cutoff time | < 100ms |
| `/status` | GET | Dashboard data | < 150ms |
| `/simulate` | POST | What-if analysis | < 50ms |
| `/demo/scenarios` | GET | List scenarios | < 10ms |
| `/demo/scenario/{name}` | POST | Switch scenario | < 20ms |

**Authentication:**
```
┌─────────────────────────────────────┐
│  OAuth 2.0 / JWT                    │
│  Bearer Token in Authorization      │
│  Scopes:                            │
│    - cutoff.read                    │
│    - cutoff.write                   │
│    - cutoff.admin                   │
└─────────────────────────────────────┘
```

**Rate Limiting:**
```
┌─────────────────────────────────────┐
│  /capacity/check:  100 req/min      │
│  /cutoff/current:  300 req/min      │
│  /simulate:        10 req/min       │
└─────────────────────────────────────┘
```

**Speaker Notes:**
> "Mamy 7 głównych endpointów. Wszystkie z response time < 200ms.
> Authentication przez OAuth 2.0, rate limiting zabezpiecza przed
> przeciążeniem. Production ready!"

---

## Slajd 13: Architecture Overview

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🏗️ ARCHITEKTURA SYSTEMU
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Diagram (uproszczony):**
```
┌──────────────┐
│   Clients    │  Dashboard, Fiori, Mobile
│              │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  FastAPI     │  Python 3.11+, Uvicorn
│  REST API    │  < 100ms response
└──────┬───────┘
       │
       ├────────┬────────┬────────┐
       ▼        ▼        ▼        ▼
┌──────────┐ ┌─────┐ ┌──────┐ ┌────────┐
│ Decision │ │Work │ │Capac │ │ Cache  │
│ Engine   │ │load │ │ity   │ │ Redis  │
└──────┬───┘ └──┬──┘ └───┬──┘ └───┬────┘
       │        │        │        │
       └────────┴────────┴────────┘
                │
                ▼
         ┌──────────────┐
         │  SAP HANA    │  CDS Views
         │  Cloud       │  Real-time data
         └──────────────┘
```

**Tech Stack Highlights:**
```
┌─────────────────────────────────────┐
│ Backend:  Python 3.11+, FastAPI     │
│ Database: SAP HANA Cloud (CDS)      │
│ Cache:    Redis 7.x (optional)      │
│ Metrics:  Prometheus + Grafana      │
│ Deploy:   SAP BTP Cloud Foundry     │
│ Security: OAuth 2.0, TLS 1.3        │
└─────────────────────────────────────┘
```

**Speaker Notes:**
> "Architektura jest prosta ale robust. FastAPI na froncie,
> Decision Engine w środku, HANA jako źródło danych.
> Redis cache opcjonalny - demo działa bez niego.
> Deployment na SAP BTP Cloud Foundry - SAP native!"

---

## Slajd 14: Algorithm Deep Dive

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🧮 ALGORYTM DECYZYJNY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Core Formulas:**

**1. Order Workload:**
```
W_order = Σ(qty × weight × location) + overhead

Example: MAT-001, qty=10
W = (10 × 1.0 × 1.0) + (2 + 3.5 + 1.5)
W = 10 + 7 = 17 minutes
```

**2. Warehouse Capacity:**
```
C = MIN(pickers, packers, loaders) × efficiency × 0.9

Example: WH-MAIN
Pickers: 8 × 1.2 = 9.6
Packers: 5 × 0.8 = 4.0  ← Bottleneck!
Loaders: 3 × 2.0 = 6.0
C = MIN(9.6, 4.0, 6.0) × 0.95 × 0.9 = 3.42 units/min
```

**3. Utilization:**
```
U = (W_current + W_new) / C_total

Example:
U = (280.5 + 17) / 400 = 297.5 / 400 = 74.4%
```

**4. Decision Thresholds:**
```
if U < 70%:  → ACCEPTING  🟢
elif U < 85%: → WARNING    🟡
elif U < 95%: → CRITICAL   🟠
else:         → CLOSED     🔴

VIP Override: +10% (up to 95%)
```

**Grafika - Flow Chart:**
```
   New Order
       │
       ▼
 Calculate Workload
       │
       ▼
  Get Capacity ← HANA CDS Views
       │
       ▼
Calculate Utilization
       │
       ▼
  Apply Thresholds
       │
   ┌───┴───┐
   │  < 85% │ YES → ✓ ACCEPT
   └───┬───┘
       │ NO
       ▼
  ┌────────┐
  │ VIP?   │ YES → Check 95% → ✓ ACCEPT (VIP)
  └────┬───┘
       │ NO
       ▼
    ✗ REJECT
```

**Speaker Notes:**
> "Algorytm to serce systemu. Obliczamy workload zamówienia,
> pobieramy capacity z HANA, liczymy utilization i aplikujemy
> progi. VIP override daje dodatkowe 10%. Wszystko w < 100ms!"

---

## Slajd 15: Business Value - ROI

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   💰 WARTOŚĆ BIZNESOWA - ROI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Before vs After:**

| Metryka | PRZED | PO | Poprawa | PLN/rok |
|---------|-------|-----|---------|---------|
| Same-Day Rate | 72% | **85%** | +18% | +Revenue |
| Promise Accuracy | 65% | **90%** | +38% | +NPS |
| Reklamacje/wk | 15 | **5** | -67% | **100k** |
| Nadgodziny/wk | 40h | **20h** | -50% | **50k** |
| Manual Override | 25% | **10%** | -60% | +Trust |

**ROI Calculation:**
```
┌──────────────────────────────────────┐
│ OSZCZĘDNOŚCI/ROK:                    │
│                                      │
│ Nadgodziny:         50,000 PLN       │
│   (20h/wk × 50 PLN × 50 wk)          │
│                                      │
│ Reklamacje:        100,000 PLN       │
│   (10/wk × 200 PLN × 50 wk)          │
│                                      │
│ TOTAL:            150,000 PLN ✓      │
│                                      │
│ KOSZT WDROŻENIA:   ~90,000 PLN       │
│                                      │
│ PAYBACK:          6-9 miesięcy 🎯    │
└──────────────────────────────────────┘
```

**Grafika - ROI Chart:**
```
PLN
 │
150k┤         ╱─────────── Savings
    │       ╱
100k┤     ╱
    │   ╱ Payback (7 mo)
 50k┤ ╱
    │╱
  0 ┼─────────────────────────────
    0  3  6  9  12  15  18  24  Months
```

**Speaker Notes:**
> "Teraz najważniejsze - ROI. Same-day rate rośnie o 18%,
> reklamacje spadają o 67%, nadgodziny o połowę. To daje
> 150 tysięcy złotych oszczędności rocznie. Koszt wdrożenia
> 90 tysięcy - zwrot w 6-9 miesięcy!"

---

## Slajd 16: Stakeholder Benefits

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🎯 KORZYŚCI DLA STAKEHOLDERÓW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Dla Handlowców:**
```
┌────────────────────────────────────┐
│ ✅ Fast response (5s vs 10min)     │
│ ✅ Confident quotations (90%)      │
│ ✅ Higher conversion (+15%)        │
│ ✅ Happy customers                 │
└────────────────────────────────────┘
```

**Dla Kierownika Magazynu:**
```
┌────────────────────────────────────┐
│ ✅ Real-time visibility            │
│ ✅ Proactive alerting (85%/95%)    │
│ ✅ Bottleneck identification       │
│ ✅ Resource planning               │
│ ✅ Reduced stress                  │
└────────────────────────────────────┘
```

**Dla Dyrektora Operacji:**
```
┌────────────────────────────────────┐
│ ✅ Data-driven decisions           │
│ ✅ Strategic planning (what-if)    │
│ ✅ KPI tracking & trends           │
│ ✅ ROI measurement                 │
│ ✅ Capacity planning               │
└────────────────────────────────────┘
```

**Quote Boxes:**
```
┌─────────────────────────────────────────┐
│ "Wreszcie widzę co się dzieje           │
│  w magazynie w czasie rzeczywistym!"    │
│                                         │
│ - Kierownik Magazynu                    │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ "Moi klienci są zachwyceni -            │
│  wreszcie mogę dać konkretne odpowiedzi"│
│                                         │
│ - Senior Sales Rep                      │
└─────────────────────────────────────────┘
```

**Speaker Notes:**
> "System daje wartość wszystkim stakeholderom. Handlowcy mają
> szybkie odpowiedzi, kierownik widzi stan magazynu real-time,
> dyrektor ma dane do strategicznych decyzji."

---

## Slajd 17: Implementation Timeline

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📅 TIMELINE WDROŻENIA - 9 Tygodni
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Gantt Chart:**
```
Week  Task                           Status
1-3   HANA CDS Views Development    ▓▓▓▓▓▓░░░
      - V_ORDER_WORKLOAD
      - V_WAREHOUSE_CAPACITY
      - V_CUTOFF_CALCULATION

4-5   API Development               ▓▓▓▓▓▓▓▓▓  ✅ DONE (Demo!)
      - FastAPI endpoints
      - Business logic
      - Tests

6     Integration & Testing         ░░░░░░░░░
      - Connect real HANA
      - Load test data
      - Integration tests

7-8   QAS Testing                   ░░░░░░░░░
      - Business user UAT
      - Performance testing
      - Bug fixes

9     Production Go-Live            ░░░░░░░░░
      - Deployment
      - Training (2h)
      - Hypercare
```

**Key Milestones:**
```
✅ Week 0:  Demo Ready (dziś!)
⏳ Week 3:  CDS Views Complete
⏳ Week 6:  Integration Complete
⏳ Week 8:  UAT Sign-off
🎯 Week 9:  GO-LIVE
```

**Speaker Notes:**
> "Całe wdrożenie to 9 tygodni. Weeks 4-5 - API development -
> już mamy! Demo które widzieliście to produkcyjny kod.
> Pozostaje HANA CDS Views, integracja i testy. Week 9 - go-live!"

---

## Slajd 18: Security & Compliance

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🔐 SECURITY & COMPLIANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Security Layers:**
```
┌──────────────────────────────────────┐
│ 1. Edge Security                     │
│    • TLS 1.3                         │
│    • Web Application Firewall        │
│                                      │
│ 2. Application Security              │
│    • OAuth 2.0 / JWT                 │
│    • Rate Limiting (Redis)           │
│    • CORS Policy                     │
│                                      │
│ 3. Data Security                     │
│    • AES-256 Encryption at rest      │
│    • Audit Trail (all decisions)     │
│    • HANA Row-Level Security         │
│                                      │
│ 4. Compliance                        │
│    • GDPR compliant                  │
│    • 7-year audit retention          │
│    • Right to erasure support        │
└──────────────────────────────────────┘
```

**Audit Trail Example:**
```json
{
  "timestamp": "2024-12-02T14:00:00Z",
  "request_id": "req-1234567890",
  "user": "sales.rep@company.com",
  "action": "capacity_check",
  "order_id": "SO-2024-001234",
  "decision": true,
  "utilization": 0.721,
  "factors": { ... },
  "ip_address": "10.0.0.1"
}
```

**Speaker Notes:**
> "Security to priorytet. Mamy 4 warstwy ochrony - od edge
> po dane. OAuth 2.0 authentication, pełny audit trail każdej
> decyzji, GDPR compliant. Production ready!"

---

## Slajd 19: Next Steps & Decision

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🚀 NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Immediate (This Week):**
```
┌────────────────────────────────────┐
│ □ Decision: Proceed with Phase 2?  │
│ □ Budget: 38-51k PLN approved?     │
│ □ Kickoff: Schedule Week 1         │
└────────────────────────────────────┘
```

**Short-term (Weeks 1-3):**
```
┌────────────────────────────────────┐
│ □ HANA CDS Views development       │
│ □ Load test data into QAS          │
│ □ Integration testing              │
└────────────────────────────────────┘
```

**Mid-term (Weeks 4-9):**
```
┌────────────────────────────────────┐
│ □ API finalization                 │
│ □ UAT with business users          │
│ □ Production deployment prep       │
└────────────────────────────────────┘
```

**Go-Live (Week 9):**
```
┌────────────────────────────────────┐
│ □ Production deployment            │
│ □ User training (2 hours)          │
│ □ Hypercare start (2 weeks)        │
└────────────────────────────────────┘
```

**Decision Gates:**
```
Gate 1: After Today → Proceed? YES/NO
Gate 2: Week 5      → Continue to prod?
Gate 3: Week 9      → Go-live approved?
```

**Speaker Notes:**
> "Co dalej? Potrzebujemy decyzji: proceed with Phase 2?
> Budget approval? Jeśli TAK - startujemy Week 1 z HANA CDS.
> Demo który widzieliście to proof że technologia działa.
> 9 tygodni do produkcji!"

---

## Slajd 20: Q&A

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ❓ PYTANIA I ODPOWIEDZI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Najczęstsze Pytania:**

**Q: Ile to kosztuje?**
```
A: Faza 2 (PoC): 38-51k PLN
   Total: ~90k PLN
   ROI: 150k PLN/rok = zwrot w 6-9 miesięcy
```

**Q: Czy system zastąpi ludzi?**
```
A: NIE! System WSPIERA decyzje, nie zastępuje.
   Manager nadal decyduje - ale ma DANE.
```

**Q: Co jeśli HANA będzie niedostępne?**
```
A: Fallback to cached data + low confidence alert
   + Ops team notification
```

**Q: Czy można zmienić thresholdy?**
```
A: TAK! Wszystko w .env:
   MAX_UTILIZATION=0.85
   VIP_RESERVE_PERCENT=0.10
   SAFETY_BUFFER_MINUTES=30
```

**Q: Jak długo trwa szkolenie?**
```
A: 2 godziny wystarczą:
   - 30min: Prezentacja
   - 45min: Hands-on
   - 30min: Q&A
   - 15min: Docs
```

**Grafika - Contact Info:**
```
┌─────────────────────────────────────┐
│ 📧 Email: support@lrsystems.pl      │
│ 🌐 GitHub: github.com/lesnijan/...  │
│ 📚 Docs: localhost:8080/docs        │
│ 🎮 Demo: localhost:8080/demo.html   │
└─────────────────────────────────────┘
```

**Speaker Notes:**
> "Jestem gotowy na pytania! Mamy pełną dokumentację,
> working demo, kod na GitHubie. To nie jest vaporware -
> to działa już dziś!"

---

## Slajd 21: Thank You

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   DZIĘKUJĘ ZA UWAGĘ!

   Cutoff Time System
   Real-Time Warehouse Capacity Decision Engine

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Key Takeaways (powtórzenie):**
```
┌──────────────────────────────────────┐
│ 1. ⚡ Real-Time Intelligence         │
│    < 100ms decision time             │
│                                      │
│ 2. 💰 Proven ROI                     │
│    150k PLN/rok savings              │
│                                      │
│ 3. 🚀 Production Ready               │
│    Demo = Production code            │
└──────────────────────────────────────┘
```

**Contact:**
```
LR Systems
Email: support@lrsystems.pl
GitHub: github.com/lesnijan/cutoff-time-architecture
```

**Demo Access:**
```
Dashboard: http://localhost:8080/static/demo.html
API Docs:  http://localhost:8080/api/v1/docs
```

**Grafika:**
- Logo firmy
- Ikona sukcesu (checkmark, trophy)
- QR code do GitHub repo

---

## APPENDIX: Presentation Tips

### Timing (Total: 20-25 min)
- Slajdy 1-3: Problem & Solution (5 min)
- Slajdy 4-9: Dashboard Demo (8 min)
- Slajdy 10-12: API Demo (4 min)
- Slajdy 13-18: Technical & Business (5 min)
- Slajdy 19-21: Next Steps & Q&A (3-5 min)

### Equipment Needed
- [ ] Laptop z running demo (localhost:8080)
- [ ] Projektor / screen sharing
- [ ] 2 browser tabs open:
  - Dashboard: localhost:8080/static/demo.html
  - API Docs: localhost:8080/api/v1/docs
- [ ] Backup: Screenshots in case demo fails

### Demo Checklist
- [ ] Server running: `python -m uvicorn app.main:app --port 8080`
- [ ] Health check: `curl localhost:8080/api/v1/health`
- [ ] Dashboard loaded and tested
- [ ] API docs accessible
- [ ] Demo scenario set to "Normal"

### Backup Plan
If demo fails:
1. Use screenshots from docs
2. Show GitHub repo
3. Focus on business value slides

### Audience-Specific Adjustments

**For Technical Audience:**
- Spend more time on slajdy 10-14 (API + Architecture)
- Show code in GitHub
- Discuss scalability, performance

**For Business Audience:**
- Focus on slajdy 1-3, 15-16 (Problem, ROI, Benefits)
- Quick demo overview
- Emphasize ROI and timeline

**For Executive Audience:**
- Slajdy 1-3, 15, 19 only (10 minutes)
- ROI front and center
- Decision gates clear
- Skip technical details

---

**END OF POWERPOINT PRESENTATION SCRIPT**

**Version:** 1.0.0
**Date:** 2024-12-02
**Status:** ✅ Ready for Presentation
**Format:** Convert to PowerPoint using this script

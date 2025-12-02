# ⚡ Quick Start - 2 Minutes

## 🚀 Start Demo in 3 Commands

```bash
# 1. Zainstaluj zależności
poetry install

# 2. Uruchom serwer
poetry run uvicorn app.main:app --reload --port 8080

# 3. Otwórz przeglądarkę
http://localhost:8080/static/demo.html
```

## ✨ That's It!

- ✅ **No configuration** - działa od razu
- ✅ **No database** - używa mock data
- ✅ **No setup** - wszystko gotowe

---

## 🎮 What to Try

### 1. Dashboard
Open: http://localhost:8080/static/demo.html
- Zobacz aktualny stan magazynu
- Sprawdź utilization (domyślnie 70%)

### 2. Test Capacity
W dashboardzie:
- Wybierz product: **MAT-001**
- Quantity: **10**
- Kliknij **"Check Capacity"**
- **Result**: ✓ Order accepted

### 3. Switch Scenario
- Kliknij **"High Utilization"**
- Zobacz jak utilization rośnie do 90%
- Spróbuj znów tego samego zamówienia
- **Result**: ✗ Order rejected

### 4. VIP Override
- Zmień Priority na **"VIP"**
- Spróbuj ponownie
- **Result**: ✓ Order accepted (VIP reserve!)

---

## 📚 More Info

- **Full Demo Guide**: [DEMO.md](DEMO.md)
- **Complete Summary**: [DEMO-SUMMARY.md](DEMO-SUMMARY.md)
- **API Docs**: http://localhost:8080/api/v1/docs

---

## 🐛 Problems?

### Poetry not found?
```bash
pip install poetry
```

### Port 8080 in use?
```bash
# Use different port
poetry run uvicorn app.main:app --port 8000
```

### Browser shows error?
- Check terminal - API must be running
- Try: http://localhost:8080/api/v1/health

---

**That's all you need!** 🎉

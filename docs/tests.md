# Test-Dokumentation

## Übersicht

Dieses Dokument beschreibt die Teststrategie des Fitnesscenter-Management-Systems.

Ziel ist es, die wichtigsten Komponenten des Systems isoliert sowie im Zusammenspiel zu testen.

---

## Teststruktur

### Unit Tests

**Ziel:**  
Einzelne Komponenten isoliert testen (ohne externe Abhängigkeiten)

**Speicherort:**
- `tests/unit/test_domain.py`
- `tests/test_product.py`
- `tests/test_member.py`

### Getestete Komponenten

#### Domain-Modelle
- `Product`
- `Member`
- `Employee`
- `Equipment`
- `VendingMachine`
- `Movement`

Typische Tests:
- Erstellung von Objekten
- Validierungen (z. B. leere Felder, negative Werte)
- Methodenlogik (z. B. Bestandsänderung)

---

### Integration Tests

**Ziel:**  
Zusammenspiel mehrerer Komponenten testen (Service + Repository)

**Speicherort:**
- `tests/integration/test_integration.py`
- `test_supabase.py`

Getestet wird:
- vollständige Workflows (Produkt erstellen → Bestand ändern → Report)
- Datenfluss zwischen Service und Repository
- grundlegende Supabase-Anbindung

---

## Test-Ausführung

### Alle Tests
```bash
pytest
```

### Unit Tests
```bash
pytest tests/unit/ -v
```

### Integration Tests
```bash
pytest tests/integration/ -v
```

### Mit Coverage
```bash
pytest --cov=src tests/
```

---

## Teststrategie

Das Projekt verwendet folgende Testansätze:

### 1. Isolierte Tests (Unit Tests)
- Fokus auf Domain-Logik
- Keine Datenbankverbindung
- Nutzung von In-Memory-Daten

### 2. Integrationstests
- Verbindung von Service und Repository
- Test von realistischen Use-Cases

### 3. Manuelle Tests (GUI)
- GUI wird aktuell manuell getestet
- Fokus auf:
  - Navigation
  - Dialoge
  - Datenanzeige

---

## Testdaten

Beispiel für Testdaten:

```python
service.create_product(
    product_id="P001",
    name="Protein Shake",
    description="Fitness Getränk",
    price=4.99,
    category="Getränke",
    initial_quantity=10,
)
```

---

## Mocking / Testadapter

Für Unit Tests werden keine echten Datenbanken verwendet.

Stattdessen:
- In-Memory Repository
- einfache Testdaten

Ziel:
- schnelle Tests
- keine externen Abhängigkeiten

---

## Aktueller Stand

### Bereits umgesetzt
- Basis-Unit-Tests für Domain-Modelle
- einfache Integrationstests
- Tests für Produkt- und Member-Funktionalität

### Noch offen
- vollständige Testabdeckung aller Services
- detaillierte Integrationstests für alle Module
- automatisierte GUI-Tests (optional)

---

## Bekannte Einschränkungen

- Keine vollständige Testabdeckung
- Supabase-Tests abhängig von externer Konfiguration (.env)
- GUI nur manuell getestet

---

**Letzte Aktualisierung:** 2026-04-23

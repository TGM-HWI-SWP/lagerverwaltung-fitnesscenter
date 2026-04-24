# Changelog - [Jovan Vitorovic]

Persönliches Changelog für [Jovan Vitorovic], Rolle: [Rolle 2 Businesslogik und Datenbank]

---

## [v0.1] - 2026-03-13

### Implementiert
- Supabase Repository Support hinzugefügt
- Supabase Repository Adapter implementiert
- Erste Testdaten mit Supabase integriert
- Member Domain Model erstellt
- Allgemeine Code-Anpassungen durchgeführt

### Tests geschrieben
- Erste Testdaten-Integration (Supabase)

### Commits
```
- 1218016 Feat: Add Supabase repository support
- 7e1b5975 Feat: Add Supabase repository adapter
- 06351878 Test: First Test Data input with Supabase
- 9e2cc411 Feat: Add member domain model
- 5d59851f Refactor: Effective changemnet of some files
```

### Mergekonflikt(e)
- Keine

---

## [v0.2] - 2026-03-20

### Implementiert
- Repository- und Service-Refactoring für neue Role1-Architektur
- Struktur für Repositories und Services erweitert


### Tests geschrieben
- Test für Member-Tabelle erstellt

### Commits
```
- 70041d00 Refactor: Refactor repositories and service to new role1 architecture
- 2158f061 Feat: Creating changes for the repository and services
- 66767c0e Test: Test file for member Table
```

### Mergekonflikt(e)
- Keine

---

## [v0.3] - 2026-03-27

### Implementiert
- Report A (Lagerbestandsbericht) implementiert
- ConsoleReportAdapter implementiert
- Report-Generierung in Service integriert (generate_inventory_report)
- Report zeigt Produktname, Kategorie, Bestand, Preis und Gesamtwert
- Gesamtwert des gesamten Lagers wird berechnet

### Tests geschrieben
- Test für den Report A geschrieben

### Commits
```
- bf4bdec6 Report A implemented. Waiting for Role 1 domain and ports to run tests.
```

### Mergekonflikt(e)
- Keine

---

## [v0.4] - 2026-04-17

### Implementiert
- Service Layer (Business Logic) weiterentwickelt und überprüft
- Lagerlogik (add_stock, remove_stock) finalisiert
- Movement-System getestet (automatische Erstellung bei Lagerbewegungen)
- Report A funktional integriert

### Datenbank

- Supabase-Datenbank bereinigt (alle alten Datensätze gelöscht)
- Neue Daten für folgende Tabellen erstellt und eingefügt:
- Equipment
- Vending Machines
- Movements
- Members
- Products
- Employees

### Tests geschrieben
- Unit-Tests für Produkt- und Lagerfunktionen erstellt
- Teststruktur in mehrere Dateien aufgeteilt (z. B. test_product.py)
- Testumgebung mit InMemory Repository weiter vorbereitet

### Sonstiges
- Fehleranalyse bei fehlenden Domain-Dateien (Rolle 1)
- Workaround für Tests dokumentiert

### Commits
```
- Keine
```

### Mergekonflikt(e)
- Keine

---

## [v0.5] - 2026-04-20

### Implementiert
- Fertigstellung von Report A (Lagerbestandsbericht)
- Anpassungen an der Adapter-Struktur (__init__.py) zur Fehlerbehebung

### Tests geschrieben
- Testskript für Report A erstellt (test_inventory_report.py)
- Funktionalität des Lagerberichts erfolgreich überprüft

### Commits
```
- Adding some changes to the init file in the adapters folder
- Finishing report A
```

### Mergekonflikt(e)
- Keine

---

## [v1.0] - 2026-04-22

### Implementiert
- Report A (Lagerbestandsbericht) mit Supabase umgesetzt
- Verbindung zwischen Business Logic und Supabase Repository getestet
- Ausgabe des Lagerbestands über echtes Datenbanksystem

### Tests geschrieben
- Test-Script für Report A mit Supabase erstellt und ausgeführt

### Commits
```
- Creating the Report A for the products using the supabase Repository
```

### Mergekonflikt(e)
- Keine

---

## [v1.1] - 2026-04-23

### Implementiert
- Finalisierung von Report A (Inventory Report mit Supabase-Daten)
- Integration der Supabase Repositories in den Service Layer
- Erweiterung der Test-Skripte:
  - test_supabase.py
  - test_member.py
  - test_inventory_report.py
- Anpassung und Finalisierung bestehender Tests:
  - test_domain.py (Unit Tests)
  - test_integration.py (Integration Tests)
- Pytest Ergänzung
- Ergänzung von Docstrings in Test-Dateien und Scripts
- Überarbeitung und Finalisierung der README-Dokumentation (inkl. korrekter Testbefehle)

### Tests geschrieben
- Ausführung von Unit Tests (test_domain.py)
- Ausführung von Integration Tests (test_integration.py)
- Alle Tests erfolgreich bestanden (15/15)
- Test der Supabase-Anbindung (Speichern und Laden von Daten)
- Test der Report-Funktionalität (Inventory Report)
- Testen von allen Test Dateien die ich erstellt habe inklusive eben pytest von dem ganzen

### Commits
```
- b4c94f1b - Adding the test commands for pytest to the README
- 9760bf7f - docs: add comprehensive docstrings to tests and scripts; test: implement and validate unit and integration tests ; feat: finalize Report A and Supabase integration
- 7ffb8084 - Adding some changes
- 84abb051 - Changing the pyproject toml and adding some necessary changes
- e62df99e - Including the env file with the URL and KEY from SUPABASE and changing the gitignore file
```

### Mergekonflikt(e)
- Keine

---

## Zusammenfassung

**Gesamt implementierte Features:** 12  
**Gesamt geschriebene Tests:** 8  
**Gesamt Commits:** 14  
**Größte Herausforderung:** Integration der Supabase-Datenbank in die bestehende Port-Adapter-Architektur sowie das Abstimmen der Businesslogik mit den Domain- und Repository-Strukturen anderer Rollen  
**Schönste Code-Zeile:** `report = service.generate_inventory_report()`

---

**Changelog erstellt von:** Jovan Vitorovic  
**Letzte Aktualisierung:** 2026-04-23

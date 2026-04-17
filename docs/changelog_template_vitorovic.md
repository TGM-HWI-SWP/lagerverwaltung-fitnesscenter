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
- [Datei]: [Kurzbeschreibung und Lösung]

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
- [Konflikte, falls vorhanden]

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
- [Commits]
```

### Mergekonflikt(e)
- [Konflikte]

---

## [v0.5] - [Datum]

### Implementiert
- [Feature/Fix]

### Tests geschrieben
- [Tests]

### Commits
```
- [Commits]
```

### Mergekonflikt(e)
- [Konflikte]

---

## [v1.0] - [Datum]

### Implementiert
- [Feature/Fix]

### Tests geschrieben
- [Tests]

### Commits
```
- [Commits]
```

### Mergekonflikt(e)
- [Konflikte]

---

## Zusammenfassung

**Gesamt implementierte Features:** [Anzahl]  
**Gesamt geschriebene Tests:** [Anzahl]  
**Gesamt Commits:** [Anzahl]  
**Größte Herausforderung:** [Beschreibung]  
**Schönste Code-Zeile:** [Code-Snippet]

---

**Changelog erstellt von:** [Name]  
**Letzte Aktualisierung:** [Datum]

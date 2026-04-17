# Changelog - [Ivan Strainovic]

Persönliches Changelog für [Ivan Strainovic], Rolle: [Projektverantwortung & Schnittstellen (Contract Owner) ]

---

## [v0.1] - 2026-03-13

### Implementiert
- Refactoring der Contracts auf Fitnesscenter-Domain
- Definition erster Repository Ports (Member, Membership, Check-in)
- Erstellung Service Contracts für Core Use-Cases
- Einführung Report Port (Member Overview)

### Tests geschrieben
- Keine

### Commits
```
- f5b3ccb Refactor: contracts from warehouse to fitnesscenter domain
- 6e350c5 Feat: add repository ports for members, memberships, check-ins
- 8e86665 Feat: add service contract for core fitnesscenter use cases
- 6402053 Feat: add report port and remove old dependency
- 68a5841 Docs: update contract version history
```


### Mergekonflikt(e)
- Keine

---

## [v0.2] - 2026-03-13

### Implementiert
- Erweiterung aller Repository Contracts für Inventory System
- Service Contracts für Fitnesscenter vollständig definiert
- Report Contracts für Inventory & Equipment ergänzt

### Tests geschrieben
- Keine

### Commits
```
- d7a024d Feat: update repository contracts for fitnesscenter inventory system
- 0609555 Feat: update service contracts for fitnesscenter management system
- a711d69 Feat: update report contracts for inventory and equipment
```


### Mergekonflikt(e)
- Keine

---

## [v0.3] - 2026-03-13

### Implementiert
- Erstellung aller spezifischen Repository Ports:
- Product
- Movement
- Employee
- Equipment
- VendingMachine
- Finale Version der Contracts Dokumentation

### Tests geschrieben
- Keine

### Commits
```
- f7e16e7 Feat: add product repository port
- 2c99c71 Feat: add movement repository port
- 79fa252 Feat: add employee repository port
- e57af5d Feat: add equipment repository port
- 6e2b060 Feat: add vending machine repository port
- e230de7 Docs: finalize contracts architecture documentation
```

### Mergekonflikt(e)
- Keine

---

## [v0.4] - 2026-03-13

### Implementiert
- Implementierung aller Domain-Modelle mit Validierung und Verhalten:
- Member
- Employee
- Equipment
- VendingMachine
- Erweiterung Domain um vollständige Fitnesscenter-Struktur

### Tests geschrieben
- Keine

### Commits
```
- a5f33f3 Feat: implement member domain model with validation and behavior
- df36631 Feat: implement employee domain model with validation and behavior
- 2dd0e30 Feat: implement equipment domain model with validation and status handling
- 9b6d7e2 Feat: implement vending machine domain model with validation and assignment
```

### Mergekonflikt(e)
- Keine

---

## [v0.5] - 2026-03-20

### Implementiert
- Anpassung der Contracts an aktuelle Domain- und Service-Struktur
- Vollständige Architektur-Dokumentation (Hexagonal Architecture)
- Umstellung von Warehouse → Fitnesscenter abgeschlossen

### Tests geschrieben
- Keine

### Commits
```
- 6f891ab Docs: align contracts with domain and service structure
- 32dddc5 Docs: update architecture to fitness center (hexagonal architecture)
```

### Mergekonflikt(e)
- Keine

---

## [v0.3] - 2026-04-17

### Implementiert
- Controller-Schicht erstellt:
  - MemberController
  - EmployeeController
  - ProductController
  - EquipmentController
  - VendingMachineController
- Verbindung Controller ↔ Service vorbereitet
- Projekt auf aktuellen Stand von `main` gebracht

### Tests geschrieben
- Keine

### Commits

### Mergekonflikt(e)
- `src/domain/member.py`: Konflikt zwischen `id` und `member_id` sowie Zeitstempel (`datetime.now` vs `datetime.utcnow`) beim Merge gelöst. Einheitlich auf `member_id` und `datetime.utcnow` angepasst.

---

## Zusammenfassung

**Gesamt implementierte Features:** 15+  
**Gesamt geschriebene Tests:** 0  
**Gesamt Commits:** ~20  
**Größte Herausforderung:** Umstellung der gesamten Architektur von Warehouse auf Fitnesscenter + saubere Trennung Domain / Ports / Services  
**Schönste Code-Zeile:**  
```python
#class MemberRepositoryPort(ABC):

---

**Changelog erstellt von:** [Ivan Strainovic]  
**Letzte Aktualisierung:** [20.03.2026]

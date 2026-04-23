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

## [v0.6] - 2026-03-27

### Implementiert
- Erste Implementierung der Controller-Schicht:
  - MemberController
  - EmployeeController
  - ProductController
  - EquipmentController
  - VendingMachineController
- Erweiterung der GUI:
  - Produktseite mit Filter, Suche und Dialogen
- Vorbereitung der Verbindung GUI ↔ Controller

### Tests geschrieben
- Keine

### Commits
```
129944d feat(controller): add member controller
a7e736e feat(controller): add employee controller
b81e817c feat(controller): add product controller
2d158b09 feat(controller): add equipment controller
7f894bff feat(controller): add vending machine controller
1a0ecda Feat: GUI erweitert um Produkte-Seite mit Filter, Suche und Dialogen
bf4bdec Report A implemented. Waiting for Role 1 domain and ports to run tests
```

### Mergekonflikt(e)
- Keine

---

## [v0.7] - 2026-04-10

### Implementiert
- Erweiterung der Controller-Schicht:
  - MovementController hinzugefügt
  - ReportController hinzugefügt
- Strukturierung des controllers-Pakets (__init__ ergänzt)
- Anpassung der Controller für bessere Integration mit Service Layer

### Tests geschrieben
- Keine

### Commits
```
c7671094 feat(controller): add report controller
4f57633d feat(controller): add movement controller
97479f04 feat(controller): add controllers package init
```

### Mergekonflikt(e)
- Keine

---

## [v0.8] - 2026-04-17

### Implementiert
- Vollständige Controller-Schicht implementiert:
  - MemberController
  - EmployeeController
  - ProductController
  - EquipmentController
  - VendingMachineController
  - MovementController
  - ReportController
- Anbindung Controller ↔ Service vorbereitet
- Einheitliche Schnittstelle für UI geschaffen
- Projektstand mit `main` synchronisiert

### Tests geschrieben
- Keine

### Commits
```
ae568b1 feat(controller): align product controller with service layer
```

### Mergekonflikt(e)
- `src/domain/member.py`: Konflikt zwischen `id` und `member_id` sowie Zeitstempel (`datetime.now` vs `datetime.utcnow`) beim Merge gelöst. Einheitlich auf `member_id` und `datetime.utcnow` angepasst.

---

## [v0.9] - 2026-04-21

### Implementiert
- Erweiterung der Service-Schicht:
  - Update-Funktionalität für Member, Employee und Product
  - Delete-Funktionalität für Product, Equipment und VendingMachine
- Erweiterung der Repository-Ports:
  - Delete-Methoden für Equipment und VendingMachine ergänzt
- Erweiterung der Controller:
  - Unterstützung für Update- und Delete-Operationen
  - Integration von Stock-Management (add_stock / remove_stock)
- Anpassung der Domain-Modelle auf finale Struktur überprüft
- Vorbereitung der vollständigen Integration mit GUI (Role 4)

### Tests geschrieben
- Keine

### Commits
```
0df7064 feat: Controller & Service Integration vorbereitet
ae568b1 feat(controller): align product controller with service layer
834f63f docs(changelog): update changelog for controller implementation and merge
```

### Mergekonflikt(e)
- Keine

---

## [v0.10] - 2026-04-23

### Implementiert
- Überarbeitung der Dokumentation:
  - README.md vollständig an Fitnesscenter-System angepasst
  - architecture.md finalisiert (Controller + Supabase integriert)
  - contracts.md an aktuellen Service-Stand angepasst
  - tests.md aktualisiert (Teststruktur angepasst)
  - known_issues.md überarbeitet (realer Projektstatus ergänzt)
  - retrospective.md ausgefüllt und aktualisiert
- Neue Dokumente erstellt:
  - CHECKLISTE_fitnesscenter.md (Projektstatus)
  - Peer_Feedback_Strainovic.md
- Vereinheitlichung der gesamten Dokumentationsstruktur
- Anpassung aller Inhalte von Vorlage → reales Projekt (Fitnesscenter)

### Tests geschrieben
- Keine

### Commits
```
Docs: update README to fitnesscenter version
Docs: finalize architecture documentation
Docs: update contracts to match service layer
Docs: adjust tests documentation
Docs: update known issues
Docs: complete retrospective
Docs: add project checklist
Docs: add peer feedback
```

### Mergekonflikt(e)
- Keine

---

## Zusammenfassung

**Gesamt implementierte Features:** ~20  
**Gesamt geschriebene Tests:** 0  
**Gesamt Commits:** ~30 
**Größte Herausforderung:** Umstellung der gesamten Architektur von Warehouse auf Fitnesscenter + saubere Trennung Domain / Ports / Services  
**Schönste Code-Zeile:**  
```python
#class MemberRepositoryPort(ABC):

---

**Changelog erstellt von:** [Ivan Strainovic]  
**Letzte Aktualisierung:** [23.04.2026]

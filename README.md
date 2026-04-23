[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Pc_A4vY0)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22780668&assignment_repo_type=AssignmentRepo)

# Fitnesscenter Management System

Vollständiges Softwareentwicklungsprojekt für die Verwaltung eines Fitnesscenters.  
Das System basiert auf einer **Hexagonalen Architektur (Port-Adapter / Hexagonal Architecture)** und kombiniert:

- Businesslogik
- Datenbankanbindung über Supabase
- moderne GUI mit PyQt6
- strukturierte Dokumentation
- Tests und Projektmanagement-Artefakte


## Projektüberblick

- **Projektdauer:** 8 Wochen
- **Unterricht:** 2 UE pro Woche
- **Gruppengröße:** 3er Gruppe
- **Ziel:** Professionelle Softwareentwicklung und Projektmanagement
- **Projekttyp:** Softwareentwicklungs- und Projektmanagementprojekt
- **Ziel:** Entwicklung eines modularen Fitnesscenter-Management-Systems
- **Architektur:** Port-Adapter-Architektur (Hexagonal Architecture)
- **GUI-Technologie:** PyQt6
- **Persistenz:** Supabase
- **Gruppengröße:** 3er-/4er-Gruppe

---

## Features

Das System unterstützt aktuell folgende Kernbereiche:

- **Mitgliederverwaltung**
- **Mitarbeiterverwaltung**
- **Produktverwaltung**
- **Lager- und Bestandsverwaltung**
- **Lagerbewegungen (IN / OUT)**
- **Geräteverwaltung**
- **Verkaufsautomaten (Vending Machines)**
- **Reporting**
- **Authentifizierung / Login**
- **Dokumentation & Changelogs**

---

## Projektstruktur

```text
LAGERVERWALTUNG-FITNESSCENTER/
├── docs/
│   ├── architecture.md
│   ├── changelog_Ristic.md
│   ├── changelog_strainovic.md
│   ├── changelog_template_vitorovic.md
│   ├── changelog_template.md
│   ├── contracts.md
│   ├── DATACLASS_ERKLAERT.md
│   ├── known_issues.md
│   ├── retrospective.md
│   └── tests.md
│
├── src/
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── report.py
│   │   ├── repository.py
│   │   └── supabase_repository.py
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   ├── employee_controller.py
│   │   ├── equipment_controller.py
│   │   ├── member_controller.py
│   │   ├── movement_controller.py
│   │   ├── product_controller.py
│   │   ├── report_controller.py
│   │   └── vending_machine_controller.py
│   │
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── employee.py
│   │   ├── equipment.py
│   │   ├── member.py
│   │   ├── product.py
│   │   ├── vending_machine.py
│   │   └── warehouse.py
│   │
│   ├── ports/
│   │   ├── __init__.py
│   │   ├── checkin_repository_port.py
│   │   ├── employee_repository_port.py
│   │   ├── equipment_repository_port.py
│   │   ├── member_repository_port.py
│   │   ├── membership_repository_port.py
│   │   ├── movement_repository_port.py
│   │   ├── product_repository_port.py
│   │   ├── report_port.py
│   │   └── vending_machine_repository_port.py
│   │
│   ├── reports/
│   │   └── __init__.py
│   │
│   ├── services/
│   │   └── __init__.py
│   │
│   ├── ui/
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── login_window.py
│   │   │   ├── session.json
│   │   │   └── users.json
│   │   │
│   │   ├── dialogs/
│   │   ├── pages/
│   │   │   ├── dashboard_page.py
│   │   │   ├── employees_page.py
│   │   │   ├── equipment_page.py
│   │   │   ├── members_page.py
│   │   │   ├── movements_page.py
│   │   │   ├── products_page.py
│   │   │   ├── reports_page.py
│   │   │   └── vending_page.py
│   │   │
│   │   ├── styles/
│   │   │   ├── auth.qss
│   │   │   └── main.qss
│   │   │
│   │   ├── tables/
│   │   │   └── inventory_table.py
│   │   │
│   │   ├── widgets/
│   │   │   ├── animated_stack.py
│   │   │   ├── sidebar.py
│   │   │   └── stat_card.py
│   │   │
│   │   ├── __init__.py
│   │   └── main_window.py
│   │
│   ├── __init__.py
│   └── main.py
│
├── tests/
│   ├── integration/
│   │   └── test_integration.py
│   ├── unit/
│   │   └── test_domain.py
│   ├── conftest.py
│   └── test_product.py
│
├── .env
├── .flake8
├── .gitignore
├── .pylintrc
├── CHECKLISTE.md
├── GIT_WORKFLOW.md
├── INDEX.md
├── pyproject.toml
├── README.md
├── report_supabase.py
├── TEMPLATE_INFO.md
├── test_inventory_report.py
├── test_member.py
└── test_supabase.py
```
---

## Installation & Setup

### Voraussetzungen
- Python 3.10 oder höher
- pip
- Git
- Supabase-Projekt mit gültigen Zugangsdaten

### Entwicklungsumgebung aufbauen

```bash
# 1. Repository klonen
git clone <repository-url>
cd lagerverwaltung-fitnesscenter

# 2. Virtuelle Umgebung erstellen
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / Mac
source .venv/bin/activate

# 3. Dependencies installieren
pip install -e .
pip install -e ".[dev]"

# 4. Tests ausführen
pytest

# 5. Environment Variablen
Für die Supabase-Anbindung wird eine `.env` Datei benötigt.

Beispiel:
SUPABASE_URL=deine_supabase_url
SUPABASE_KEY=dein_supabase_key

Ohne diese Werte kann die Anwendung mit Supabase-Repositories nicht korrekt starten.

# 6. GUI starten
python -m src.main
```
---

## Architektur

UI → Controller → Service → Repository Port → Repository Adapter → Datenbank
Das Projekt folgt der **Port-Adapter-Architektur** (auch Hexagonal Architecture genannt):


### Schichten im Überblick

- **Domain Layer:**  
  Enthält die fachlichen Kernobjekte wie `Member`, `Employee`, `Product`, `Equipment`, `VendingMachine` und `Movement`.

- **Ports:**  
  Definieren Schnittstellen für Datenzugriffe und Reports.

- **Adapters:**  
  Implementieren die Ports konkret, z. B.:
  - In-Memory-Repositories  
  - Supabase-Repositories  
  - Report-Adapter  

- **Services:**  
  Enthalten die Businesslogik und Use Cases des Systems.

- **Controllers:**  
  Vermitteln zwischen GUI und Service Layer.

- **UI:**  
  PyQt6-basierte Oberfläche mit Pages, Dialogen, Widgets und Stylesheets.

### Vorteile dieser Architektur

- **Testbarkeit:**  
  Klare Trennung der Verantwortlichkeiten ermöglicht einfaches Testen

- **Austauschbarkeit:**  
  Datenquellen können leicht ersetzt werden (z. B. In-Memory ↔ Datenbank)

- **Wartbarkeit:**  
  Gute Struktur erleichtert Erweiterung und Pflege

---

## Rollenvergabe (3er-Gruppe)

### Rolle 1 – Projektverantwortung & Schnittstellen (Contract Owner)
- Projektkoordination  
- Definition und Pflege der Schnittstellen  
- Architektur und Dokumentation  
- Unterstützung bei Mergekonflikten  
- Domain-Modelle und Controller  

### Rolle 2 – Businesslogik & Persistenz
- Service Layer  
- Datenbankanbindung  
- Repository-Implementierungen  
- Report-Logik  

### Rolle 3 / 4 – GUI & Interaktion
- Aufbau der Benutzeroberfläche  
- Dialoge, Tabellen und Navigation  
- Styling mit QSS  
- Anbindung an Controller und Service  

---

## Entwicklungsablauf

### Versionsmeilensteine
- **v0.1** – Projektstart, Rollen, erste Contracts  
- **v0.2** – Architektur & Walking Skeleton  
- **v0.3** – Kernstrukturen & Domain  
- **v0.4** – Erweiterung Domain / Ports / Architektur  
- **v0.5** – Architektur-Anpassung auf Fitnesscenter  
- **v0.6** – erste Controller  
- **v0.7** – zusätzliche Controller  
- **v0.8** – Controller-/Service-Integration  
- **v0.9** – finale Backend-Vorbereitung für GUI-Anbindung  

### Git-Workflow

```bash
# Feature-Branch erstellen
git checkout -b feature/<rollenname>/<feature>

# Änderungen committen
git commit -m "Feat: Beschreibung"
git commit -m "Fix: Bugfix-Beschreibung"
git commit -m "Docs: Dokumentation"
git commit -m "Test: Testcode"

# Branch pushen
git push origin feature/<rollenname>/<feature>
# Pull Request erstellen → Review → Merge
```

### Dokumentation der Versionen

Jedes Gruppen mitglied führt: `docs/changelog_<name>.md`
Bsp.: docs/changelog_strainovic.md

Beispiel-Format:
```markdown
## [0.2] - 2025-02-06

### Implementiert
- Warehouse Service erstellt
- Produktklasse mit Validierung

### Tests
- test_product_creation
- test_update_quantity

### Commits
- abc1234 Feat: Warehouse Service
- def5678 Test: Product Tests
```

---

## Testing

### Alle Tests

```bash
pytest
```

### Unit Tests ausführen

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

## Reports

Aktuell ist insbesondere ein Inventory Report vorgesehen.

Reports sollen:
- auf echten Daten basieren
- deterministisch sein
- testbar bleiben
- unabhängig von der GUI funktionieren

Beispielhafte Nutzung:

### Produkt erstellen:
```python
from src.services import FitnessCenterService

product = service.create_product(
    product_id="P001",
    name="Protein Shake",
    description="Getränk für Fitnessstudio",
    price=4.99,
    category="Getränke",
    initial_quantity=10,
)
```

### Bestand erhöhen:
```python
service.add_stock("P001", 5, reason="Neue Lieferung", user="system")
```

### Bestand verringern:
```python
service.remove_stock("P001", 2, reason="Verkauf", user="system")
```

### Inventory Report erzeugen:
```python
report = service.generate_inventory_report()
print(report)
```

---

## Bekannte Punkte / aktueller Stand

Der Projektstand ist weit fortgeschritten, jedoch noch nicht in allen Bereichen final integriert.

### Aktuell fertig / weitgehend fertig
- Domain-Modelle
- Ports
- Service Layer
- Repository Adapter
- Controller Layer
- die GUI-Struktur
- vollständige GUI-Anbindung an Controller und Service
- Bereinigung verbleibender Demo-Daten in einzelnen UI-Seiten
- finale End-to-End-Tests

#### Weitere Hinweise siehe:

- docs/known_issues.md
- docs/tests.md
- docs/retrospective.md

---

## Projektmanagement-Dokumente

### Im separaten PDF befinden sich unter anderem:

1. **Projektcharta**
   - Ziel & Nicht-Ziele
   - Stakeholder
   - Risiken

2. **Vorgehensmodell**
   - Beschreibung (iterativ / Scrum-light)
   - Begründung

3. **Projektstrukturplan (PSP)**
   - Gliederung der Projektarbeit

4. **Gantt-Diagramm**
   - Zeitliche Planung über 8 Wochen

5. **Rollenverteilung**
   - Aufgaben pro Rolle


### Im Ordner docs/ befinden sich unter anderem:
- Architektur-Dokumentation
- Contracts
- Tests-Dokumentation
- Retrospektive
- persönliche Changelogs

Zusätzliche Projektübersichten:

- CHECKLISTE.md
- GIT_WORKFLOW.md
- INDEX.md

---

## Versionierung

### Version Format
```
MAJOR.MINOR.PATCH
0.1.0
```

### Tags im Repository
```bash
git tag -a v0.1 -m "v0.1 - Projektstart"
git push origin v0.1
```

---

## Known Issues

Siehe `docs/known_issues.md`

---

## Lizenz

Schulprojekt - TGM

---

## Kontakt

Projektverantwortung: Ivan Strainovic - Rolle 1 (Contract Owner)

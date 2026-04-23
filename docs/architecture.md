# Architektur-Dokumentation

## Architektur-Übersicht

Das Projekt folgt der **Port-Adapter-Architektur** (Hexagonal Architecture), um eine klare Trennung zwischen GUI, Businesslogik und Datenpersistenz zu erreichen.

Ziele dieser Architektur:

- hohe Testbarkeit
- klare Verantwortlichkeiten
- austauschbare Datenzugriffe
- gute Wartbarkeit und Erweiterbarkeit

---

## Schichten-Modell

```text
┌──────────────────────────────────────────────────────────────┐
│                         UI-Layer (PyQt6)                    │
│      LoginWindow, MainWindow, Pages, Dialoge, Widgets       │
└───────────────────────────┬──────────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────────┐
│                        Controller-Layer                      │
│ member_controller, product_controller, ...                  │
└───────────────────────────┬──────────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────────┐
│                         Service-Layer                        │
│                 FitnessCenterService                         │
└───────────────────────────┬──────────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────────┐
│                          Domain-Layer                        │
│   Product, Member, Employee, Equipment, VendingMachine,     │
│   Movement                                                   │
└───────────────────────────┬──────────────────────────────────┘
                            │
          ┌─────────────────┴─────────────────┐
          │                                   │
┌─────────▼─────────┐               ┌─────────▼──────────────┐
│ Ports             │               │ Adapters               │
│ (Abstraktion)     │◄─────────────►│ (Implementierungen)    │
│ Repository Ports  │               │ InMemory / Supabase    │
│ Report Contracts  │               │ Report Adapter         │
└───────────────────┘               └────────────────────────┘
```

---

## Komponenten

### 1. Domain Layer (src/domain/)

**Verantwortung:**  
Reine fachliche Modelle und Verhaltenslogik, unabhängig von GUI, Datenbank oder Frameworks.

#### product.py
Klasse: Product

Attribute:
- id
- name
- description
- price
- quantity
- sku
- category
- created_at
- updated_at
- notes

Methoden:
- update_quantity(amount)
- get_total_value()
- is_low_stock()

---

#### warehouse.py

Enthält:
- Movement
- Warehouse

Movement Attribute:
- id
- product_id
- product_name
- quantity_change
- movement_type
- reason
- timestamp
- performed_by

Warehouse:
Verwaltungsklasse für Produkt- und Bewegungsdaten  
dient als ergänzende Struktur für Lagerlogik

---

#### member.py
Klasse: Member

Attribute:
- member_id
- first_name
- last_name
- email
- phone
- membership_type
- active
- created_at

Methoden:
- activate()
- deactivate()
- full_name()

---

#### employee.py
Klasse: Employee

Attribute:
- employee_id
- first_name
- last_name
- role
- email
- phone
- active
- created_at

Methoden:
- activate()
- deactivate()
- full_name()

---

#### equipment.py
Klasse: Equipment

Attribute:
- equipment_id
- name
- equipment_type
- location
- status
- assigned_employee_id
- created_at

Methoden:
- set_status(status)
- assign_employee(employee_id)

---

#### vending_machine.py
Klasse: VendingMachine

Attribute:
- machine_id
- location
- machine_type
- assigned_employee_id
- active
- created_at

Methoden:
- activate()
- deactivate()
- assign_employee(employee_id)

---

### 2. Ports (src/ports/)

**Verantwortung:**  
Abstrakte Schnittstellen für Datenzugriff und Reports.

#### Repository Ports
- ProductRepositoryPort
- MovementRepositoryPort
- MemberRepositoryPort
- EmployeeRepositoryPort
- EquipmentRepositoryPort
- VendingMachineRepositoryPort

#### Typische Methoden
- save_...(entity)
- load_...(id)
- load_all_...()
- delete_...(id)

#### Weitere Ports / Altbestand
- checkin_repository_port.py
- membership_repository_port.py
- report_port.py

---

### 3. Adapters (src/adapters/)

**Verantwortung:**  
Konkrete Implementierungen der Ports.

#### InMemory-Repositories
- InMemoryProductRepository
- InMemoryMovementRepository
- InMemoryMemberRepository
- InMemoryEmployeeRepository
- InMemoryEquipmentRepository
- InMemoryVendingMachineRepository

Eigenschaften:
- Speicherung im RAM
- schnell
- gut für Tests
- keine dauerhafte Persistenz

#### Supabase-Repositories
- SupabaseProductRepository
- SupabaseMovementRepository
- SupabaseMemberRepository
- SupabaseEmployeeRepository
- SupabaseEquipmentRepository
- SupabaseVendingMachineRepository

Eigenschaften:
- Persistenz in Supabase
- produktionsnäher
- benötigt .env

#### Report Adapter
- ConsoleReportAdapter

---

### 4. Services (src/services/)

**Verantwortung:**  
Zentrale Businesslogik und Use Cases.

FitnessCenterService enthält:
- Member, Employee, Product, Equipment, VendingMachine, Movement, Reports

---

### 5. Controller Layer (src/controllers/)

**Verantwortung:**  
Vermittlung zwischen GUI und Service Layer.

Controller:
- member_controller.py
- employee_controller.py
- product_controller.py
- equipment_controller.py
- vending_machine_controller.py
- movement_controller.py
- report_controller.py

---

### 6. UI Layer (src/ui/)

**Verantwortung:**  
Benutzeroberfläche mit PyQt6.

Regeln:
- keine direkte DB
- nur Controller/Service
- keine Businesslogik

---

### 7. Tests (tests/)

- Unit Tests
- Integration Tests

---

### Dependency Injection

```python
service = FitnessCenterService(...)
```

---

### Datenfluss

```
GUI
↓
Controller
↓
Service
↓
Repository Port
↓
Repository Adapter
↓
Datenbank / InMemory
↓
Antwort zurück an GUI
```

---

### Erweiterungen / Roadmap
- GUI vollständig
- Tests erweitern
- Reports
- Rollen
- REST API

---

### Sicherheit
- Validierung
- Fehlerbehandlung
- Trennung

---

### Dokumentation
- docs/contracts.md
- docs/architecture.md
- docs/tests.md
- docs/changelog_<name>.md

---

**Letzte Aktualisierung:** 2026-04-23  
**Version:** 0.9
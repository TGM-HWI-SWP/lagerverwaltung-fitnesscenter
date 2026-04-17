# Architektur-Dokumentation

## Architektur-Übersicht

Das Projekt folgt der **Port-Adapter-Architektur** (Hexagonal Architecture) für maximale Testbarkeit und Wartbarkeit.

## Schichten-Modell

```
┌─────────────────────────────────────────────────────────┐
│                    UI-Layer (PyQt6)                     │
│              WarehouseMainWindow, Dialoge               │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  Service-Layer                          │
│              WarehouseService, BusinessLogic            │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  Domain-Layer                           │
│          Product, Movement, Warehouse (Entities)        │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
┌───────▼────────┐          ┌────────▼──────────┐
│  Ports         │          │   Adapters        │
│  (Abstract)    │          │ (Implementations) │
│                │          │                   │
│RepositoryPort  │◄────────►│InMemoryRepository │
│ReportPort      │          │(sqlite, json, ...)|
└────────────────┘          └───────────────────┘
```

---

## Komponenten

### 1. Domain Layer (`src/domain/`)

**Verantwortung:** Reine Geschäftslogik, unabhängig von technischen Details

#### `product.py`
- Klasse: `Product`
- Attribute: product_id, name, description, price, quantity, category
- Methoden:
  - `update_quantity(amount)`
- Validierung: keine negativen Werte

---

#### `movement.py`
- Klasse: `Movement`
- Attribute: movement_id, product_id, quantity_change, movement_type, timestamp, performed_by

---

#### `member.py`
- Klasse: `Member`
- Attribute: member_id, first_name, last_name, email, phone, membership_type, active, created_at
- Methoden:
  - `activate()`
  - `deactivate()`
  - `full_name()`

---

#### `employee.py`
- Klasse: `Employee`
- Attribute: employee_id, first_name, last_name, role, email, phone, active, created_at
- Methoden:
  - `activate()`
  - `deactivate()`
  - `full_name()`

---

#### `equipment.py`
- Klasse: `Equipment`
- Attribute: equipment_id, name, equipment_type, location, status, assigned_employee_id, created_at
- Methoden:
  - `set_status(status)`
  - `assign_employee(employee_id)`

---

#### `vending_machine.py`
- Klasse: `VendingMachine`
- Attribute: machine_id, location, machine_type, assigned_employee_id, active, created_at
- Methoden:
  - `activate()`
  - `deactivate()`
  - `assign_employee(employee_id)`

---

### 2. Ports (`src/ports/`)

**Verantwortung:** Schnittstellen (Abstraktion)

#### Repository Ports
- `ProductRepositoryPort`
- `MovementRepositoryPort`
- `MemberRepositoryPort`
- `EmployeeRepositoryPort`
- `EquipmentRepositoryPort`
- `VendingMachineRepositoryPort`

#### Typische Methoden
```python
save(...)
load(id)
load_all()
delete(id)
```

---

#### ReportPort
```python
class ReportPort(ABC):
    @abstractmethod
    def generate_inventory_report(self) -> list[dict]: ...

    @abstractmethod
    def generate_equipment_status_report(self) -> list[dict]: ...
```

---

### 3. Adapters (`src/adapters/`)

**Verantwortung:** Implementierungen der Ports

#### Repository Adapter
- `InMemoryProductRepository`
- `InMemoryMemberRepository`
- `InMemoryEmployeeRepository`
- `InMemoryEquipmentRepository`
- `InMemoryVendingMachineRepository`

**Eigenschaften:**
- Speicherung im RAM
- schnell
- keine Persistenz

---

#### Report Adapter
- `ConsoleReportAdapter`

**Funktion:**
- generiert strukturierte Reports

---

### 4. Services (`src/services/`)

**Verantwortung:** Businesslogik

#### `FitnessCenterService`

##### Member
- `create_member(...)`
- `get_member(...)`
- `get_all_members()`
- `activate_member(...)`
- `deactivate_member(...)`

---

##### Employee
- `create_employee(...)`
- `get_all_employees()`

---

##### Product
- `create_product(...)`
- `add_stock(...)`
- `remove_stock(...)`
- `get_all_products()`

---

##### Equipment
- `create_equipment(...)`
- `update_equipment_status(...)`
- `assign_employee_to_equipment(...)`
- `get_all_equipment()`

---

##### VendingMachine
- `create_machine(...)`
- `assign_employee_to_machine(...)`
- `get_all_machines()`

---

##### Movement
- `get_movements()`

---

### 5. UI Layer (`src/ui/`)

**Verantwortung:** GUI (PyQt6)

#### Struktur
- Dashboard
- Members
- Employees
- Products
- Movements
- Equipment
- Vending Machines
- Reports

#### Regeln
- GUI nutzt nur Service
- keine direkte DB-Logik

---

### 6. Tests (`tests/`)

#### Unit Tests
- Domain testen
- Service testen

---

#### Integration Tests
- komplette Workflows

---

### Dependency Injection

```python
product_repo = InMemoryProductRepository()
member_repo = InMemoryMemberRepository()

service = FitnessCenterService(product_repo, member_repo)
```

---

### Datenfluss

```
GUI
 ↓
Service
 ↓
Domain
 ↓
Repository
 ↓
Speicherung
 ↓
Antwort an GUI
```

---

### Erweiterungen (Roadmap)

- Datenbank (SQLite / Supabase)
- REST API
- Export (PDF / CSV)
- Login-System

---

### Sicherheit

- Input-Validierung
- Rollen
- Logging

---

### Dokumentation

- docs/contracts.md
- docs/architecture.md
- docs/tests.md
- docs/changelog_<name>.md

---

**Letzte Aktualisierung:** 2026-03-20  
**Version:** 0.2
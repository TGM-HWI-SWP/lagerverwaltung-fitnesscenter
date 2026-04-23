# Schnittstellen-Dokumentation (Contracts)

## Übersicht

Diese Datei dokumentiert die zentralen Schnittstellen des Projekts **Fitnesscenter Management System**.  
Sie wird von **Rolle 1 (Contract Owner)** gepflegt und bei Änderungen an Architektur, Services, Repositories oder Reports aktualisiert.

Die Contracts definieren, wie die einzelnen Komponenten miteinander kommunizieren:

- GUI
- Controller
- Businesslogik
- Datenpersistenz
- Reports

---

## 1. Zentrale Domänenobjekte

### Product

Repräsentiert ein Produkt im Fitnesscenter (z. B. Snacks, Getränke, Zubehör).

**Attribute:**
- `id: str` - Eindeutige Produkt-ID
- `name: str` - Produktname
- `description: str` - Beschreibung
- `price: float` - Preis pro Einheit
- `quantity: int` - Lagerbestand
- `sku: str` - Lager-/Artikelnummer
- `category: str` - Kategorie
- `created_at: datetime`
- `updated_at: datetime`
- `notes: str | None`

**Methoden:**
- `update_quantity(amount: int) -> None`
- `get_total_value() -> float`
- `is_low_stock() -> bool`

---

### Movement

Repräsentiert eine Lagerbewegung eines Produkts.

**Attribute:**
- `id: str`
- `product_id: str`
- `product_name: str`
- `quantity_change: int`
- `movement_type: str` - z. B. `IN`, `OUT`, `CORRECTION`
- `reason: str | None`
- `timestamp: datetime`
- `performed_by: str`

---

### Member

Repräsentiert ein Mitglied des Fitnesscenters.

**Attribute:**
- `member_id: str`
- `first_name: str`
- `last_name: str`
- `email: str`
- `phone: str`
- `membership_type: str`
- `active: bool`
- `created_at: datetime`

**Methoden:**
- `deactivate() -> None`
- `activate() -> None`
- `full_name() -> str`

---

### Employee

Repräsentiert einen Mitarbeiter des Fitnesscenters.

**Attribute:**
- `employee_id: str`
- `first_name: str`
- `last_name: str`
- `role: str`
- `email: str`
- `phone: str`
- `active: bool`
- `created_at: datetime`

**Methoden:**
- `deactivate() -> None`
- `activate() -> None`
- `full_name() -> str`

---

### Equipment

Repräsentiert ein Fitnessgerät.

**Attribute:**
- `equipment_id: str`
- `name: str`
- `equipment_type: str`
- `location: str`
- `status: str`
- `assigned_employee_id: str`
- `created_at: datetime`

**Methoden:**
- `set_status(status: str) -> None`
- `assign_employee(employee_id: str) -> None`

---

### VendingMachine

Repräsentiert einen Snack- oder Getränkeautomaten.

**Attribute:**
- `machine_id: str`
- `location: str`
- `machine_type: str`
- `assigned_employee_id: str`
- `active: bool`
- `created_at: datetime`

**Methoden:**
- `deactivate() -> None`
- `activate() -> None`
- `assign_employee(employee_id: str) -> None`

---

## 2. RepositoryPorts

RepositoryPorts definieren die Schnittstellen zur Datenpersistenz.

---

### ProductRepositoryPort

Speichert und lädt Produkte.

**Methoden:**
- `save_product(product: Product) -> None`
- `load_product(product_id: str) -> Product | None`
- `load_all_products() -> list[Product]`
- `delete_product(product_id: str) -> None`

---

### MovementRepositoryPort

Speichert Lagerbewegungen.

**Methoden:**
- `save_movement(movement: Movement) -> None`
- `load_movements() -> list[Movement]`

---

### MemberRepositoryPort

Speichert Mitglieder.

**Methoden:**
- `save_member(member: Member) -> None`
- `load_member(member_id: str) -> Member | None`
- `load_all_members() -> list[Member]`
- `delete_member(member_id: str) -> None`

---

### EmployeeRepositoryPort

Speichert Mitarbeiter.

**Methoden:**
- `save_employee(employee: Employee) -> None`
- `load_employee(employee_id: str) -> Employee | None`
- `load_all_employees() -> list[Employee]`
- `delete_employee(employee_id: str) -> None`

---

### EquipmentRepositoryPort

Speichert Fitnessgeräte.

**Methoden:**
- `save_equipment(equipment: Equipment) -> None`
- `load_equipment(equipment_id: str) -> Equipment | None`
- `load_all_equipment() -> list[Equipment]`
- `delete_equipment(equipment_id: str) -> None`

---

### VendingMachineRepositoryPort

Speichert Automaten.

**Methoden:**
- `save_machine(machine: VendingMachine) -> None`
- `load_machine(machine_id: str) -> VendingMachine | None`
- `load_all_machines() -> list[VendingMachine]`
- `delete_machine(machine_id: str) -> None`

---

## 3. FitnessCenterService

Service-Klasse für die zentrale Businesslogik.

### Member Management

- `create_member(member_id: str, first_name: str, last_name: str, email: str, phone: str = "", membership_type: str = "Standard") -> Member`
- `get_member(member_id: str) -> Member | None`
- `get_all_members() -> list[Member]`
- `update_member(member_id: str, first_name: str, last_name: str, email: str, phone: str = "", membership_type: str = "Standard") -> Member`
- `deactivate_member(member_id: str) -> None`
- `activate_member(member_id: str) -> None`

---

### Employee Management

- `create_employee(employee_id: str, first_name: str, last_name: str, role: str, email: str, phone: str = "") -> Employee`
- `get_employee(employee_id: str) -> Employee | None`
- `get_all_employees() -> list[Employee]`
- `update_employee(employee_id: str, first_name: str, last_name: str, role: str, email: str, phone: str = "") -> Employee`
- `deactivate_employee(employee_id: str) -> None`
- `activate_employee(employee_id: str) -> None`

---

### Product Management

- `create_product(product_id: str, name: str, description: str, price: float, category: str = "", initial_quantity: int = 0, sku: str = "", notes: str | None = None) -> Product`
- `get_product(product_id: str) -> Product | None`
- `get_all_products() -> list[Product]`
- `update_product(product_id: str, name: str, description: str, price: float, category: str = "", sku: str = "", notes: str | None = None) -> Product`
- `delete_product(product_id: str) -> None`
- `add_stock(product_id: str, quantity: int, reason: str = "", user: str = "system") -> None`
- `remove_stock(product_id: str, quantity: int, reason: str = "", user: str = "system") -> None`
- `get_total_inventory_value() -> float`

---

### Equipment Management

- `create_equipment(equipment_id: str, name: str, equipment_type: str, location: str, status: str = "available", assigned_employee_id: str = "") -> Equipment`
- `get_equipment(equipment_id: str) -> Equipment | None`
- `get_all_equipment() -> list[Equipment]`
- `update_equipment_status(equipment_id: str, status: str) -> None`
- `assign_employee_to_equipment(equipment_id: str, employee_id: str) -> None`
- `delete_equipment(equipment_id: str) -> None`

---

### Vending Machine Management

- `create_machine(machine_id: str, location: str, machine_type: str, assigned_employee_id: str = "") -> VendingMachine`
- `get_machine(machine_id: str) -> VendingMachine | None`
- `get_all_machines() -> list[VendingMachine]`
- `assign_employee_to_machine(machine_id: str, employee_id: str) -> None`
- `activate_machine(machine_id: str) -> None`
- `deactivate_machine(machine_id: str) -> None`
- `delete_machine(machine_id: str) -> None`

---

### Movement Management

- `get_movements() -> list[Movement]`

---

### Report Management

- `generate_inventory_report() -> str`

---

## 4. ReportPort / Report-Adapter

Die Report-Logik erzeugt derzeit einen textbasierten Lager-/Inventarbericht.

### Unterstützte Reports

#### `generate_inventory_report() -> str`

Generiert eine textbasierte Übersicht über:
- Produkte
- Bestände
- Lagerwert
- kritische Bestände
- Bewegungsdaten

**Rückgabeformat:**  
- `str`

**Beispielhafte Inhalte:**
- Produkt-ID
- Name
- Bestand
- Preis
- Gesamtwert
- Anzahl kritischer Produkte

---

## 5. GUI-Verwendung der Contracts

Die grafische Benutzeroberfläche (GUI) greift nicht direkt auf die Datenbank zu.

Die GUI kommuniziert über:
- Controller
- Service Layer

**Verwendete Komponenten:**
- `FitnessCenterService`
- Controller-Schicht (`member_controller`, `product_controller`, usw.)
- Report-Logik

**Typische GUI-Funktionen:**
- Produkte anzeigen
- Produkte anlegen, bearbeiten, löschen
- Lagerbestand erhöhen oder verringern
- Mitglieder anzeigen und verwalten
- Mitarbeiter verwalten
- Geräte anzeigen und zuweisen
- Automaten verwalten
- Reports anzeigen

Dadurch bleibt die Anwendung:

- klar strukturiert
- testbar
- wartbar

---

## 6. Architekturregel

Die Kommunikation zwischen den Komponenten erfolgt nach folgendem Prinzip:

`GUI -> Controller -> Service -> RepositoryPort -> RepositoryAdapter -> Datenbank`

**Zusätzliche Regeln:**
- Die GUI enthält keine direkte Datenbanklogik.
- Die Controller enthalten keine Businesslogik.
- Die Businesslogik greift nur über RepositoryPorts auf Daten zu.
- Persistenzadapter können ausgetauscht werden, ohne die Businesslogik zu verändern.
- Reports basieren auf gespeicherten Daten aus den Repositories.

---

## Versionshistorie der Contracts

### v0.9
- Ergänzung der Update-Methoden bei Member, Employee und Product
- Ergänzung der Delete-Methoden bei Product, Equipment und VendingMachine
- Service-Schnittstellen final an aktuellen Code angepasst
- Report-Rückgabeformat auf `str` präzisiert

### v0.8
- Controller-/Service-Integration vorbereitet
- Abgleich mit aktueller GUI-Anbindung

### v0.5
- Abgleich der Contracts mit den aktuellen Domain-Modellen
- Ergänzung von `email`, `phone`, `membership_type` und `created_at` bei `Member`
- Ergänzung von `email`, `phone` und `created_at` bei `Employee`
- Umbenennung von `type` zu `equipment_type`
- Ergänzung von `assigned_employee_id` und `created_at` bei `Equipment`
- Ergänzung von `machine_type`, `assigned_employee_id` und `created_at` bei `VendingMachine`
- Erweiterung der Service-Schnittstellen passend zum aktuellen Code-Stand

### v0.2
- Erweiterung der Domänenmodelle um:
  - Product
  - Movement
  - Employee
  - Equipment
  - VendingMachine
- Anpassung der RepositoryPorts
- Erweiterung des FitnessCenterService
- Definition der Report-Ports für Lager und Geräte

### v0.1
- Erste Version der Contracts-Struktur
# Schnittstellen-Dokumentation (Contracts)

## Übersicht

# Schnittstellen-Dokumentation (Contracts)

Diese Datei dokumentiert die zentralen Schnittstellen des Projekts **Fitnesscenter**.
Sie wird von **Rolle 1 (Contract Owner)** gepflegt und bei Änderungen an Architektur, Services, Repositories oder Reports aktualisiert.

Die Contracts definieren, wie die einzelnen Komponenten miteinander kommunizieren:

- GUI
- Businesslogik
- Datenpersistenz
- Reports

---

## 1. Zentrale Domänenobjekte

### Product

Repräsentiert ein Produkt im Fitnesscenter (z. B. Snacks, Getränke, Zubehör).

**Attribute:**
- `product_id: str` - Eindeutige Produkt-ID
- `name: str` - Produktname
- `description: str` - Beschreibung
- `price: float` - Preis pro Einheit
- `quantity: int` - Lagerbestand
- `category: str` - Kategorie (Snack, Getränk, Zubehör)

---

### Movement

Repräsentiert eine Lagerbewegung eines Produkts.

**Attribute:**
- `movement_id: str`
- `product_id: str`
- `quantity_change: int`
- `movement_type: str` - IN / OUT / CORRECTION
- `timestamp: str`
- `performed_by: str`

---

### Member

Repräsentiert ein Mitglied des Fitnesscenters.

**Attribute:**
- `member_id: str`
- `first_name: str`
- `last_name: str`
- `birth_date: str`
- `active: bool`

---

### Employee

Repräsentiert einen Mitarbeiter des Fitnesscenters.

**Attribute:**
- `employee_id: str`
- `first_name: str`
- `last_name: str`
- `role: str`
- `active: bool`

---

### Equipment

Repräsentiert ein Fitnessgerät.

**Attribute:**
- `equipment_id: str`
- `name: str`
- `type: str`
- `status: str`
- `location: str`

---

### VendingMachine

Repräsentiert einen Snack- oder Getränkeautomaten.

**Attribute:**
- `machine_id: str`
- `location: str`
- `assigned_employee: str`
- `active: bool`

---

## 2. RepositoryPorts

RepositoryPorts definieren die Schnittstellen zur Datenpersistenz.

---

### ProductRepositoryPort

Speichert und lädt Produkte.

Methoden:

- `save_product(product: Product) -> None`
- `load_product(product_id: str) -> Product | None`
- `load_all_products() -> list[Product]`
- `delete_product(product_id: str) -> None`

---

### MovementRepositoryPort

Speichert Lagerbewegungen.

Methoden:

- `save_movement(movement: Movement) -> None`
- `load_movements() -> list[Movement]`

---

### MemberRepositoryPort

Speichert Mitglieder.

Methoden:

- `save_member(member: Member) -> None`
- `load_member(member_id: str) -> Member | None`
- `load_all_members() -> list[Member]`
- `delete_member(member_id: str) -> None`

---

### EmployeeRepositoryPort

Speichert Mitarbeiter.

Methoden:

- `save_employee(employee: Employee) -> None`
- `load_employee(employee_id: str) -> Employee | None`
- `load_all_employees() -> list[Employee]`
- `delete_employee(employee_id: str) -> None`

---

### EquipmentRepositoryPort

Speichert Fitnessgeräte.

Methoden:

- `save_equipment(equipment: Equipment) -> None`
- `load_equipment(equipment_id: str) -> Equipment | None`
- `load_all_equipment() -> list[Equipment]`
- `delete_equipment(equipment_id: str) -> None`

---

### VendingMachineRepositoryPort

Speichert Automaten.

Methoden:

- `save_machine(machine: VendingMachine) -> None`
- `load_machine(machine_id: str) -> VendingMachine | None`
- `load_all_machines() -> list[VendingMachine]`
- `delete_machine(machine_id: str) -> None`
---

## 3. FitnessCenterService

Service-Klasse für die zentrale Businesslogik.

### Member Management

- `create_member(first_name: str, last_name: str, birth_date: str) -> Member`
- `get_member(member_id: str) -> Member | None`
- `get_all_members() -> list[Member]`
- `deactivate_member(member_id: str) -> None`

---

### Employee Management

- `create_employee(first_name: str, last_name: str, role: str) -> Employee`
- `get_all_employees() -> list[Employee]`

---

### Product Management

- `create_product(name: str, description: str, price: float) -> Product`
- `add_stock(product_id: str, quantity: int) -> None`
- `remove_stock(product_id: str, quantity: int) -> None`
- `get_all_products() -> list[Product]`

---

### Equipment Management

- `create_equipment(name: str, type: str, location: str) -> Equipment`
- `update_equipment_status(equipment_id: str, status: str) -> None`
- `get_all_equipment() -> list[Equipment]`

---

### Vending Machine Management

- `create_machine(location: str) -> VendingMachine`
- `assign_employee_to_machine(machine_id: str, employee_id: str) -> None`
- `get_all_machines() -> list[VendingMachine]`

---

## 4. ReportPort

Port für Report-Generierung.

### Methoden

`generate_inventory_report() -> list[dict]`

Generiert eine Übersicht aller Produkte und deren Bestand.

Beispiel:

- product_id
- name
- quantity
- price

---

`generate_equipment_status_report() -> list[dict]`

Übersicht über den Status aller Fitnessgeräte.

Beispiel:

- equipment_id
- name
- status
- location
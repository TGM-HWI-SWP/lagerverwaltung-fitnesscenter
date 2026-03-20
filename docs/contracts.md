# Schnittstellen-Dokumentation (Contracts)

## Übersicht

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
- `deactivate_member(member_id: str) -> None`
- `activate_member(member_id: str) -> None`

---

### Employee Management

- `create_employee(employee_id: str, first_name: str, last_name: str, role: str, email: str, phone: str = "") -> Employee`
- `get_employee(employee_id: str) -> Employee | None`
- `get_all_employees() -> list[Employee]`
- `deactivate_employee(employee_id: str) -> None`
- `activate_employee(employee_id: str) -> None`

---

### Product Management

- `create_product(product_id: str, name: str, description: str, price: float, quantity: int, category: str) -> Product`
- `get_product(product_id: str) -> Product | None`
- `get_all_products() -> list[Product]`
- `add_stock(product_id: str, quantity: int, performed_by: str) -> None`
- `remove_stock(product_id: str, quantity: int, performed_by: str) -> None`
- `delete_product(product_id: str) -> None`

---

### Equipment Management

- `create_equipment(equipment_id: str, name: str, equipment_type: str, location: str, status: str = "available") -> Equipment`
- `get_equipment(equipment_id: str) -> Equipment | None`
- `get_all_equipment() -> list[Equipment]`
- `update_equipment_status(equipment_id: str, status: str) -> None`
- `assign_employee_to_equipment(equipment_id: str, employee_id: str) -> None`
- `delete_equipment(equipment_id: str) -> None`

---

### Vending Machine Management

- `create_machine(machine_id: str, location: str, machine_type: str) -> VendingMachine`
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

## 4. ReportPort

Port für Report-Generierung.

### Methoden

#### `generate_inventory_report() -> list[dict]`

Generiert eine Übersicht aller Produkte und deren Bestand.

**Beispiel-Ausgabe:**
- `product_id`
- `name`
- `quantity`
- `price`
- `category`

---

#### `generate_equipment_status_report() -> list[dict]`

Generiert eine Übersicht über den Status aller Fitnessgeräte.

**Beispiel-Ausgabe:**
- `equipment_id`
- `name`
- `equipment_type`
- `status`
- `location`
- `assigned_employee_id`

---

## 5. GUI-Verwendung der Contracts

Die grafische Benutzeroberfläche (GUI) greift nicht direkt auf die Datenbank zu.

Die GUI kommuniziert ausschließlich über die Businesslogik.

**Verwendete Komponenten:**
- `FitnessCenterService`
- `ReportPort`

**Typische GUI-Funktionen:**
- Produkte anzeigen
- Produkte zum Lager hinzufügen oder entfernen
- Mitglieder anzeigen
- Mitarbeiter verwalten
- Geräte anzeigen
- Automaten verwalten
- Reports anzeigen

Dadurch bleibt die Anwendung:

- klar strukturiert
- testbar
- wartbar

---

## 6. Architekturregel

Die Kommunikation zwischen den Komponenten erfolgt nach folgendem Prinzip:

`GUI -> Service -> Repository -> Datenbank`

**Zusätzliche Regeln:**
- Die GUI enthält keine direkte Datenbanklogik.
- Die Businesslogik greift nur über RepositoryPorts auf Daten zu.
- Persistenzadapter können ausgetauscht werden, ohne die Businesslogik zu verändern.
- Reports basieren auf gespeicherten Daten aus den Repositories.

---

## Versionshistorie der Contracts

### v0.3
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
- Definition der ReportPorts für Lager und Geräte

### v0.1
- Erste Version der Contracts-Struktur
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

### Member

Repräsentiert ein Mitglied des Fitnesscenters.

**Attribute:**
- `member_id: str` - Eindeutige ID des Mitglieds
- `first_name: str` - Vorname
- `last_name: str` - Nachname
- `birth_date: str` - Geburtsdatum
- `membership_id: str | None` - Zugewiesene Mitgliedschaft
- `active: bool` - Status des Mitglieds

### Membership

Repräsentiert eine Mitgliedschaft bzw. ein Abo.

**Attribute:**
- `membership_id: str` - Eindeutige ID der Mitgliedschaft
- `name: str` - Name des Abos
- `price_per_month: float` - Monatlicher Preis
- `duration_months: int` - Laufzeit in Monaten
- `active: bool` - Status der Mitgliedschaft

### CheckIn

Repräsentiert einen Check-in eines Mitglieds.

**Attribute:**
- `checkin_id: str` - Eindeutige ID des Check-ins
- `member_id: str` - Zugehörige Mitglieds-ID
- `timestamp: str` - Zeitpunkt des Check-ins

---

## 2. ReportPort

**Verantwortlich:** Rolle 3 (Reports & Qualität)

### Beschreibung
Abstrakte Schnittstelle für Report-Generierung.

### Methoden

#### `generate_inventory_report() -> str`
Generiert einen Lagerbestandsbericht.

**Return:**
- Formatierter String-Bericht

**Implementierungen:**
- `ConsoleReportAdapter` (v0.1)

#### `generate_movement_report() -> str`
Generiert ein Bewegungsprotokoll.

**Return:**
- Formatierter String-Bericht

**Implementierungen:**
- `ConsoleReportAdapter` (v0.1)

---

## 3. WarehouseService

**Verantwortlich:** Rolle 2 (Businesslogik)

### Beschreibung
Service-Klasse für zentrale Lagerverwaltungslogik.

### Methoden

#### `create_product(...) -> Product`
Erstellt ein neues Produkt.

**Parameter:**
- `product_id: str` - Eindeutige ID
- `name: str` - Produktname
- `description: str` - Beschreibung
- `price: float` - Preis
- `category: str` - Kategorie (optional)
- `initial_quantity: int` - Anfangsbestand

**Return:**
- Neue Product-Instanz

**Exceptions:**
- `ValueError`: Bei ungültigen Eingaben

#### `add_to_stock(product_id: str, quantity: int, reason: str, user: str) -> None`
Erhöht den Bestand.

**Parameter:**
- `product_id: str`
- `quantity: int` - Menge
- `reason: str` - Grund (optional)
- `user: str` - Benutzer (default: "system")

**Exceptions:**
- `ValueError`: Wenn Produkt nicht existiert

#### `remove_from_stock(product_id: str, quantity: int, reason: str, user: str) -> None`
Verringert den Bestand.

**Parameter:**
- `product_id: str`
- `quantity: int` - Menge
- `reason: str` - Grund (optional)
- `user: str` - Benutzer (default: "system")

**Exceptions:**
- `ValueError`: Wenn Bestand unzureichend oder Produkt nicht existiert

#### `get_product(product_id: str) -> Optional[Product]`
Ruft ein einzelnes Produkt ab.

**Return:**
- Product oder None

#### `get_all_products() -> Dict[str, Product]`
Ruft alle Produkte ab.

**Return:**
- Dictionary mit allen Produkten

#### `get_movements() -> List[Movement]`
Ruft alle Lagerbewegungen ab.

**Return:**
- Liste aller Movements

#### `get_total_inventory_value() -> float`
Berechnet den Gesamtwert des Lagers.

**Return:**
- Wert in Euro

---

## 4. Domain Models

### Product

**Attribute:**
- `id: str` - Eindeutige ID
- `name: str` - Produktname
- `description: str` - Beschreibung
- `price: float` - Preis pro Einheit
- `quantity: int` - Bestand
- `sku: str` - Stock Keeping Unit
- `category: str` - Kategorie
- `created_at: datetime` - Erstellungsdatum
- `updated_at: datetime` - Änderungsdatum
- `notes: str` - Anmerkungen

**Methoden:**
- `update_quantity(amount: int) -> None` - Bestand ändern
- `get_total_value() -> float` - Gesamtwert berechnen

### Movement

**Attribute:**
- `id: str` - Eindeutige Bewegungs-ID
- `product_id: str` - Verweis auf Produkt
- `product_name: str` - Name des Produkts
- `quantity_change: int` - Mengenänderung (+/-)
- `movement_type: str` - "IN", "OUT", "CORRECTION"
- `reason: str` - Grund (optional)
- `timestamp: datetime` - Zeitstempel
- `performed_by: str` - Benutzer

---

## Versionshistorie der Contracts

### v0.1 (2025-01-20)
- RepositoryPort: Grundlegende CRUD-Operationen
- ReportPort: Basis-Report-Generierung
- WarehouseService: Kern-Use-Cases
- Product: Basis-Domain-Model
- Movement: Lagerbewegungen-Protokoll
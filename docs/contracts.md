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

### 2.1 MemberRepositoryPort

**Verantwortlich:** Rolle 1 / Rolle 2

### Beschreibung
Abstrakte Schnittstelle für die Persistenz von Mitgliedern.

### Methoden

#### `save_member(member: Member) -> None`
Speichert ein Mitglied.

**Parameter:**
- `member`: Member-Instanz

**Exceptions:**
- Keine

**Implementierungen:**
- `InMemoryMemberRepository` (v0.1)
- `SupabaseMemberRepository` (geplant)

---

#### `load_member(member_id: str) -> Member | None`
Lädt ein einzelnes Mitglied.

**Parameter:**
- `member_id`: Eindeutige Mitglieds-ID

**Return:**
- `Member` oder `None`, falls nicht gefunden

**Implementierungen:**
- `InMemoryMemberRepository` (v0.1)
- `SupabaseMemberRepository` (geplant)

---

#### `load_all_members() -> list[Member]`
Lädt alle Mitglieder.

**Return:**
- Liste aller Member-Objekte

**Implementierungen:**
- `InMemoryMemberRepository` (v0.1)
- `SupabaseMemberRepository` (geplant)

---

#### `delete_member(member_id: str) -> None`
Löscht ein Mitglied.

**Parameter:**
- `member_id`: Eindeutige Mitglieds-ID

**Exceptions:**
- Keine

**Implementierungen:**
- `InMemoryMemberRepository` (v0.1)
- `SupabaseMemberRepository` (geplant)

---

### 2.2 MembershipRepositoryPort

**Verantwortlich:** Rolle 1 / Rolle 2

### Beschreibung
Abstrakte Schnittstelle für die Persistenz von Mitgliedschaften.

### Methoden

#### `save_membership(membership: Membership) -> None`
Speichert eine Mitgliedschaft.

#### `load_membership(membership_id: str) -> Membership | None`
Lädt eine einzelne Mitgliedschaft.

#### `load_all_memberships() -> list[Membership]`
Lädt alle Mitgliedschaften.

#### `delete_membership(membership_id: str) -> None`
Löscht eine Mitgliedschaft.

**Implementierungen:**
- `InMemoryMembershipRepository` (v0.1)
- `SupabaseMembershipRepository` (geplant)

---

### 2.3 CheckInRepositoryPort

**Verantwortlich:** Rolle 1 / Rolle 2

### Beschreibung
Abstrakte Schnittstelle für die Persistenz von Check-ins.

### Methoden

#### `save_checkin(checkin: CheckIn) -> None`
Speichert einen Check-in.

#### `load_all_checkins() -> list[CheckIn]`
Lädt alle Check-ins.

#### `load_checkins_by_member(member_id: str) -> list[CheckIn]`
Lädt alle Check-ins eines bestimmten Mitglieds.

**Implementierungen:**
- `InMemoryCheckInRepository` (v0.1)
- `SupabaseCheckInRepository` (geplant)

---

## 3. FitnessCenterService

**Verantwortlich:** Rolle 2 (Businesslogik)

### Beschreibung
Service-Klasse für die zentrale Businesslogik des Fitnesscenter-Projekts.

### Methoden

#### `create_member(first_name: str, last_name: str, birth_date: str) -> Member`
Erstellt ein neues Mitglied.

**Parameter:**
- `first_name: str` - Vorname
- `last_name: str` - Nachname
- `birth_date: str` - Geburtsdatum

**Return:**
- Neue `Member`-Instanz

**Exceptions:**
- `ValueError`: Bei ungültigen Eingaben

---

#### `get_member(member_id: str) -> Member | None`
Lädt ein einzelnes Mitglied.

**Parameter:**
- `member_id: str`

**Return:**
- `Member` oder `None`

---

#### `get_all_members() -> list[Member]`
Lädt alle Mitglieder.

**Return:**
- Liste aller `Member`-Objekte

---

#### `assign_membership(member_id: str, membership_id: str) -> None`
Weist einem Mitglied eine Mitgliedschaft zu.

**Parameter:**
- `member_id: str`
- `membership_id: str`

**Exceptions:**
- `ValueError`: Wenn Mitglied oder Mitgliedschaft nicht existiert

---

#### `deactivate_member(member_id: str) -> None`
Deaktiviert ein Mitglied.

**Parameter:**
- `member_id: str`

**Exceptions:**
- `ValueError`: Wenn Mitglied nicht existiert

---

#### `create_membership(name: str, price_per_month: float, duration_months: int) -> Membership`
Erstellt eine neue Mitgliedschaft.

**Parameter:**
- `name: str`
- `price_per_month: float`
- `duration_months: int`

**Return:**
- Neue `Membership`-Instanz

**Exceptions:**
- `ValueError`: Bei ungültigen Eingaben

---

#### `get_all_memberships() -> list[Membership]`
Lädt alle Mitgliedschaften.

**Return:**
- Liste aller `Membership`-Objekte

---

#### `check_in_member(member_id: str) -> CheckIn`
Erfasst einen Check-in für ein Mitglied.

**Parameter:**
- `member_id: str`

**Return:**
- Neue `CheckIn`-Instanz

**Exceptions:**
- `ValueError`: Wenn Mitglied nicht existiert oder inaktiv ist

---

#### `get_checkins_by_member(member_id: str) -> list[CheckIn]`
Lädt alle Check-ins eines Mitglieds.

**Return:**
- Liste aller `CheckIn`-Objekte

---

## 4. ReportPort

**Verantwortlich:** Rolle 2 / spätere Integration

### Beschreibung
Abstrakte Schnittstelle für die Generierung von Reports auf Basis gespeicherter Daten.

Da das Projekt derzeit ohne Report B weitergeführt wird, wird zunächst nur **Report A** berücksichtigt.

### Methoden

#### `generate_member_overview() -> list[dict]`
Generiert eine Übersicht aller Mitglieder.

**Return:**
- Liste von Dictionaries mit z. B.:
  - `member_id`
  - `full_name`
  - `membership_name`
  - `active`

**Implementierungen:**
- `MemberOverviewReportAdapter` (geplant)

---

#### `generate_active_members_report() -> list[dict]`
Generiert eine Übersicht aktiver Mitglieder.

**Return:**
- Liste aktiver Mitglieder

**Implementierungen:**
- `MemberOverviewReportAdapter` (optional)

---

## 5. GUI-Verwendung der Contracts

Die GUI greift nicht direkt auf die Datenbank zu.

Die GUI verwendet folgende Services:

- `FitnessCenterService`
- `ReportPort`

Mögliche GUI-Funktionen:

- Mitglied anlegen
- Mitglieder anzeigen
- Mitgliedschaft zuweisen
- Check-in erfassen
- Report A anzeigen

Dadurch bleibt die Anwendung:

- klar strukturiert
- testbar
- wartbar

---

## 6. Architekturregel

Die Kommunikation zwischen den Komponenten erfolgt nach folgendem Prinzip:

`GUI -> Service -> Repository -> Datenbank`

Zusätzliche Regeln:

- Die GUI enthält keine direkte Datenbanklogik
- Die Businesslogik greift nur über RepositoryPorts auf Daten zu
- Reports basieren auf gespeicherten Daten
- Persistenzadapter können ausgetauscht werden, ohne die Businesslogik zu ändern

---

## Versionshistorie der Contracts

### v0.1
- Umstellung der Contracts von Lagerverwaltung auf Fitnesscenter
- Einführung der Domänenobjekte `Member`, `Membership` und `CheckIn`
- Definition der RepositoryPorts für Mitglieder, Mitgliedschaften und Check-ins
- Definition des zentralen `FitnessCenterService`
- Definition eines ersten Report-Contracts für Report A
- Ergänzung der GUI-Nutzung und Architekturregeln
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
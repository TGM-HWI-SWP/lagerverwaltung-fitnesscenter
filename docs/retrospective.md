# Retrospektive

## Projektübersicht

**Projekttitel:** Fitnesscenter Management System  
**Projektdauer:** 8 Wochen  
**Gruppengröße:** 3 Personen  
**Projektverantwortung:** Ivan Strainovic (Rolle 1 – Contract Owner)

---

## Versionsmilestones

### v0.1 - Projektstart & Grundarchitektur
**Abschluss:** 13.03.2026

#### Was lief gut?
- Klare Rollenverteilung von Anfang an
- Frühe Entscheidung für Hexagonale Architektur
- Struktur von Domain, Ports und Services sauber definiert

#### Was konnte verbessert werden?
- Anfangs Unsicherheit bei Architekturverständnis
- Wenig Abstimmung bei Naming (z. B. member_id vs id)

#### Learnings
- Architektur muss früh fixiert werden, sonst Chaos

---

### v0.2 - Walking Skeleton
**Abschluss:** 13.03.2026

#### Was lief gut?
- Alle wichtigen Ports definiert
- Services als zentrale Logik festgelegt
- Grundstruktur vollständig vorhanden

#### Was konnte verbessert werden?
- Kaum Tests geschrieben
- UI noch komplett fehlend

#### Learnings
- Skeleton ist wichtig, aber ohne Tests wenig wert

---

### v0.3 - Domain & Struktur
**Abschluss:** 13.03.2026

#### Was lief gut?
- Domain-Modelle vollständig implementiert
- Validierungen direkt integriert
- Klare Trennung zwischen Schichten

#### Was konnte verbessert werden?
- Teilweise doppelte Logik zwischen Klassen
- Naming nicht überall konsistent

#### Learnings
- Domain ist das Fundament → muss sauber sein

---

### v0.4 - Architektur-Umstellung
**Abschluss:** 20.03.2026

#### Was lief gut?
- Erfolgreiche Umstellung von Warehouse auf Fitnesscenter
- Architektur-Dokumentation verbessert
- Struktur jetzt realitätsnah

#### Was konnte verbessert werden?
- Umstellung hat viel Zeit gekostet
- Teilweise doppelte Arbeit

#### Learnings
- Änderungen früh machen, nicht mitten im Projekt

---

### v0.6 - Controller & erste GUI
**Abschluss:** 27.03.2026

#### Was lief gut?
- Controller-Schicht sauber aufgebaut
- Erste GUI-Seiten funktional
- Verbindung UI ↔ Controller vorbereitet

#### Was konnte verbessert werden?
- UI und Backend nicht abgestimmt
- Unterschiedliche Datenformate (dict vs Objekt)

#### Learnings
- Schnittstellen müssen exakt definiert sein

---

### v0.7 - Erweiterung Controller
**Abschluss:** 10.04.2026

#### Was lief gut?
- Movement und Report Controller ergänzt
- Struktur vollständig

#### Was konnte verbessert werden?
- Teilweise redundanter Code
- Tests fehlen weiterhin

#### Learnings
- Ohne Tests verliert man schnell Überblick

---

### v0.8 - Integration
**Abschluss:** 17.04.2026

#### Was lief gut?
- Controller vollständig integriert
- Service-Anbindung vorbereitet
- Merge-Konflikte gelöst

#### Was konnte verbessert werden?
- Merge-Konflikte durch fehlende Abstimmung
- Unterschiedliche Implementierungen im Team

#### Learnings
- Regelmäßiges Pullen verhindert Chaos

---

### v0.9 - Finale Backend-Struktur
**Abschluss:** 21.04.2026

#### Was lief gut?
- Service vollständig (CRUD + Stock)
- Repository Ports erweitert
- Vorbereitung für finale UI-Integration

#### Was konnte verbessert werden?
- UI noch nicht vollständig integriert
- Tests fehlen weiterhin großteils

#### Learnings
- Backend zuerst stabil machen → dann UI

---

## Überblick: Stärken & Schwächen

### Team-Stärken
- Gute technische Umsetzung
- Saubere Architektur
- Klare Rollenverteilung
- Gute Problemlösungskompetenz

### Verbesserungspotenzial
- Kommunikation zwischen UI und Backend
- Mehr Tests
- Frühere Abstimmung im Team

---

## Einzelne Learnings pro Rolle

### Rolle 1 (Contract Owner)
- Gelernt: Architektur, Schnittstellen, Koordination
- Verbessern: Mehr Kontrolle über Konsistenz im Team

### Rolle 2 (Businesslogik & Persistenz)
- Gelernt: Service Layer + Datenbankanbindung
- Verbessern: Testabdeckung

### Rolle 3 / 4 (GUI)
- Gelernt: PyQt6, UI-Struktur
- Verbessern: Anbindung an Backend sauberer gestalten

---

## Technische Erkenntnisse

### Was funktioniert gut?
- Port-Adapter-Architektur → sehr klare Struktur
- Service Layer → zentrale Logik gut gekapselt
- Supabase Integration → funktioniert stabil

### Technische Schulden
- Fehlende Tests
- UI teilweise noch mit Demo-Daten
- Inkonsistente Datenformate (dict vs Objekt)

### Empfehlungen für Folge-Projekte
1. Tests von Anfang an schreiben
2. UI und Backend früh verbinden
3. Einheitliche Datenstruktur definieren

---

## Mergekonflikte & Lösungen

| Datei | Konflikt-Typ | Lösung | Gelerntes |
|------|-------------|--------|----------|
| src/domain/member.py | Naming + Timestamp | Vereinheitlicht auf member_id und datetime.utcnow | Konsistenz ist extrem wichtig |

---

## Abschließende Bewertung

### Projektqualität (1-10)
- Code-Qualität: 8
- Dokumentation: 9
- Tests: 4
- Zusammenarbeit: 9  
- **Durchschnitt:** 8

---

### Was würde ich anders machen?
1. Früher Tests schreiben  
2. UI und Backend früher verbinden  
3. Mehr Abstimmung im Team  

---

### Feedback an die Lehrperson
- Gute Projektstruktur und realitätsnah  
- Mehr Fokus auf Testing wäre hilfreich  

---

**Retrospektive erstellt:** 23.04.2026  
**Geschrieben von:** Ivan Strainovic (Rolle 1)
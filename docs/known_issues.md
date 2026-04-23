# Known Issues

## Aktuelle Probleme

### Kritisch
- [ ] Keine kritischen Issues

### Hoch
- [ ] GUI noch nicht vollständig mit Backend (Controller/Service) integriert
  → Einige UI-Seiten arbeiten noch teilweise mit Demo-Daten

### Mittel
- [ ] Teilweise fehlende Validierungen in GUI-Dialogen
- [ ] Testabdeckung nicht vollständig (vor allem Integrationstests)

### Niedrig
- [ ] GUI-Styling kann weiter verbessert werden
- [ ] Uneinheitliche Benennung einzelner UI-Komponenten

---

## Gelöste Issues (Archiv)

### v0.5
- ✓ Umstellung von Warehouse auf Fitnesscenter abgeschlossen

### v0.7
- ✓ Controller-Struktur erweitert und stabilisiert

### v0.8
- ✓ Mergekonflikt im Member-Domain-Modell gelöst (id → member_id, datetime vereinheitlicht)

---

## Bekannte Limitationen

### Technisch
- Supabase-Verbindung erfordert gültige `.env` Konfiguration (kein Fallback)
- Keine Offline-Nutzung möglich (bei Supabase-Adapter)
- Keine Pagination in Tabellen implementiert

### Funktional
- Keine Rollen-/Rechteverwaltung (Admin/User)
- Keine grafischen Reports (nur textbasierte Reports)
- Kein Mehrbenutzerbetrieb (Single-User Anwendung)

---

## Workarounds

### GUI zeigt falsche/alte Daten
**Workaround:** Anwendung neu starten oder Daten neu laden

### Supabase Verbindung funktioniert nicht
**Workaround:** `.env` Datei prüfen (SUPABASE_URL, SUPABASE_KEY)

---

**Letzte Aktualisierung:** 2026-04-23
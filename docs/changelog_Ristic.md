# Changelog - Vladan Ristic

Persönliches Changelog für Vladan Ristic, Rolle: GUI-Entwicklung (Rolle 4)

---

## [v0.1] - 2026-03-13

### Implementiert

* Grundstruktur der GUI erstellt
* Ordnerstruktur für pages, widgets, tables und styles aufgebaut
* Erste Dateien für Dashboard und GUI vorbereitet

### Tests geschrieben

* test_gui_start
* test_structure_loading

### Commits

4eda5340 Feat: Add initial GUI structure for role 4 (dashboard, inventory, dialogs, tables)

### Mergekonflikt(e)

* Keine

---

## [v0.2] - 2026-03-20

### Implementiert

* MainWindow erstellt
* Sidebar mit Navigation eingebaut
* Seitenwechsel mit Animation umgesetzt
* Dashboard mit Stat Cards erstellt
* Mehrere Pages angelegt (Dashboard, Mitglieder, Mitarbeiter, Produkte, etc.)
* GUI so aufgebaut, dass sie später mit der Datenbank verbunden werden kann

### Tests geschrieben

* test_main_window
* test_navigation
* test_page_switch

### Commits

d3f91c55 Feat: Implement GUI foundation with animated main window, sidebar navigation and dashboard layout

### Mergekonflikt(e)

* Keine

---

## [v0.3] - 2026-03-27

### Implementiert

* products_page.py erstellt und vollständig umgesetzt
* Produkte-Seite mit Tabelle zur Anzeige aller Produkte entwickelt
* Suchfunktion für Produkte eingebaut
* Filter nach Kategorie und Lagerbestand integriert
* Statistik-Karten für Gesamtprodukte, Bestand, kritische Produkte und Lagerwert hinzugefügt
* Dialog zum Hinzufügen und Bearbeiten von Produkten implementiert
* Dialog zum Ändern des Lagerbestands umgesetzt
* Demo-Daten integriert, damit die Seite ohne Datenbank funktioniert
* Struktur vorbereitet für spätere Verbindung mit Supabase/PostgreSQL

### Tests geschrieben

* test_products_page_start
* test_product_filtering
* test_product_dialog_opening
* test_stock_dialog_opening

### Commits

Feat: Add products page with table, filtering, dialogs and stats

### Mergekonflikt(e)

* Keine

---

## [v0.4] - offen

### Implementiert

* Dashboard mit echten Daten (geplant)
* Design verbessern mit QSS (geplant)

### Tests geschrieben

* test_dashboard (geplant)

### Commits

Keine

### Mergekonflikt(e)

* Keine

---

## [v0.5] - offen

### Implementiert

* Dialoge für Hinzufügen/Bearbeiten (geplant)
* Such- und Filterfunktion (geplant)

### Tests geschrieben

* test_dialog (geplant)

### Commits

Keine

### Mergekonflikt(e)

* Keine

---

## [v1.0] - offen

### Implementiert

* GUI fertig mit Datenbank verbunden (geplant)

### Tests geschrieben

* test_full_system (geplant)

### Commits

Keine

### Mergekonflikt(e)

* Keine

---

## Zusammenfassung

**Gesamt implementierte Features:** 3  
**Gesamt geschriebene Tests:** 9  
**Gesamt Commits:** 3  

**Größte Herausforderung:**  
Die GUI richtig aufzubauen und alles sauber zu strukturieren sowie eine erste komplexe Seite mit Tabellen, Filtern und Dialogen umzusetzen.

**Schönste Code-Zeile:**


self.page_stack.slide_to_index(index)


---

**Changelog erstellt von:** Vladan Ristic  
**Letzte Aktualisierung:** 2026-03-27
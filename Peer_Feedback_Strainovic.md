# TGM WI | SWP | Fitnesscenter

## Peer Feedback an Simsek

---

## Kriterium 1

Wurde die vorgegebene Projektstruktur sinnvoll genutzt oder verändert in Bezug auf die Vorlage?

Wirkt die Struktur des Projekts (Ordner, Module, Klassen) nachvollziehbar?

**Kommentar für Kriterium 1:**

Die Projektstruktur ist insgesamt gut aufgebaut und leicht verständlich. Die vorgegebene Struktur wurde übernommen und sinnvoll erweitert. Man erkennt klar die Aufteilung in Bereiche wie domain, services, ports, adapters, ui und reports, was gut zum Port-Adapter-Prinzip passt.

Auch der tests-Ordner ist übersichtlich organisiert, mit einer Trennung zwischen Unit- und Integrationstests, was sehr sinnvoll ist.

Positiv ist außerdem, dass eine Architektur-Dokumentation vorhanden ist, in der die Struktur erklärt wird. Dadurch kann man das Projekt besser nachvollziehen.

Insgesamt wirkt alles strukturiert und durchdacht, ohne unnötige oder unlogische Änderungen.

---

## Kriterium 2

Welche neue Kernfunktion der Software konntet ihr bereits nachvollziehen?

**Kommentar für Kriterium 2:**

Eine zentrale Kernfunktion der Software ist die Verwaltung von Fahrzeugen, Kunden und Ersatzteilen. Dabei können Daten erstellt, bearbeitet, gelöscht und abgefragt werden.

Zusätzlich gibt es Funktionen zur Validierung der Eingaben sowie zur Fehlerbehandlung, wodurch die Anwendung stabiler wirkt. Auch ein Export von Daten (z. B. als CSV oder Excel) ist möglich.

Außerdem ist eine Dashboard-Funktion vorhanden, die einen Überblick über wichtige Daten gibt.

Insgesamt sind die wichtigsten Funktionen einer Verwaltung gut umgesetzt und nachvollziehbar.

---

## Kriterium 3

Was wirkt aktuell noch unklar oder unvollständig?

**Kommentar für Kriterium 3:**

Einige Teile der Software wirken noch nicht vollständig fertig oder miteinander verbunden. Vor allem ist nicht immer klar, wie alle Komponenten zusammen in der Anwendung genutzt werden, da der Gesamtfluss teilweise fehlt.

Auch die GUI scheint noch nicht vollständig integriert zu sein bzw. ist nicht klar ersichtlich, wie alle Funktionen darüber gesteuert werden können.

Teilweise könnten Abläufe und Zusammenhänge noch besser dokumentiert oder nachvollziehbarer dargestellt werden.

---

## Kriterium 4

Gibt es erkennbare Schnittstellen zwischen Komponenten (z.B. GUI – Businesslogik – Datenhaltung)?

**Kommentar für Kriterium 4:**

Es sind klare Schnittstellen zwischen den einzelnen Komponenten erkennbar. Die GUI greift auf die Services zu, welche wiederum über Ports mit der Datenhaltung verbunden sind.

Die Trennung zwischen den einzelnen Schichten ist gut umgesetzt und entspricht dem Port-Adapter-Prinzip. Dadurch bleibt die Struktur übersichtlich und die Komponenten sind sauber voneinander getrennt.

---

## Kriterium 5

Wo wurden Contracts oder klar definierte Schnittstellen dokumentiert?

**Kommentar für Kriterium 5:**

Die Schnittstellen wurden im Projekt klar dokumentiert, insbesondere in der Datei contracts.md. Dort werden die wichtigsten Interfaces beschrieben und nachvollziehbar erklärt.

Zusätzlich sind die Schnittstellen auch im Code durch die Ports umgesetzt, wodurch die Trennung der Komponenten deutlich wird.

Insgesamt sind die Contracts gut erkennbar und sinnvoll dokumentiert.

---

## Kriterium 6

Welche technische Stärke des Projekts ist euch besonders aufgefallen?

Wo seht ihr aktuell das größte technische Risiko bis zur Endabgabe?

**Kommentar für Kriterium 6:**

Eine besondere technische Stärke des Projekts ist die klare Strukturierung in verschiedene Schichten wie GUI, Services, Ports und Adapters. Dadurch wirkt das Projekt gut aufgebaut und insgesamt technisch durchdacht. Auch die Aufteilung der Funktionen auf mehrere Services sowie die vorhandenen Tests und Reports sind positiv aufgefallen.

Das größte technische Risiko bis zur Endabgabe sehen wir aktuell in der vollständigen Integration aller Teile. Vor allem muss am Ende sichergestellt sein, dass GUI, Businesslogik und Datenhaltung sauber zusammenspielen und alle Funktionen im Gesamtfluss zuverlässig funktionieren.

---

## Kriterium 7

Wirkt die Commit-Historie aktiv und nachvollziehbar?

Was würdest du hier noch verbessern?

**Kommentar für Kriterium 7:**

Die Commit-Historie wirkt insgesamt aktiv und über mehrere Tage verteilt, was zeigt, dass regelmäßig am Projekt gearbeitet wurde. Positiv ist, dass einige Commit-Nachrichten konkret sind und beschreiben, was geändert wurde.

Allerdings gibt es auch mehrere eher unklare oder zu allgemeine Nachrichten wie „test“, „update“ oder „files“, wodurch nicht immer sofort ersichtlich ist, was genau gemacht wurde. Dadurch wird die Nachvollziehbarkeit teilweise eingeschränkt.

Verbessern könnte man die Commit-Messages, indem man sie durchgehend klarer und einheitlicher formuliert (z. B. nach dem Schema „feat: …“, „fix: …“). Außerdem könnten die Änderungen noch feiner aufgeteilt werden, damit jeder Schritt besser erkennbar ist.

---

## Kriterium 8

Sind Beiträge verschiedener Teammitglieder erkennbar?

**Kommentar für Kriterium 8:**

Die Commit-Historie wirkt insgesamt aktiv und über mehrere Tage verteilt, was Beiträge verschiedener Teammitglieder sind klar erkennbar. Mehrere Personen haben aktiv am Projekt gearbeitet und regelmäßig Commits beigetragen.

Die Verteilung der Beiträge wirkt insgesamt ausgewogen, auch wenn einzelne Mitglieder etwas mehr beigetragen haben als andere. Trotzdem ist erkennbar, dass alle am Projekt beteiligt waren.

Insgesamt ist die Zusammenarbeit im Team gut nachvollziehbar.

---

## Kriterium 9

Wie schätzt ihr den aktuellen Projektfortschritt ein?

**Kommentar für Kriterium 9:**

Der Projektfortschritt ist insgesamt schon ziemlich gut. Die Grundstruktur, Businesslogik, Services und auch Teile der GUI sind vorhanden. Außerdem wurden Reports und erste Tests umgesetzt, was zeigt, dass das Projekt schon weit entwickelt ist.

Allerdings fällt auf, dass die Changelogs nicht vollständig nach Vorlage ausgefüllt sind. Bei mehreren Versionen fehlen konkrete Einträge zu Features, Tests, Commits oder Mergekonflikten. Dadurch ist der Fortschritt zwar erkennbar, aber nicht immer klar und nachvollziehbar dokumentiert.

Insgesamt ist das Projekt technisch schon relativ weit, aber bei der Dokumentation (vor allem Changelogs) besteht noch Verbesserungsbedarf.

---

## Kriterium 10

Welche Frage würdet ihr dem Team als Code-Reviewer stellen?

**Kommentar für Kriterium 10:**

Wie stellt ihr sicher, dass eure Services unabhängig von der Datenhaltung bleiben und sauber über die Ports angebunden sind?

Außerdem wäre interessant, ob ihr geplant habt, die Testabdeckung noch weiter zu erhöhen, vor allem bei Randfällen und Fehlerbehandlung.

---

## Kriterium 11

Welchen konkreten Verbesserungsvorschlag würdet ihr dem Team geben?

**Kommentar für Kriterium 11:**

Ein konkreter Verbesserungsvorschlag wäre, die Dokumentation weiter zu vervollständigen, vor allem die Changelogs. Dort fehlen teilweise noch genaue Angaben zu Features, Tests und Commits, wodurch der Fortschritt nicht immer klar nachvollziehbar ist.

Außerdem könnte die Integration der einzelnen Komponenten (GUI, Services, Datenhaltung) noch besser abgestimmt werden, damit der Gesamtfluss der Anwendung klarer und vollständiger funktioniert.

---

## Gesamtfeedback

Insgesamt macht das Projekt einen guten und durchdachten Eindruck. Die Struktur ist klar aufgebaut und folgt dem Port-Adapter-Prinzip, wodurch die einzelnen Komponenten sauber getrennt sind. Besonders positiv sind die Services, Ports, Adapter sowie die vorhandenen Tests und Reports.

Auch die Zusammenarbeit im Team ist erkennbar, da regelmäßig von mehreren Mitgliedern Commits gemacht wurden.

Der Projektfortschritt ist schon weit, die wichtigsten Funktionen sind umgesetzt. Allerdings gibt es noch kleinere Schwächen in der Dokumentation, vor allem bei den Changelogs, die teilweise unvollständig sind.

Zusätzlich könnte die Integration der einzelnen Komponenten noch etwas verbessert werden, damit der Gesamtfluss klarer wird.

Insgesamt ein solides Projekt mit gutem Fortschritt, bei dem vor allem beim Feinschliff noch Potenzial besteht.

---

Strainovic  
4BHWII
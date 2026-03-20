from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)


# ---------------------------
# STAT CARD (WIEDERVERWENDBAR)
# ---------------------------
class StatCard(QFrame):
    """Moderne Statistik-Karte für Dashboard."""

    def __init__(self, title: str, value: str, subtitle: str = "") -> None:
        super().__init__()

        self.setObjectName("statCard")
        self.setMinimumHeight(120)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(6)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("statTitle")

        self.value_label = QLabel(value)
        self.value_label.setObjectName("statValue")

        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setObjectName("statSubtitle")

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtitle_label)


# ---------------------------
# DASHBOARD PAGE
# ---------------------------
class DashboardPage(QWidget):
    """Dashboard mit Übersicht über das gesamte System."""

    def __init__(self, controller=None) -> None:
        super().__init__()
        self.controller = controller

        self._create_ui()

    def _create_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)

        # Titel
        title = QLabel("Übersicht")
        title.setObjectName("dashboardTitle")

        subtitle = QLabel("Alle wichtigen Kennzahlen auf einen Blick")
        subtitle.setObjectName("dashboardSubtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # Grid für Karten
        grid = QGridLayout()
        grid.setSpacing(18)

        # Erste Reihe
        self.members_card = StatCard("Mitglieder", "124", "+12 diesen Monat")
        self.employees_card = StatCard("Mitarbeiter", "18", "Aktiv im System")
        self.products_card = StatCard("Produkte", "56", "Im Lager verfügbar")

        # Zweite Reihe
        self.equipment_card = StatCard("Geräte", "32", "Im Einsatz")
        self.vending_card = StatCard("Automaten", "6", "Aktiv")
        self.low_stock_card = StatCard("Kritische Bestände", "4", "Sofort prüfen")

        # Layout setzen
        grid.addWidget(self.members_card, 0, 0)
        grid.addWidget(self.employees_card, 0, 1)
        grid.addWidget(self.products_card, 0, 2)

        grid.addWidget(self.equipment_card, 1, 0)
        grid.addWidget(self.vending_card, 1, 1)
        grid.addWidget(self.low_stock_card, 1, 2)

        main_layout.addLayout(grid)

        # Platz für zukünftige Charts / Tabellen
        self._create_bottom_section(main_layout)

    def _create_bottom_section(self, layout: QVBoxLayout) -> None:
        """Unterer Bereich (z. B. Bewegungen, Charts)."""
        container = QFrame()
        container.setObjectName("dashboardBottom")

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(18, 18, 18, 18)

        label = QLabel("Letzte Aktivitäten (coming soon)")
        label.setObjectName("dashboardSectionTitle")

        container_layout.addWidget(label)

        layout.addWidget(container)

    # ---------------------------
    # SPÄTER: DATEN LADEN
    # ---------------------------
    def refresh_data(self) -> None:
        """Wird vom MainWindow aufgerufen (F5 etc.)."""
        if not self.controller:
            return

        # Beispiel (später implementieren)
        # members = self.controller.get_member_count()
        # self.members_card.value_label.setText(str(members))

        pass
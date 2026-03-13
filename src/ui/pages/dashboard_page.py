from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class StatCard(QFrame):
    """Kleine Statistik-Karte für das Dashboard."""

    def __init__(self, title: str, value: str, description: str) -> None:
        super().__init__()
        self.setObjectName("statCard")
        self.setMinimumHeight(140)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(8)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("statCardTitle")

        self.value_label = QLabel(value)
        self.value_label.setObjectName("statCardValue")

        self.description_label = QLabel(description)
        self.description_label.setObjectName("statCardDescription")
        self.description_label.setWordWrap(True)

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.description_label)
        layout.addStretch()


class InfoPanel(QFrame):
    """Allgemeines Info-Panel für Hinweise oder Schnellinfos."""

    def __init__(self, title: str, lines: list[str]) -> None:
        super().__init__()
        self.setObjectName("infoPanel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setObjectName("infoPanelTitle")
        layout.addWidget(title_label)

        for line in lines:
            line_label = QLabel(f"• {line}")
            line_label.setObjectName("infoPanelText")
            line_label.setWordWrap(True)
            layout.addWidget(line_label)

        layout.addStretch()


class QuickActionPanel(QFrame):
    """Panel für schnelle Aktionen auf dem Dashboard."""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("quickActionPanel")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        title_label = QLabel("Schnellaktionen")
        title_label.setObjectName("infoPanelTitle")
        layout.addWidget(title_label)

        button_row = QHBoxLayout()
        button_row.setSpacing(12)

        self.add_item_button = QPushButton("Artikel hinzufügen")
        self.add_item_button.setObjectName("primaryButton")

        self.stock_button = QPushButton("Bestand ändern")
        self.stock_button.setObjectName("secondaryButton")

        self.report_button = QPushButton("Report öffnen")
        self.report_button.setObjectName("secondaryButton")

        button_row.addWidget(self.add_item_button)
        button_row.addWidget(self.stock_button)
        button_row.addWidget(self.report_button)

        layout.addLayout(button_row)
        layout.addStretch()


class DashboardPage(QWidget):
    """Dashboard-Startseite der Anwendung."""

    def __init__(self) -> None:
        super().__init__()
        self._create_ui()

    def _create_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)

        header_widget = self._create_header_section()
        stats_widget = self._create_stats_section()
        lower_widget = self._create_lower_section()

        main_layout.addWidget(header_widget)
        main_layout.addWidget(stats_widget)
        main_layout.addWidget(lower_widget)
        main_layout.addStretch()

    def _create_header_section(self) -> QWidget:
        """Erstellt den oberen Begrüßungsbereich."""
        header = QFrame()
        header.setObjectName("dashboardHeader")
        header.setMinimumHeight(150)

        layout = QVBoxLayout(header)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(8)

        welcome_label = QLabel("Willkommen im FitnessGym Lager-Dashboard")
        welcome_label.setObjectName("dashboardWelcomeLabel")

        text_label = QLabel(
            "Behalte Bestände, Lagerbewegungen und kritische Artikel im Blick."
        )
        text_label.setObjectName("dashboardTextLabel")
        text_label.setWordWrap(True)

        layout.addWidget(welcome_label)
        layout.addWidget(text_label)
        layout.addStretch()

        return header

    def _create_stats_section(self) -> QWidget:
        """Erstellt die Statistik-Karten."""
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setHorizontalSpacing(16)
        layout.setVerticalSpacing(16)

        self.total_items_card = StatCard(
            "Artikel gesamt",
            "186",
            "Gesamte Anzahl aller aktuell verwalteten Lagerartikel.",
        )
        self.critical_items_card = StatCard(
            "Kritische Artikel",
            "7",
            "Artikel, die den Mindestbestand erreicht oder unterschritten haben.",
        )
        self.total_value_card = StatCard(
            "Lagerwert",
            "€ 12.480",
            "Geschätzter Gesamtwert des aktuellen Lagerbestandes.",
        )
        self.movements_today_card = StatCard(
            "Heutige Bewegungen",
            "23",
            "Warenein- und -ausgänge, die heute gebucht wurden.",
        )

        layout.addWidget(self.total_items_card, 0, 0)
        layout.addWidget(self.critical_items_card, 0, 1)
        layout.addWidget(self.total_value_card, 1, 0)
        layout.addWidget(self.movements_today_card, 1, 1)

        return widget

    def _create_lower_section(self) -> QWidget:
        """Erstellt den unteren Bereich mit Infos und Schnellaktionen."""
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setHorizontalSpacing(16)
        layout.setVerticalSpacing(16)

        self.warning_panel = InfoPanel(
            "Warnungen & Hinweise",
            [
                "7 Artikel liegen unter dem Mindestbestand.",
                "Protein Powder Vanilla muss bald nachbestellt werden.",
                "Resistance Bands sind fast ausverkauft.",
                "Nächste Inventur ist für Freitag geplant.",
            ],
        )

        self.activity_panel = InfoPanel(
            "Letzte Aktivitäten",
            [
                "08:15 Uhr – Wareneingang für Supplements gebucht.",
                "09:40 Uhr – 8 Handtücher aus Lager entnommen.",
                "10:05 Uhr – Reinigungsmittelbestand aktualisiert.",
                "11:30 Uhr – Report für Nachbestellungen geöffnet.",
            ],
        )

        self.quick_actions_panel = QuickActionPanel()

        layout.addWidget(self.warning_panel, 0, 0)
        layout.addWidget(self.activity_panel, 0, 1)
        layout.addWidget(self.quick_actions_panel, 1, 0, 1, 2)

        return widget
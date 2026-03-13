from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ReportCard(QFrame):
    """Karte für einen Report."""

    def __init__(self, title: str, description: str, button_text: str) -> None:
        super().__init__()
        self.setObjectName("reportCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("reportCardTitle")

        self.description_label = QLabel(description)
        self.description_label.setObjectName("reportCardDescription")
        self.description_label.setWordWrap(True)

        self.open_button = QPushButton(button_text)
        self.open_button.setObjectName("primaryButton")

        layout.addWidget(self.title_label)
        layout.addWidget(self.description_label)
        layout.addStretch()
        layout.addWidget(self.open_button)


class ReportsPage(QWidget):
    """Seite für Berichte und Auswertungen."""

    def __init__(self) -> None:
        super().__init__()
        self._create_ui()

    def _create_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)

        title_card = QFrame()
        title_card.setObjectName("dashboardHeader")

        title_layout = QVBoxLayout(title_card)
        title_layout.setContentsMargins(24, 24, 24, 24)
        title_layout.setSpacing(8)

        title = QLabel("Reports & Analysen")
        title.setObjectName("dashboardWelcomeLabel")

        subtitle = QLabel(
            "Erstelle Übersichten über Bestand, Nachbestellungen und Lagerbewegungen."
        )
        subtitle.setObjectName("dashboardTextLabel")
        subtitle.setWordWrap(True)

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        reports_widget = QWidget()
        reports_layout = QGridLayout(reports_widget)
        reports_layout.setContentsMargins(0, 0, 0, 0)
        reports_layout.setHorizontalSpacing(16)
        reports_layout.setVerticalSpacing(16)

        reports_layout.addWidget(
            ReportCard(
                "Lagerbestandsbericht",
                "Übersicht über alle aktuell im System befindlichen Artikel.",
                "Öffnen",
            ),
            0,
            0,
        )
        reports_layout.addWidget(
            ReportCard(
                "Nachbestellliste",
                "Zeigt alle kritischen Artikel, die nachbestellt werden sollten.",
                "Öffnen",
            ),
            0,
            1,
        )
        reports_layout.addWidget(
            ReportCard(
                "Bewegungsprotokoll",
                "Liste aller Warenein- und -ausgänge in einem Zeitraum.",
                "Öffnen",
            ),
            1,
            0,
        )
        reports_layout.addWidget(
            ReportCard(
                "Wertanalyse",
                "Geschätzter Lagerwert nach Kategorien und Gesamtbestand.",
                "Öffnen",
            ),
            1,
            1,
        )

        main_layout.addWidget(title_card)
        main_layout.addWidget(reports_widget)
        main_layout.addStretch()
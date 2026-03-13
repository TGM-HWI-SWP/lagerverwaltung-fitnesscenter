from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ui.pages.dashboard_page import DashboardPage
from ui.pages.inventory_page import InventoryPage
from ui.pages.movements_page import MovementsPage
from ui.pages.reports_page import ReportsPage
from ui.widgets.sidebar import Sidebar


class MainWindow(QMainWindow):
    """Hauptfenster der Lagerverwaltungsanwendung."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("FitnessCenter Lagerverwaltung")
        self.setMinimumSize(1400, 850)

        self._setup_window()
        self._create_pages()
        self._create_ui()
        self._connect_signals()

    def _setup_window(self) -> None:
        """Grundlegende Fenstereinstellungen."""
        self.statusBar().showMessage("System bereit")

    def _create_pages(self) -> None:
        """Erstellt alle Hauptseiten."""
        self.dashboard_page = DashboardPage()
        self.inventory_page = InventoryPage()
        self.movements_page = MovementsPage()
        self.reports_page = ReportsPage()

        self.page_stack = QStackedWidget()
        self.page_stack.setObjectName("pageStack")
        self.page_stack.addWidget(self.dashboard_page)
        self.page_stack.addWidget(self.inventory_page)
        self.page_stack.addWidget(self.movements_page)
        self.page_stack.addWidget(self.reports_page)

    def _create_ui(self) -> None:
        """Erstellt die komplette Benutzeroberfläche."""
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar()
        content_widget = self._create_content_area()

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(content_widget, 1)

    def _create_content_area(self) -> QWidget:
        """Erstellt den rechten Inhaltsbereich."""
        content_widget = QWidget()
        content_widget.setObjectName("contentWidget")

        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(18)

        header_widget = self._create_header()

        content_layout.addWidget(header_widget)
        content_layout.addWidget(self.page_stack, 1)

        return content_widget

    def _create_header(self) -> QWidget:
        """Erstellt den oberen Header-Bereich."""
        header_widget = QWidget()
        header_widget.setObjectName("headerWidget")
        header_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(4)

        self.title_label = QLabel("Dashboard")
        self.title_label.setObjectName("headerTitle")

        self.subtitle_label = QLabel(
            "Übersicht über Bestand, Bewegungen und Reports"
        )
        self.subtitle_label.setObjectName("headerSubtitle")

        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.subtitle_label)

        return header_widget

    def _connect_signals(self) -> None:
        """Verbindet Sidebar-Signale mit den Seiten."""
        self.sidebar.dashboard_clicked.connect(
            lambda: self.switch_page(
                0,
                "Dashboard",
                "Übersicht über Bestand, Bewegungen und Reports",
            )
        )
        self.sidebar.inventory_clicked.connect(
            lambda: self.switch_page(
                1,
                "Lagerbestand",
                "Alle Artikel, Suche, Filter und Bestandsverwaltung",
            )
        )
        self.sidebar.movements_clicked.connect(
            lambda: self.switch_page(
                2,
                "Lagerbewegungen",
                "Wareneingänge, Ausgänge und Inventuränderungen",
            )
        )
        self.sidebar.reports_clicked.connect(
            lambda: self.switch_page(
                3,
                "Reports",
                "Analysen, Bestandsberichte und Nachbestellungen",
            )
        )

    def switch_page(self, index: int, title: str, subtitle: str) -> None:
        """Wechselt die aktuelle Seite."""
        self.page_stack.setCurrentIndex(index)
        self.title_label.setText(title)
        self.subtitle_label.setText(subtitle)
        self.statusBar().showMessage(f"Aktive Seite: {title}")

    def keyPressEvent(self, event) -> None:
        """Optionale Shortcuts für Seitenwechsel."""
        if event.key() == Qt.Key.Key_F1:
            self.switch_page(
                0,
                "Dashboard",
                "Übersicht über Bestand, Bewegungen und Reports",
            )
        elif event.key() == Qt.Key.Key_F2:
            self.switch_page(
                1,
                "Lagerbestand",
                "Alle Artikel, Suche, Filter und Bestandsverwaltung",
            )
        elif event.key() == Qt.Key.Key_F3:
            self.switch_page(
                2,
                "Lagerbewegungen",
                "Wareneingänge, Ausgänge und Inventuränderungen",
            )
        elif event.key() == Qt.Key.Key_F4:
            self.switch_page(
                3,
                "Reports",
                "Analysen, Bestandsberichte und Nachbestellungen",
            )
        else:
            super().keyPressEvent(event)
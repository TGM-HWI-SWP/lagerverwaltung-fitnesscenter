from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.pages.dashboard_page import DashboardPage
from ui.pages.employees_page import EmployeesPage
from ui.pages.equipment_page import EquipmentPage
from ui.pages.members_page import MembersPage
from ui.pages.movements_page import MovementsPage
from ui.pages.products_page import ProductsPage
from ui.pages.reports_page import ReportsPage
from ui.pages.vending_page import VendingPage
from ui.widgets.animated_stack import AnimatedStackedWidget
from ui.widgets.sidebar import Sidebar


@dataclass(frozen=True)
class PageDefinition:
    """Beschreibt eine Hauptseite der Anwendung."""

    key: str
    title: str
    subtitle: str
    factory: Callable[[Optional[object]], QWidget]


class MainWindow(QMainWindow):
    """Zentrales Hauptfenster der Fitnesscenter-Management-Software."""

    def __init__(self, controller: Optional[object] = None) -> None:
        super().__init__()

        self.controller = controller
        self._pages: list[tuple[PageDefinition, QWidget]] = []

        self._configure_window()
        self._build_page_registry()
        self._create_ui()
        self._create_actions()
        self._connect_signals()
        self._show_default_page()
        self._animate_window_fade_in()

    def _configure_window(self) -> None:
        """Setzt grundlegende Eigenschaften des Fensters."""
        self.setWindowTitle("Fitnesscenter Management Suite")
        self.setMinimumSize(1500, 900)
        self.resize(1600, 950)
        self.statusBar().showMessage("System bereit")

    def _build_page_registry(self) -> None:
        """Definiert alle Hauptbereiche zentral an einer Stelle."""
        self.page_definitions: list[PageDefinition] = [
            PageDefinition(
                key="dashboard",
                title="Dashboard",
                subtitle="Zentrale Übersicht über Mitglieder, Mitarbeiter, Produkte, Geräte und Lagerbewegungen",
                factory=lambda controller: DashboardPage(controller=controller),
            ),
            PageDefinition(
                key="members",
                title="Mitglieder",
                subtitle="Verwaltung von Mitgliedern, Kontaktdaten, Mitgliedschaftstypen und Aktivstatus",
                factory=lambda controller: MembersPage(controller=controller),
            ),
            PageDefinition(
                key="employees",
                title="Mitarbeiter",
                subtitle="Verwaltung von Mitarbeitern, Rollen, Kontaktdaten und Zuständigkeiten",
                factory=lambda controller: EmployeesPage(controller=controller),
            ),
            PageDefinition(
                key="products",
                title="Produkte",
                subtitle="Produktdaten, Lagerbestand, Preise, Kategorien und Zusatzinformationen",
                factory=lambda controller: ProductsPage(controller=controller),
            ),
            PageDefinition(
                key="movements",
                title="Lagerbewegungen",
                subtitle="Warenein- und -ausgänge, Korrekturen, Gründe und verantwortliche Personen",
                factory=lambda controller: MovementsPage(controller=controller),
            ),
            PageDefinition(
                key="equipment",
                title="Geräte",
                subtitle="Geräteübersicht mit Typ, Standort, Status und Mitarbeiterzuweisung",
                factory=lambda controller: EquipmentPage(controller=controller),
            ),
            PageDefinition(
                key="vending",
                title="Automaten",
                subtitle="Vending Machines mit Standort, Typ, Aktivstatus und Zuständigkeit",
                factory=lambda controller: VendingPage(controller=controller),
            ),
            PageDefinition(
                key="reports",
                title="Reports",
                subtitle="Management-Berichte, Auswertungen und zusammengefasste Analysen",
                factory=lambda controller: ReportsPage(controller=controller),
            ),
        ]

    def _create_ui(self) -> None:
        """Baut die komplette Oberfläche des Hauptfensters."""
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.sidebar = Sidebar()
        self.content_area = self._create_content_area()

        root_layout.addWidget(self.sidebar)
        root_layout.addWidget(self.content_area, 1)

    def _create_content_area(self) -> QWidget:
        """Erstellt den rechten Inhaltsbereich."""
        content_widget = QWidget()
        content_widget.setObjectName("contentWidget")

        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 20, 24, 20)
        content_layout.setSpacing(18)

        self.header_card = self._create_header_card()
        self.page_container = self._create_page_container()

        content_layout.addWidget(self.header_card)
        content_layout.addWidget(self.page_container, 1)

        return content_widget

    def _create_header_card(self) -> QWidget:
        """Erstellt den Kopfbereich über den Seiten."""
        header_card = QFrame()
        header_card.setObjectName("headerCard")
        header_card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        layout = QVBoxLayout(header_card)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(6)

        self.header_title_label = QLabel()
        self.header_title_label.setObjectName("headerTitle")

        self.header_subtitle_label = QLabel()
        self.header_subtitle_label.setObjectName("headerSubtitle")
        self.header_subtitle_label.setWordWrap(True)

        layout.addWidget(self.header_title_label)
        layout.addWidget(self.header_subtitle_label)

        return header_card

    def _create_page_container(self) -> QWidget:
        """Erstellt den Container mit animiertem Seiten-Stack."""
        container = QFrame()
        container.setObjectName("pageContainer")

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.page_stack = AnimatedStackedWidget()
        self.page_stack.setObjectName("pageStack")
        self.page_stack.set_animation_duration(320)

        self._instantiate_pages()

        layout.addWidget(self.page_stack)
        return container

    def _instantiate_pages(self) -> None:
        """Erzeugt alle Seiten anhand der zentralen Definition."""
        self._pages.clear()

        for definition in self.page_definitions:
            page_widget = definition.factory(self.controller)
            self._pages.append((definition, page_widget))
            self.page_stack.addWidget(page_widget)

    def _create_actions(self) -> None:
        """Erstellt globale Aktionen und Tastenkürzel."""
        self.refresh_action = QAction("Aktualisieren", self)
        self.refresh_action.setShortcut(QKeySequence("F5"))
        self.refresh_action.triggered.connect(self.refresh_current_page)
        self.addAction(self.refresh_action)

    def _connect_signals(self) -> None:
        """Verbindet Sidebar und Hauptfenster."""
        self.sidebar.page_selected.connect(self.open_page_by_index)

    def _show_default_page(self) -> None:
        """Zeigt beim Start die Dashboard-Seite."""
        self.open_page_by_index(0, animated=False)

    def open_page_by_index(self, index: int, animated: bool = True) -> None:
        """Öffnet eine Seite anhand ihres Index."""
        if not 0 <= index < len(self._pages):
            return

        definition, _page = self._pages[index]

        current_index = self.page_stack.currentIndex()
        if animated and index != current_index:
            self.page_stack.slide_to_index(index)
        else:
            self.page_stack.setCurrentIndex(index)

        self._update_header(definition.title, definition.subtitle)
        self._animate_header_change()
        self._update_status(definition.title)
        self.sidebar.set_active_index(index)

    def open_page_by_key(self, key: str) -> None:
        """Öffnet eine Seite anhand ihres internen Schlüssels."""
        for index, (definition, _page) in enumerate(self._pages):
            if definition.key == key:
                self.open_page_by_index(index)
                return

    def _update_header(self, title: str, subtitle: str) -> None:
        """Aktualisiert den Header."""
        self.header_title_label.setText(title)
        self.header_subtitle_label.setText(subtitle)

    def _update_status(self, current_area: str) -> None:
        """Aktualisiert die Statusleiste."""
        self.statusBar().showMessage(f"Aktiver Bereich: {current_area}")

    def refresh_current_page(self) -> None:
        """Aktualisiert die aktuell sichtbare Seite, falls unterstützt."""
        current_widget = self.page_stack.currentWidget()

        if current_widget is None:
            self.statusBar().showMessage("Keine aktive Seite gefunden")
            return

        refresh_method = getattr(current_widget, "refresh_data", None)

        if callable(refresh_method):
            refresh_method()
            self.statusBar().showMessage("Aktuelle Seite wurde aktualisiert")
        else:
            self.statusBar().showMessage(
                "Für diese Seite ist noch keine Aktualisierung verfügbar"
            )

    def _animate_window_fade_in(self) -> None:
        """Blendet das Hauptfenster weich ein."""
        self.window_opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.window_opacity_effect)

        self.fade_animation = QPropertyAnimation(
            self.window_opacity_effect,
            b"opacity",
            self,
        )
        self.fade_animation.setDuration(450)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.fade_animation.start()

    def _animate_header_change(self) -> None:
        """Lässt den Header beim Seitenwechsel weich einblenden."""
        effect = QGraphicsOpacityEffect(self.header_card)
        self.header_card.setGraphicsEffect(effect)

        animation = QPropertyAnimation(effect, b"opacity", self)
        animation.setDuration(220)
        animation.setStartValue(0.35)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        animation.start()

        self._header_animation = animation

    def keyPressEvent(self, event) -> None:
        """Schneller Seitenwechsel über Funktionstasten."""
        key_map = {
            Qt.Key.Key_F1: 0,
            Qt.Key.Key_F2: 1,
            Qt.Key.Key_F3: 2,
            Qt.Key.Key_F4: 3,
            Qt.Key.Key_F6: 4,
            Qt.Key.Key_F7: 5,
            Qt.Key.Key_F8: 6,
            Qt.Key.Key_F9: 7,
        }

        target_index = key_map.get(event.key())

        if target_index is not None:
            self.open_page_by_index(target_index)
            return

        super().keyPressEvent(event)
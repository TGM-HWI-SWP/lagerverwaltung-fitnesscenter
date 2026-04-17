from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PyQt6.QtGui import QAction, QKeyEvent, QKeySequence
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.auth.auth_service import AuthService
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
    factory: Callable[[Any | None], QWidget]


class MainWindow(QMainWindow):
    """Zentrales Hauptfenster der Fitnesscenter-Management-Software."""

    PAGE_SHORTCUTS = {
        Qt.Key.Key_F1: 0,
        Qt.Key.Key_F2: 1,
        Qt.Key.Key_F3: 2,
        Qt.Key.Key_F4: 3,
        Qt.Key.Key_F6: 4,
        Qt.Key.Key_F7: 5,
        Qt.Key.Key_F8: 6,
        Qt.Key.Key_F9: 7,
    }

    def __init__(self, controller: Any | None = None) -> None:
        super().__init__()

        self.controller = controller
        self.auth_service = AuthService()
        self.current_username = self.auth_service.get_logged_in_user()

        self._pages: list[tuple[PageDefinition, QWidget]] = []
        self._page_index_by_key: dict[str, int] = {}

        self.login_window: QWidget | None = None
        self.window_opacity_effect: QGraphicsOpacityEffect | None = None
        self.fade_animation: QPropertyAnimation | None = None
        self.header_opacity_effect: QGraphicsOpacityEffect | None = None
        self.header_animation: QPropertyAnimation | None = None

        self.sidebar: Sidebar | None = None
        self.content_area: QWidget | None = None
        self.header_card: QFrame | None = None
        self.page_container: QFrame | None = None
        self.page_stack: AnimatedStackedWidget | None = None

        self.header_title_label: QLabel | None = None
        self.header_subtitle_label: QLabel | None = None
        self.user_label: QLabel | None = None
        self.logout_button: QPushButton | None = None

        self._configure_window()
        self._build_page_registry()
        self._create_ui()
        self._load_styles()
        self._prepare_header_animation()
        self._create_actions()
        self._connect_signals()
        self._show_default_page()
        self._animate_window_fade_in()

    def _configure_window(self) -> None:
        """Setzt grundlegende Eigenschaften des Fensters."""
        self.setWindowTitle("Fitnesscenter Management Suite")
        self.setMinimumSize(1500, 900)
        self.resize(1600, 950)
        self._show_status("Bereit | F1-F9 Navigation | F5 Aktualisieren")

    def _load_styles(self) -> None:
        """Lädt das Hauptstylesheet, falls vorhanden."""
        qss_path = Path(__file__).resolve().parent / "styles" / "main.qss"

        if qss_path.exists():
            try:
                with qss_path.open("r", encoding="utf-8") as file:
                    self.setStyleSheet(file.read())
            except OSError:
                self._show_status("Stylesheet konnte nicht geladen werden")

    def _build_page_registry(self) -> None:
        """Definiert alle Hauptbereiche zentral an einer Stelle."""
        self.page_definitions: list[PageDefinition] = [
            PageDefinition(
                key="dashboard",
                title="Dashboard",
                subtitle="Zentrale Übersicht über Mitglieder, Mitarbeiter, Produkte, Geräte und Lagerbewegungen",
                factory=lambda controller: DashboardPage(
                    controller=controller,
                    navigator=self.open_page_by_key,
                    quick_action_handler=self.handle_dashboard_quick_action,
                    snapshot_provider=self.get_dashboard_snapshot,
                    health_provider=self.get_system_health,
                ),
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
        content_layout.setSpacing(20)

        self.header_card = self._create_header_card()
        self.page_container = self._create_page_container()

        content_layout.addWidget(self.header_card, 0)
        content_layout.addWidget(self.page_container, 1)

        return content_widget

    def _create_header_card(self) -> QFrame:
        """Erstellt den stabilen Kopfbereich über den Seiten."""
        header_card = QFrame()
        header_card.setObjectName("headerCard")
        header_card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        header_card.setMinimumHeight(110)
        header_card.setMaximumHeight(130)

        outer_layout = QHBoxLayout(header_card)
        outer_layout.setContentsMargins(24, 18, 24, 18)
        outer_layout.setSpacing(16)

        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)

        self.header_title_label = QLabel("Dashboard")
        self.header_title_label.setObjectName("headerTitle")
        self.header_title_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        self.header_subtitle_label = QLabel("Die wichtigsten Bereiche im Überblick.")
        self.header_subtitle_label.setObjectName("headerSubtitle")
        self.header_subtitle_label.setWordWrap(True)
        self.header_subtitle_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        text_layout.addStretch()
        text_layout.addWidget(self.header_title_label)
        text_layout.addWidget(self.header_subtitle_label)
        text_layout.addStretch()

        right_layout = QVBoxLayout()
        right_layout.setSpacing(6)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        username_text = self.current_username if self.current_username else "Gast"
        self.user_label = QLabel(f"Angemeldet als: {username_text}")
        self.user_label.setObjectName("userInfoLabel")
        self.user_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.logout_button = QPushButton("Abmelden")
        self.logout_button.setObjectName("logoutButton")
        self.logout_button.clicked.connect(self.logout)

        right_layout.addStretch()
        right_layout.addWidget(self.user_label, alignment=Qt.AlignmentFlag.AlignRight)
        right_layout.addWidget(self.logout_button, alignment=Qt.AlignmentFlag.AlignRight)
        right_layout.addStretch()

        outer_layout.addLayout(text_layout, 1)
        outer_layout.addLayout(right_layout, 0)

        return header_card

    def _create_page_container(self) -> QFrame:
        """Erstellt den Container mit animiertem Seiten-Stack."""
        container = QFrame()
        container.setObjectName("pageContainer")

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.page_stack = AnimatedStackedWidget()
        self.page_stack.setObjectName("pageStack")
        self.page_stack.set_animation_duration(340)

        self._instantiate_pages()

        layout.addWidget(self.page_stack)
        return container

    def _instantiate_pages(self) -> None:
        """Erzeugt alle Seiten anhand der zentralen Definition."""
        if self.page_stack is None:
            return

        self._pages.clear()
        self._page_index_by_key.clear()

        for index, definition in enumerate(self.page_definitions):
            try:
                page_widget = definition.factory(self.controller)
            except Exception as error:
                page_widget = self._build_error_page(definition.title, str(error))

            self._pages.append((definition, page_widget))
            self._page_index_by_key[definition.key] = index
            self.page_stack.addWidget(page_widget)

    def _build_error_page(self, page_title: str, error_text: str) -> QWidget:
        """Erstellt eine Fehlerseite, falls eine Page nicht geladen werden kann."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(14)

        title_label = QLabel(f"Seite konnte nicht geladen werden: {page_title}")
        title_label.setObjectName("errorPageTitle")
        title_label.setWordWrap(True)

        info_label = QLabel("Beim Erzeugen dieser Seite ist ein Fehler aufgetreten.")
        info_label.setObjectName("errorPageSubtitle")
        info_label.setWordWrap(True)

        error_label = QLabel(error_text)
        error_label.setObjectName("errorPageText")
        error_label.setWordWrap(True)

        layout.addStretch()
        layout.addWidget(title_label)
        layout.addWidget(info_label)
        layout.addWidget(error_label)
        layout.addStretch()

        return widget

    def _prepare_header_animation(self) -> None:
        """Header-Animation deaktiviert, damit der Header immer stabil sichtbar bleibt."""
        self.header_opacity_effect = None
        self.header_animation = None

    def _create_actions(self) -> None:
        """Erstellt globale Aktionen und Tastenkürzel."""
        self.refresh_action = QAction("Aktualisieren", self)
        self.refresh_action.setShortcut(QKeySequence("F5"))
        self.refresh_action.triggered.connect(self.refresh_current_page)
        self.addAction(self.refresh_action)

        self.dashboard_action = QAction("Zum Dashboard", self)
        self.dashboard_action.setShortcut(QKeySequence("Ctrl+1"))
        self.dashboard_action.triggered.connect(lambda: self.open_page_by_key("dashboard"))
        self.addAction(self.dashboard_action)

        self.members_action = QAction("Zu Mitglieder", self)
        self.members_action.setShortcut(QKeySequence("Ctrl+2"))
        self.members_action.triggered.connect(lambda: self.open_page_by_key("members"))
        self.addAction(self.members_action)

        self.products_action = QAction("Zu Produkte", self)
        self.products_action.setShortcut(QKeySequence("Ctrl+3"))
        self.products_action.triggered.connect(lambda: self.open_page_by_key("products"))
        self.addAction(self.products_action)

    def _connect_signals(self) -> None:
        """Verbindet Sidebar und Hauptfenster."""
        if self.sidebar is not None:
            self.sidebar.page_selected.connect(self.open_page_by_index)

    def _show_default_page(self) -> None:
        """Zeigt beim Start die Dashboard-Seite."""
        self.open_page_by_index(0, animated=False)

    def open_page_by_index(self, index: int, animated: bool = True) -> None:
        """Öffnet eine Seite anhand ihres Index."""
        if not 0 <= index < len(self._pages):
            self._show_status("Ungültiger Seitenindex")
            return

        if self.page_stack is None or self.sidebar is None:
            return

        definition, _page = self._pages[index]
        current_index = self.page_stack.currentIndex()

        try:
            if animated and index != current_index:
                self.page_stack.slide_to_index(index)
            else:
                self.page_stack.setCurrentIndex(index)

            self._update_header(definition.title, definition.subtitle)
            self._animate_header_change()
            self._update_status(definition.title)
            self.sidebar.set_active_index(index)
        except Exception as error:
            self._show_status(f"Seite konnte nicht geöffnet werden: {error}")

    def open_page_by_key(self, key: str, animated: bool = True) -> None:
        """Öffnet eine Seite anhand ihres internen Schlüssels."""
        index = self._page_index_by_key.get(key)

        if index is None:
            self._show_status(f"Seite '{key}' wurde nicht gefunden")
            return

        self.open_page_by_index(index, animated=animated)

    def _update_header(self, title: str, subtitle: str) -> None:
        """Aktualisiert den Header."""
        if self.header_title_label is not None:
            self.header_title_label.setText(title)

        if self.header_subtitle_label is not None:
            self.header_subtitle_label.setText(subtitle)

    def update_user_display(self, username: str | None = None) -> None:
        """Aktualisiert die Anzeige des angemeldeten Benutzers."""
        self.current_username = username or self.auth_service.get_logged_in_user()

        if self.user_label is not None:
            shown_name = self.current_username if self.current_username else "Gast"
            self.user_label.setText(f"Angemeldet als: {shown_name}")

    def _update_status(self, current_area: str) -> None:
        """Aktualisiert die Statusleiste."""
        self._show_status(f"Aktiver Bereich: {current_area} | F5 Aktualisieren")

    def _show_status(self, message: str) -> None:
        """Zeigt eine Nachricht in der Statusleiste."""
        self.statusBar().showMessage(message)

    def get_dashboard_snapshot(self) -> dict[str, Any]:
        """
        Liefert Dashboard-Daten für Live-Updates, Alerts und Analytics.
        Kann später direkt an echte Businesslogik gebunden werden.
        """
        return {
            "members": 124,
            "employees": 18,
            "products": 56,
            "equipment": 32,
            "vending": 6,
            "low_stock": 4,
            "member_trend": [98, 104, 109, 113, 118, 124],
            "stock_trend": [70, 68, 66, 61, 59, 56],
            "alerts": [
                "Kritischer Lagerbestand bei 4 Produkten",
                "1 Automat benötigt Sichtprüfung",
                "2 Geräte wurden heute aktualisiert",
            ],
            "activities": [
                "Neuer Mitarbeiter wurde angelegt",
                "Lagerbestand von Proteinriegeln aktualisiert",
                "2 Geräte wurden als verfügbar markiert",
                "Automat im Eingangsbereich wurde geprüft",
            ],
        }

    def get_system_health(self) -> dict[str, str]:
        """
        Liefert den Gesamtzustand des Systems.
        status: ok | warning | critical
        """
        snapshot = self.get_dashboard_snapshot()
        low_stock = snapshot.get("low_stock", 0)

        if low_stock >= 6:
            return {
                "status": "critical",
                "label": "Kritisch",
                "message": "Mehrere Bestände liegen im kritischen Bereich.",
            }

        if low_stock >= 3:
            return {
                "status": "warning",
                "label": "Warnung",
                "message": "Einige Produkte sollten bald nachbestellt werden.",
            }

        return {
            "status": "ok",
            "label": "Stabil",
            "message": "Alle Kernbereiche laufen im normalen Bereich.",
        }

    def handle_dashboard_quick_action(self, action_key: str) -> None:
        """Führt Quick Actions aus dem Dashboard aus."""
        action_map = {
            "new_member": ("members", "Quick Action: Mitglieder-Seite geöffnet"),
            "new_product": ("products", "Quick Action: Produkte-Seite geöffnet"),
            "new_movement": ("movements", "Quick Action: Lagerbewegungen geöffnet"),
            "reports": ("reports", "Quick Action: Reports geöffnet"),
            "employees": ("employees", "Quick Action: Mitarbeiter-Seite geöffnet"),
        }

        target = action_map.get(action_key)
        if target is None:
            self._show_status(f"Unbekannte Quick Action: {action_key}")
            return

        page_key, message = target
        self.open_page_by_key(page_key)
        self._show_status(message)

    def refresh_current_page(self) -> None:
        """Aktualisiert die aktuell sichtbare Seite, falls unterstützt."""
        if self.page_stack is None:
            self._show_status("Keine aktive Seite gefunden")
            return

        current_widget = self.page_stack.currentWidget()

        if current_widget is None:
            self._show_status("Keine aktive Seite gefunden")
            return

        refresh_method = getattr(current_widget, "refresh_data", None)

        if callable(refresh_method):
            try:
                refresh_method()
                self._show_status("Aktuelle Seite wurde aktualisiert")
            except Exception as error:
                self._show_status(f"Fehler beim Aktualisieren: {error}")
        else:
            self._show_status("Für diese Seite ist noch keine Aktualisierung verfügbar")

    def logout(self) -> None:
        """Meldet den aktuellen Benutzer ab und zeigt wieder das Login-Fenster."""
        answer = QMessageBox.question(
            self,
            "Abmelden",
            "Möchten Sie sich wirklich abmelden?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            self.auth_service.clear_session()

            from ui.auth.login_window import LoginWindow

            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Beim Abmelden ist ein Fehler aufgetreten:\n{error}",
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
        """Keine Header-Animation, damit nichts verschwindet."""
        return

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Schneller Seitenwechsel über Funktionstasten."""
        target_index = self.PAGE_SHORTCUTS.get(event.key())

        if target_index is not None:
            self.open_page_by_index(target_index)
            return

        super().keyPressEvent(event)

    def closeEvent(self, event) -> None:
        """Räumt Animationen sauber auf."""
        if self.fade_animation is not None:
            self.fade_animation.stop()

        if self.header_animation is not None:
            self.header_animation.stop()

        super().closeEvent(event)
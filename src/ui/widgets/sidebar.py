from __future__ import annotations

from dataclasses import dataclass

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


@dataclass(frozen=True)
class SidebarEntry:
    """Beschreibt einen Eintrag in der Sidebar."""

    title: str
    icon: str


class SidebarButton(QPushButton):
    """Ein einzelner Navigationsbutton der Sidebar."""

    def __init__(self, text: str, icon: str, index: int) -> None:
        super().__init__(f"{icon}  {text}")
        self.index = index
        self.base_text = text
        self.icon_text = icon

        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(54)
        self.setObjectName("sidebarButton")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setToolTip(text)


class Sidebar(QWidget):
    """Linke Navigationsleiste der Anwendung."""

    page_selected = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()

        self._buttons: list[SidebarButton] = []
        self._entries = self._build_entries()

        self.setObjectName("sidebar")
        self.setFixedWidth(300)

        self._create_ui()
        self._connect_signals()

    def _build_entries(self) -> list[SidebarEntry]:
        """Definiert alle Sidebar-Einträge zentral."""
        return [
            SidebarEntry("Dashboard", "◉"),
            SidebarEntry("Mitglieder", "👥"),
            SidebarEntry("Mitarbeiter", "🧑‍💼"),
            SidebarEntry("Produkte", "📦"),
            SidebarEntry("Lagerbewegungen", "↔"),
            SidebarEntry("Geräte", "🏋"),
            SidebarEntry("Automaten", "▣"),
            SidebarEntry("Reports", "📊"),
        ]

    def _create_ui(self) -> None:
        """Erstellt den kompletten Aufbau der Sidebar."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 22, 20, 22)
        main_layout.setSpacing(14)

        self._create_branding(main_layout)
        self._create_navigation_card(main_layout)
        self._create_footer_card(main_layout)

    def _create_branding(self, layout: QVBoxLayout) -> None:
        """Erstellt den Branding-Bereich."""
        logo_card = QFrame()
        logo_card.setObjectName("logoFrame")

        logo_layout = QVBoxLayout(logo_card)
        logo_layout.setContentsMargins(18, 18, 18, 18)
        logo_layout.setSpacing(4)

        badge_label = QLabel("FITNESS SUITE")
        badge_label.setObjectName("logoBadge")

        title_label = QLabel("FITNESSCENTER")
        title_label.setObjectName("logoTitle")

        subtitle_label = QLabel("Management Suite")
        subtitle_label.setObjectName("logoSubtitle")

        section_label = QLabel("Navigation")
        section_label.setObjectName("navSectionLabel")

        logo_layout.addWidget(badge_label, alignment=Qt.AlignmentFlag.AlignLeft)
        logo_layout.addWidget(title_label)
        logo_layout.addWidget(subtitle_label)

        layout.addWidget(logo_card)
        layout.addSpacing(6)
        layout.addWidget(section_label)

    def _create_navigation_card(self, layout: QVBoxLayout) -> None:
        """Erstellt die Kartenfläche mit den Navigationsbuttons."""
        nav_card = QFrame()
        nav_card.setObjectName("sidebarNavCard")

        nav_layout = QVBoxLayout(nav_card)
        nav_layout.setContentsMargins(10, 10, 10, 10)
        nav_layout.setSpacing(8)

        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        for index, entry in enumerate(self._entries):
            button = SidebarButton(
                text=entry.title,
                icon=entry.icon,
                index=index,
            )
            self.button_group.addButton(button)
            self._buttons.append(button)
            nav_layout.addWidget(button)

        if self._buttons:
            self._buttons[0].setChecked(True)

        layout.addWidget(nav_card, 1)

    def _create_footer_card(self, layout: QVBoxLayout) -> None:
        """Erstellt die kleine Info-Karte im unteren Bereich."""
        layout.addItem(
            QSpacerItem(
                20,
                20,
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Expanding,
            )
        )

        info_card = QFrame()
        info_card.setObjectName("sidebarInfoCard")

        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(16, 16, 16, 16)
        info_layout.setSpacing(6)

        status_badge = QLabel("● Online")
        status_badge.setObjectName("sidebarStatusBadge")

        info_title = QLabel("Systemstatus")
        info_title.setObjectName("sidebarInfoTitle")

        self.info_text = QLabel("GUI aktiv\nNavigation geladen")
        self.info_text.setObjectName("sidebarInfoText")

        hint_text = QLabel("F1–F9 für schnellen Seitenwechsel\nF5 zum Aktualisieren")
        hint_text.setWordWrap(True)
        hint_text.setObjectName("sidebarHintText")

        info_layout.addWidget(status_badge, alignment=Qt.AlignmentFlag.AlignLeft)
        info_layout.addWidget(info_title)
        info_layout.addWidget(self.info_text)
        info_layout.addSpacing(4)
        info_layout.addWidget(hint_text)

        layout.addWidget(info_card)

    def _connect_signals(self) -> None:
        """Verbindet Buttons mit dem zentralen page_selected-Signal."""
        for button in self._buttons:
            button.clicked.connect(self._emit_page_selected)

    def _emit_page_selected(self) -> None:
        """Sendet den Index des gerade aktiven Buttons."""
        button = self.sender()

        if isinstance(button, SidebarButton):
            self.page_selected.emit(button.index)

    def set_active_index(self, index: int) -> None:
        """Markiert den aktiven Navigationspunkt."""
        if 0 <= index < len(self._buttons):
            self._buttons[index].setChecked(True)

    def set_status_text(self, text: str) -> None:
        """Aktualisiert den Text im unteren Statusbereich."""
        self.info_text.setText(text)

    def button_count(self) -> int:
        """Gibt die Anzahl der Navigationsbuttons zurück."""
        return len(self._buttons)

    def button_texts(self) -> list[str]:
        """Gibt alle sichtbaren Navigationsbezeichnungen zurück."""
        return [button.base_text for button in self._buttons]
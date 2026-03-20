from __future__ import annotations

from typing import List

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


class SidebarButton(QPushButton):
    """Ein einzelner Navigationsbutton der Sidebar."""

    def __init__(self, text: str, index: int) -> None:
        super().__init__(text)
        self.index = index

        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(52)
        self.setObjectName("sidebarButton")


class Sidebar(QWidget):
    """Linke Navigationsleiste der Anwendung."""

    page_selected = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()

        self._buttons: List[SidebarButton] = []

        self.setObjectName("sidebar")
        self.setFixedWidth(285)

        self._create_ui()
        self._connect_signals()

    def _create_ui(self) -> None:
        """Erstellt den kompletten Aufbau der Sidebar."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 24, 20, 24)
        main_layout.setSpacing(14)

        self._create_branding(main_layout)
        self._create_navigation(main_layout)
        self._create_footer_card(main_layout)

    def _create_branding(self, layout: QVBoxLayout) -> None:
        """Erstellt den Branding-Bereich."""
        logo_card = QFrame()
        logo_card.setObjectName("logoFrame")

        logo_layout = QVBoxLayout(logo_card)
        logo_layout.setContentsMargins(16, 16, 16, 16)
        logo_layout.setSpacing(4)

        title_label = QLabel("FITNESSCENTER")
        title_label.setObjectName("logoTitle")

        subtitle_label = QLabel("Management Suite")
        subtitle_label.setObjectName("logoSubtitle")

        section_label = QLabel("Navigation")
        section_label.setObjectName("navSectionLabel")

        logo_layout.addWidget(title_label)
        logo_layout.addWidget(subtitle_label)

        layout.addWidget(logo_card)
        layout.addSpacing(8)
        layout.addWidget(section_label)

    def _create_navigation(self, layout: QVBoxLayout) -> None:
        """Erstellt alle Navigationsbuttons."""
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        entries = [
            "Dashboard",
            "Mitglieder",
            "Mitarbeiter",
            "Produkte",
            "Lagerbewegungen",
            "Geräte",
            "Automaten",
            "Reports",
        ]

        for index, text in enumerate(entries):
            button = SidebarButton(text=text, index=index)
            self.button_group.addButton(button)
            self._buttons.append(button)
            layout.addWidget(button)

        if self._buttons:
            self._buttons[0].setChecked(True)

        layout.addItem(
            QSpacerItem(
                20,
                20,
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Expanding,
            )
        )

    def _create_footer_card(self, layout: QVBoxLayout) -> None:
        """Erstellt die kleine Info-Karte im unteren Bereich."""
        info_card = QFrame()
        info_card.setObjectName("sidebarInfoCard")

        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(16, 16, 16, 16)
        info_layout.setSpacing(6)

        info_title = QLabel("Systemstatus")
        info_title.setObjectName("sidebarInfoTitle")

        info_text = QLabel("GUI aktiv\nNavigation geladen")
        info_text.setObjectName("sidebarInfoText")

        hint_text = QLabel("F1–F9 für schnellen Seitenwechsel verwenden.")
        hint_text.setWordWrap(True)
        hint_text.setObjectName("sidebarHintText")

        info_layout.addWidget(info_title)
        info_layout.addWidget(info_text)
        info_layout.addSpacing(4)
        info_layout.addWidget(hint_text)

        layout.addWidget(info_card)

    def _connect_signals(self) -> None:
        """Verbindet Buttons mit dem zentralen page_selected-Signal."""
        for button in self._buttons:
            button.clicked.connect(
                lambda checked=False, idx=button.index: self.page_selected.emit(idx)
            )

    def set_active_index(self, index: int) -> None:
        """Markiert den aktiven Navigationspunkt."""
        if 0 <= index < len(self._buttons):
            self._buttons[index].setChecked(True)
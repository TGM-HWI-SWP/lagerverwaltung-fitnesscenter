from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QLabel,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class SidebarButton(QPushButton):
    """Ein einzelner Navigationsbutton der Sidebar."""

    def __init__(self, text: str) -> None:
        super().__init__(text)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(52)
        self.setObjectName("sidebarButton")


class Sidebar(QWidget):
    """Linke Navigationsleiste der Anwendung."""

    dashboard_clicked = pyqtSignal()
    inventory_clicked = pyqtSignal()
    movements_clicked = pyqtSignal()
    reports_clicked = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("sidebar")
        self.setFixedWidth(280)

        self._create_ui()
        self._connect_signals()

    def _create_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 24, 20, 24)
        main_layout.setSpacing(14)

        self._create_branding(main_layout)
        self._create_navigation(main_layout)
        self._create_bottom_card(main_layout)

    def _create_branding(self, layout: QVBoxLayout) -> None:
        logo_frame = QFrame()
        logo_frame.setObjectName("logoFrame")

        logo_layout = QVBoxLayout(logo_frame)
        logo_layout.setContentsMargins(14, 14, 14, 14)
        logo_layout.setSpacing(4)

        self.logo_title = QLabel("FITNESSGYM")
        self.logo_title.setObjectName("logoTitle")

        self.logo_subtitle = QLabel("Inventory Suite")
        self.logo_subtitle.setObjectName("logoSubtitle")

        self.nav_label = QLabel("Navigation")
        self.nav_label.setObjectName("navSectionLabel")

        logo_layout.addWidget(self.logo_title)
        logo_layout.addWidget(self.logo_subtitle)

        layout.addWidget(logo_frame)
        layout.addSpacing(8)
        layout.addWidget(self.nav_label)

    def _create_navigation(self, layout: QVBoxLayout) -> None:
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        self.dashboard_button = SidebarButton("Dashboard")
        self.inventory_button = SidebarButton("Lagerbestand")
        self.movements_button = SidebarButton("Lagerbewegungen")
        self.reports_button = SidebarButton("Reports")

        self.dashboard_button.setChecked(True)

        buttons = [
            self.dashboard_button,
            self.inventory_button,
            self.movements_button,
            self.reports_button,
        ]

        for button in buttons:
            self.button_group.addButton(button)
            layout.addWidget(button)

        layout.addItem(
            QSpacerItem(
                20,
                20,
                QSizePolicy.Policy.Minimum,
                QSizePolicy.Policy.Expanding,
            )
        )

    def _create_bottom_card(self, layout: QVBoxLayout) -> None:
        bottom_card = QFrame()
        bottom_card.setObjectName("sidebarInfoCard")

        card_layout = QVBoxLayout(bottom_card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(6)

        info_title = QLabel("Systemstatus")
        info_title.setObjectName("sidebarInfoTitle")

        info_text = QLabel("Lagersystem aktiv\nAlle Kernmodule bereit")
        info_text.setObjectName("sidebarInfoText")

        hint_text = QLabel("Tipp: Über F1–F4 kannst du schnell zwischen Seiten wechseln.")
        hint_text.setWordWrap(True)
        hint_text.setObjectName("sidebarHintText")

        card_layout.addWidget(info_title)
        card_layout.addWidget(info_text)
        card_layout.addSpacing(4)
        card_layout.addWidget(hint_text)

        layout.addWidget(bottom_card)

    def _connect_signals(self) -> None:
        self.dashboard_button.clicked.connect(self.dashboard_clicked.emit)
        self.inventory_button.clicked.connect(self.inventory_clicked.emit)
        self.movements_button.clicked.connect(self.movements_clicked.emit)
        self.reports_button.clicked.connect(self.reports_clicked.emit)
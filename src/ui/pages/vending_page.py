from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ui.widgets.stat_card import StatCard


@dataclass
class VendingSlotRecord:
    slot_code: str
    machine_name: str
    product_name: str
    category: str
    price: float
    quantity: int
    status: str
    note: str


class VendingSlotCard(QFrame):
    """Ein einzelnes Fach im Automaten."""

    clicked = pyqtSignal(str, str)

    def __init__(self, slot: VendingSlotRecord, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.slot = slot
        self.is_selected = False

        self.setObjectName("vendingSlotCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(180)
        self.setMaximumHeight(200)
        self.setProperty("stockState", self._get_stock_state())
        self.setProperty("selectedSlot", False)

        self._create_ui()
        self._refresh_style()

    def _get_stock_state(self) -> str:
        if self.slot.quantity == 0 or self.slot.status == "Leer":
            return "empty"
        if self.slot.quantity < 4 or self.slot.status == "Wenig Bestand":
            return "low"
        return "ok"

    def _create_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)

        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        self.slot_label = QLabel(self.slot.slot_code)
        self.slot_label.setObjectName("vendingSlotCode")

        self.price_label_top = QLabel(f"{self.slot.price:.2f} €")
        self.price_label_top.setObjectName("vendingSlotPriceTop")

        top_row.addWidget(self.slot_label)
        top_row.addStretch()
        top_row.addWidget(self.price_label_top)

        self.icon_label = QLabel(self._get_icon())
        self.icon_label.setObjectName("vendingSlotIcon")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.product_label = QLabel(self.slot.product_name)
        self.product_label.setObjectName("vendingSlotTitle")
        self.product_label.setWordWrap(True)
        self.product_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.category_label = QLabel(self.slot.category)
        self.category_label.setObjectName("vendingSlotCategory")
        self.category_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.stock_label = QLabel(self._get_stock_text())
        self.stock_label.setObjectName("vendingSlotStock")
        self.stock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel(self.slot.status)
        self.status_label.setObjectName("vendingSlotStatus")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(top_row)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.product_label)
        layout.addWidget(self.category_label)
        layout.addStretch()
        layout.addWidget(self.stock_label)
        layout.addWidget(self.status_label)

    def _get_icon(self) -> str:
        category = self.slot.category.lower()
        if "getränke" in category:
            return "🥤"
        if "snacks" in category:
            return "🍫"
        if "supplements" in category:
            return "💪"
        return "📦"

    def _get_stock_text(self) -> str:
        return f"Bestand: {self.slot.quantity}"

    def set_selected(self, selected: bool) -> None:
        self.is_selected = selected
        self.setProperty("selectedSlot", selected)
        self._refresh_style()

    def _refresh_style(self) -> None:
        self.setProperty("stockState", self._get_stock_state())
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.slot.slot_code, self.slot.machine_name)
        super().mouseReleaseEvent(event)


class VendingMachineWidget(QFrame):
    """Visueller Automat mit Display, Glasbereich, Slots und Ausgabefach."""

    slot_selected = pyqtSignal(str, str)

    def __init__(
        self,
        machine_name: str,
        slots: list[VendingSlotRecord],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.machine_name = machine_name
        self.slots = slots
        self.slot_cards: dict[tuple[str, str], VendingSlotCard] = {}

        self.setObjectName("vendingMachineFrame")
        self._create_ui()

    def _create_ui(self) -> None:
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(18, 18, 18, 18)
        outer_layout.setSpacing(14)

        self.display_card = QFrame()
        self.display_card.setObjectName("vendingMachineDisplay")

        display_layout = QHBoxLayout(self.display_card)
        display_layout.setContentsMargins(14, 12, 14, 12)
        display_layout.setSpacing(10)

        self.machine_title = QLabel(self.machine_name.upper())
        self.machine_title.setObjectName("vendingMachineTitle")

        self.machine_info = QLabel(f"{len(self.slots)} Fächer aktiv")
        self.machine_info.setObjectName("vendingMachineInfo")

        display_layout.addWidget(self.machine_title)
        display_layout.addStretch()
        display_layout.addWidget(self.machine_info)

        self.glass_area = QFrame()
        self.glass_area.setObjectName("vendingGlassArea")

        glass_layout = QVBoxLayout(self.glass_area)
        glass_layout.setContentsMargins(14, 14, 14, 14)
        glass_layout.setSpacing(12)

        self.slot_grid = QGridLayout()
        self.slot_grid.setHorizontalSpacing(12)
        self.slot_grid.setVerticalSpacing(12)

        sorted_slots = sorted(self.slots, key=lambda s: s.slot_code)

        for index, slot in enumerate(sorted_slots):
            card = VendingSlotCard(slot)
            card.clicked.connect(self.slot_selected.emit)
            self.slot_cards[(slot.slot_code, slot.machine_name)] = card

            row = index // 3
            col = index % 3
            self.slot_grid.addWidget(card, row, col)

        for col in range(3):
            self.slot_grid.setColumnStretch(col, 1)

        glass_layout.addLayout(self.slot_grid)

        self.output_tray = QFrame()
        self.output_tray.setObjectName("vendingOutputTray")

        tray_layout = QHBoxLayout(self.output_tray)
        tray_layout.setContentsMargins(12, 10, 12, 10)

        tray_label = QLabel("Ausgabefach")
        tray_label.setObjectName("vendingOutputLabel")

        tray_layout.addStretch()
        tray_layout.addWidget(tray_label)
        tray_layout.addStretch()

        outer_layout.addWidget(self.display_card)
        outer_layout.addWidget(self.glass_area)
        outer_layout.addWidget(self.output_tray)

    def set_selected_slot(self, slot_code: str | None, machine_name: str | None) -> None:
        for key, card in self.slot_cards.items():
            is_selected = key == (slot_code, machine_name)
            card.set_selected(is_selected)


class VendingTableDialog(QDialog):
    TABLE_COLUMNS = [
        "Slot",
        "Automat",
        "Produkt",
        "Kategorie",
        "Preis",
        "Bestand",
        "Status",
        "Notiz",
    ]

    def __init__(self, parent: QWidget | None = None, slots: list[VendingSlotRecord] | None = None) -> None:
        super().__init__(parent)
        self.slots = slots or []

        self.setWindowTitle("Vending-Übersicht - vergrößerte Ansicht")
        self.setMinimumSize(1300, 780)
        self.resize(1440, 840)

        self._create_ui()
        self._populate_table()

    def _create_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Vending-Übersicht")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Große Tabellenansicht aller gefilterten Automaten-Fächer.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        self.table = QTableWidget()
        self.table.setColumnCount(len(self.TABLE_COLUMNS))
        self.table.setHorizontalHeaderLabels(self.TABLE_COLUMNS)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)

        close_button = QPushButton("Schließen")
        close_button.setObjectName("secondaryButton")
        close_button.clicked.connect(self.accept)

        button_row = QHBoxLayout()
        button_row.addStretch()
        button_row.addWidget(close_button)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.table, 1)
        layout.addLayout(button_row)

    def _populate_table(self) -> None:
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(self.slots))

        for row, slot in enumerate(self.slots):
            values = [
                slot.slot_code,
                slot.machine_name,
                slot.product_name,
                slot.category,
                f"{slot.price:.2f} €",
                slot.quantity,
                slot.status,
                slot.note,
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                if col == 5:
                    if slot.quantity == 0:
                        item.setForeground(QColor("#ff8aa5"))
                    elif slot.quantity < 4:
                        item.setForeground(QColor("#ffbb72"))
                    else:
                        item.setForeground(QColor("#8df0c4"))

                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)


class VendingPage(QWidget):
    TABLE_COLUMNS = [
        "Slot",
        "Automat",
        "Produkt",
        "Kategorie",
        "Preis",
        "Bestand",
        "Status",
        "Notiz",
    ]

    def __init__(self, controller: Any | None = None) -> None:
        super().__init__()
        self.controller = controller
        self.slots: list[VendingSlotRecord] = []
        self.filtered_slots: list[VendingSlotRecord] = []
        self.selected_slot_code: str | None = None
        self.selected_machine_name: str | None = None
        self.machine_widgets: dict[str, VendingMachineWidget] = {}

        self._create_ui()
        self._load_demo_data()
        self.refresh_data()

    def _create_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.page_scroll = QScrollArea()
        self.page_scroll.setWidgetResizable(True)
        self.page_scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.page_content = QWidget()
        self.page_content_layout = QVBoxLayout(self.page_content)
        self.page_content_layout.setContentsMargins(24, 24, 24, 24)
        self.page_content_layout.setSpacing(20)

        self.page_content_layout.addWidget(self._create_top_section())

        visual_row = QHBoxLayout()
        visual_row.setSpacing(18)

        self.left_visual = self._create_machine_visual()
        self.right_panel = self._create_detail_panel()

        visual_row.addWidget(self.left_visual, 3)
        visual_row.addWidget(self.right_panel, 2)

        self.page_content_layout.addLayout(visual_row)
        self.page_content_layout.addWidget(self._create_table_section())
        self.page_content_layout.addStretch()

        self.page_scroll.setWidget(self.page_content)
        root_layout.addWidget(self.page_scroll)

    def _create_top_section(self) -> QWidget:
        card = QFrame()
        card.setObjectName("dashboardBottomCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        title = QLabel("Vending-Monitoring 2.0")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel(
            "Visualisierte Snack- und Getränkeautomaten mit klickbaren Fächern, Detailansicht und Verwaltungstabelle."
        )
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        controls = QHBoxLayout()
        controls.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Suche nach Produkt, Slot oder Automat ...")
        self.search_input.textChanged.connect(self.apply_filters)

        self.machine_filter = QComboBox()
        self.machine_filter.addItems(["Alle Automaten", "Automat Eingang", "Automat Lounge"])
        self.machine_filter.currentTextChanged.connect(self.apply_filters)

        self.category_filter = QComboBox()
        self.category_filter.addItems(["Alle Kategorien", "Getränke", "Snacks", "Supplements"])
        self.category_filter.currentTextChanged.connect(self.apply_filters)

        self.expand_button = QPushButton("🔍 Tabelle vergrößern")
        self.expand_button.setObjectName("secondaryButton")
        self.expand_button.clicked.connect(self.open_table_dialog)

        controls.addWidget(self.search_input, 2)
        controls.addWidget(self.machine_filter, 1)
        controls.addWidget(self.category_filter, 1)
        controls.addWidget(self.expand_button)

        stats = QGridLayout()
        stats.setHorizontalSpacing(18)
        stats.setVerticalSpacing(18)

        self.machine_count_card = StatCard(
            title="Automaten",
            value="0",
            subtitle="Sichtbare Automaten",
            icon="🥤",
            accent="blue",
        )
        self.occupied_card = StatCard(
            title="Belegte Fächer",
            value="0",
            subtitle="Mit Produkt gefüllt",
            icon="📦",
            accent="green",
        )
        self.empty_card = StatCard(
            title="Leere Fächer",
            value="0",
            subtitle="Bestand gleich 0",
            icon="⚠",
            accent="red",
        )
        self.low_card = StatCard(
            title="Kritische Fächer",
            value="0",
            subtitle="Wenig Bestand",
            icon="🔔",
            accent="orange",
        )

        stats.addWidget(self.machine_count_card, 0, 0)
        stats.addWidget(self.occupied_card, 0, 1)
        stats.addWidget(self.empty_card, 0, 2)
        stats.addWidget(self.low_card, 0, 3)

        for col in range(4):
            stats.setColumnStretch(col, 1)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(controls)
        layout.addLayout(stats)

        return card

    def _create_machine_visual(self) -> QWidget:
        container = QFrame()
        container.setObjectName("dashboardBottomCard")
        container.setMinimumHeight(620)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Automaten-Simulator")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Hier wirken die Fächer wie echte Automaten-Slots hinter Glas.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        self.slot_scroll = QScrollArea()
        self.slot_scroll.setWidgetResizable(True)
        self.slot_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.slot_scroll.setMinimumHeight(500)

        self.slot_content = QWidget()
        self.machine_layout = QVBoxLayout(self.slot_content)
        self.machine_layout.setContentsMargins(0, 0, 0, 0)
        self.machine_layout.setSpacing(18)

        self.slot_scroll.setWidget(self.slot_content)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.slot_scroll, 1)

        return container

    def _create_detail_panel(self) -> QWidget:
        outer_container = QFrame()
        outer_container.setObjectName("dashboardBottomCard")
        outer_container.setMinimumHeight(620)

        outer_layout = QVBoxLayout(outer_container)
        outer_layout.setContentsMargins(18, 18, 18, 18)
        outer_layout.setSpacing(12)

        panel_scroll = QScrollArea()
        panel_scroll.setWidgetResizable(True)
        panel_scroll.setFrameShape(QFrame.Shape.NoFrame)
        panel_scroll.setMinimumHeight(500)

        panel_content = QWidget()
        layout = QVBoxLayout(panel_content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        title = QLabel("Slot-Details")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Detailansicht des aktuell ausgewählten Automaten-Fachs.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        self.selected_slot = QLabel("Kein Fach ausgewählt")
        self.selected_slot.setObjectName("dashboardSectionTitle")
        self.selected_slot.setWordWrap(True)

        self.selected_status = QLabel("● -")
        self.selected_status.setObjectName("dashboardSectionSubtitle")

        self.detail_machine = self._build_detail_label("Automat", "-")
        self.detail_product = self._build_detail_label("Produkt", "-")
        self.detail_category = self._build_detail_label("Kategorie", "-")
        self.detail_price = self._build_detail_label("Preis", "-")
        self.detail_quantity = self._build_detail_label("Bestand", "-")
        self.detail_status = self._build_detail_label("Status", "-")
        self.detail_note = self._build_detail_label("Notiz", "-")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        layout.addWidget(self.selected_slot)
        layout.addWidget(self.selected_status)
        layout.addWidget(self.detail_machine)
        layout.addWidget(self.detail_product)
        layout.addWidget(self.detail_category)
        layout.addWidget(self.detail_price)
        layout.addWidget(self.detail_quantity)
        layout.addWidget(self.detail_status)
        layout.addWidget(self.detail_note)
        layout.addStretch()

        panel_scroll.setWidget(panel_content)
        outer_layout.addWidget(panel_scroll)

        return outer_container

    def _create_table_section(self) -> QWidget:
        card = QFrame()
        card.setObjectName("dashboardBottomCard")
        card.setMinimumHeight(360)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Vending-Tabelle")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Klassische Tabellenansicht aller gefilterten Fächer.")
        subtitle.setObjectName("dashboardSectionSubtitle")

        self.vending_table = QTableWidget()
        self.vending_table.setColumnCount(len(self.TABLE_COLUMNS))
        self.vending_table.setHorizontalHeaderLabels(self.TABLE_COLUMNS)
        self.vending_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.vending_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.vending_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.vending_table.setAlternatingRowColors(True)
        self.vending_table.setSortingEnabled(True)
        self.vending_table.verticalHeader().setVisible(False)
        self.vending_table.horizontalHeader().setStretchLastSection(True)
        self.vending_table.setMinimumHeight(240)
        self.vending_table.itemSelectionChanged.connect(self._select_from_table)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.vending_table)

        return card

    def _build_detail_label(self, title: str, value: str) -> QLabel:
        label = QLabel(f"<b>{title}:</b><br>{value}")
        label.setObjectName("dashboardActivityItem")
        label.setWordWrap(True)
        return label

    def _load_demo_data(self) -> None:
        self.slots = [
            VendingSlotRecord("A1", "Automat Eingang", "Water 0.5L", "Getränke", 2.00, 8, "Verfügbar", ""),
            VendingSlotRecord("A2", "Automat Eingang", "Cola Zero", "Getränke", 2.50, 2, "Wenig Bestand", ""),
            VendingSlotRecord("A3", "Automat Eingang", "Isotonic Drink", "Getränke", 2.80, 0, "Leer", "Nachfüllen"),
            VendingSlotRecord("B1", "Automat Eingang", "Protein Bar", "Snacks", 2.90, 6, "Verfügbar", ""),
            VendingSlotRecord("B2", "Automat Eingang", "Nuts Mix", "Snacks", 2.60, 1, "Wenig Bestand", ""),
            VendingSlotRecord("B3", "Automat Eingang", "Chocolate Bar", "Snacks", 1.90, 0, "Leer", "Ausverkauft"),
            VendingSlotRecord("C1", "Automat Lounge", "Energy Drink", "Getränke", 3.20, 7, "Verfügbar", ""),
            VendingSlotRecord("C2", "Automat Lounge", "Protein Shake", "Supplements", 4.50, 3, "Wenig Bestand", ""),
            VendingSlotRecord("C3", "Automat Lounge", "BCAA Drink", "Supplements", 4.90, 5, "Verfügbar", ""),
            VendingSlotRecord("D1", "Automat Lounge", "Protein Cookie", "Snacks", 3.40, 4, "Verfügbar", ""),
            VendingSlotRecord("D2", "Automat Lounge", "Vitamin Water", "Getränke", 2.70, 0, "Leer", "Fach leer"),
            VendingSlotRecord("D3", "Automat Lounge", "Pre-Workout Shot", "Supplements", 3.90, 2, "Wenig Bestand", ""),
        ]

    def refresh_data(self) -> None:
        if self.controller is not None:
            try:
                slots = self.controller.get_all_vending_slots()
                self.slots = list(slots)
            except Exception:
                pass

        self.apply_filters()

    def apply_filters(self) -> None:
        search_text = self.search_input.text().strip().lower()
        selected_machine = self.machine_filter.currentText()
        selected_category = self.category_filter.currentText()

        result: list[VendingSlotRecord] = []

        for slot in self.slots:
            searchable = " ".join(
                [
                    slot.slot_code,
                    slot.machine_name,
                    slot.product_name,
                    slot.category,
                    slot.status,
                    slot.note,
                ]
            ).lower()

            matches_search = search_text in searchable
            matches_machine = (
                selected_machine == "Alle Automaten" or slot.machine_name == selected_machine
            )
            matches_category = (
                selected_category == "Alle Kategorien" or slot.category == selected_category
            )

            if matches_search and matches_machine and matches_category:
                result.append(slot)

        self.filtered_slots = result
        self._rebuild_machine_visual()
        self._populate_table()
        self._update_stats()

        if self.filtered_slots:
            current = self._find_slot(self.selected_slot_code, self.selected_machine_name)
            if current is None:
                self.select_slot(self.filtered_slots[0].slot_code, self.filtered_slots[0].machine_name)
            else:
                self.select_slot(current.slot_code, current.machine_name)
        else:
            self._clear_detail_panel()

    def _rebuild_machine_visual(self) -> None:
        while self.machine_layout.count():
            item = self.machine_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.machine_widgets.clear()

        grouped: dict[str, list[VendingSlotRecord]] = {}
        for slot in self.filtered_slots:
            grouped.setdefault(slot.machine_name, []).append(slot)

        for machine_name, slots in grouped.items():
            machine_widget = VendingMachineWidget(machine_name, slots)
            machine_widget.slot_selected.connect(self.select_slot)
            self.machine_widgets[machine_name] = machine_widget
            self.machine_layout.addWidget(machine_widget)

        self.machine_layout.addStretch()

    def _populate_table(self) -> None:
        self.vending_table.setSortingEnabled(False)
        self.vending_table.setRowCount(len(self.filtered_slots))

        for row, slot in enumerate(self.filtered_slots):
            values = [
                slot.slot_code,
                slot.machine_name,
                slot.product_name,
                slot.category,
                f"{slot.price:.2f} €",
                slot.quantity,
                slot.status,
                slot.note,
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                if col == 5:
                    if slot.quantity == 0:
                        item.setForeground(QColor("#ff8aa5"))
                    elif slot.quantity < 4:
                        item.setForeground(QColor("#ffbb72"))
                    else:
                        item.setForeground(QColor("#8df0c4"))

                self.vending_table.setItem(row, col, item)

        self.vending_table.resizeColumnsToContents()
        self.vending_table.setSortingEnabled(True)

        if self.filtered_slots and self.vending_table.rowCount() > 0:
            self.vending_table.selectRow(0)

    def _select_from_table(self) -> None:
        row = self.vending_table.currentRow()
        if row < 0:
            return

        slot_item = self.vending_table.item(row, 0)
        machine_item = self.vending_table.item(row, 1)

        if slot_item is None or machine_item is None:
            return

        self.select_slot(slot_item.text(), machine_item.text())

    def select_slot(self, slot_code: str, machine_name: str) -> None:
        self.selected_slot_code = slot_code
        self.selected_machine_name = machine_name

        selected = self._find_slot(slot_code, machine_name)

        if selected is None:
            self._clear_detail_panel()
            return

        self.selected_slot.setText(f"Fach {selected.slot_code}")
        self.selected_status.setText(f"● {selected.status}")

        if selected.quantity == 0 or selected.status == "Leer":
            self.selected_status.setObjectName("dashboardStatusCritical")
        elif selected.quantity < 4:
            self.selected_status.setObjectName("dashboardStatusWarn")
        else:
            self.selected_status.setObjectName("dashboardStatusOk")

        self.selected_status.style().unpolish(self.selected_status)
        self.selected_status.style().polish(self.selected_status)

        self.detail_machine.setText(f"<b>Automat:</b><br>{selected.machine_name}")
        self.detail_product.setText(f"<b>Produkt:</b><br>{selected.product_name}")
        self.detail_category.setText(f"<b>Kategorie:</b><br>{selected.category}")
        self.detail_price.setText(f"<b>Preis:</b><br>{selected.price:.2f} €")
        self.detail_quantity.setText(f"<b>Bestand:</b><br>{selected.quantity}")
        self.detail_status.setText(f"<b>Status:</b><br>{selected.status}")
        self.detail_note.setText(f"<b>Notiz:</b><br>{selected.note if selected.note else '-'}")

        for machine_widget in self.machine_widgets.values():
            machine_widget.set_selected_slot(slot_code, machine_name)

    def _clear_detail_panel(self) -> None:
        self.selected_slot.setText("Kein Fach ausgewählt")
        self.selected_status.setText("● -")
        self.selected_status.setObjectName("dashboardSectionSubtitle")
        self.selected_status.style().unpolish(self.selected_status)
        self.selected_status.style().polish(self.selected_status)

        self.detail_machine.setText("<b>Automat:</b><br>-")
        self.detail_product.setText("<b>Produkt:</b><br>-")
        self.detail_category.setText("<b>Kategorie:</b><br>-")
        self.detail_price.setText("<b>Preis:</b><br>-")
        self.detail_quantity.setText("<b>Bestand:</b><br>-")
        self.detail_status.setText("<b>Status:</b><br>-")
        self.detail_note.setText("<b>Notiz:</b><br>-")

    def _find_slot(self, slot_code: str | None, machine_name: str | None) -> VendingSlotRecord | None:
        if slot_code is None or machine_name is None:
            return None

        for slot in self.filtered_slots:
            if slot.slot_code == slot_code and slot.machine_name == machine_name:
                return slot
        return None

    def _update_stats(self) -> None:
        machines = {slot.machine_name for slot in self.filtered_slots}
        occupied = sum(1 for slot in self.filtered_slots if slot.quantity > 0)
        empty = sum(1 for slot in self.filtered_slots if slot.quantity == 0)
        low = sum(1 for slot in self.filtered_slots if 0 < slot.quantity < 4)

        self.machine_count_card.set_value_animated(len(machines))
        self.occupied_card.set_value_animated(occupied)
        self.empty_card.set_value_animated(empty)
        self.low_card.set_value_animated(low)

    def open_table_dialog(self) -> None:
        dialog = VendingTableDialog(self, self.filtered_slots)
        dialog.exec()
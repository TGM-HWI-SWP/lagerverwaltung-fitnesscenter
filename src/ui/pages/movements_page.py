from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from PyQt6.QtCore import Qt
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
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.ui.widgets.stat_card import StatCard


@dataclass
class MovementRecord:
    """Speichert die aufbereiteten Daten einer Lagerbewegung."""

    movement_id: str
    date_time: str
    product_name: str
    movement_type: str
    quantity: int
    reason: str
    employee: str
    risk: str


class MovementsTableDialog(QDialog):
    """Große Tabellenansicht für Lagerbewegungen."""

    TABLE_COLUMNS = [
        "ID",
        "Datum / Zeit",
        "Produkt",
        "Typ",
        "Menge",
        "Grund",
        "Mitarbeiter",
        "Risiko",
    ]

    def __init__(
        self,
        parent: QWidget | None = None,
        movements: list[MovementRecord] | None = None,
    ) -> None:
        """Initialisiert den Tabellen-Dialog."""
        super().__init__(parent)

        self.movements = movements or []

        self.setWindowTitle("Lagerbewegungen - vergrößerte Ansicht")
        self.setMinimumSize(1320, 780)
        self.resize(1450, 850)

        self._create_ui()
        self._populate_table()

    def _create_ui(self) -> None:
        """Erstellt die Oberfläche der großen Tabellenansicht."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Lagerbewegungen")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Große Ansicht aller gefilterten Lagerbewegungen.")
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

    def _apply_item_color(self, item: QTableWidgetItem, column: int, movement: MovementRecord) -> None:
        """Setzt passende Farben für Typ, Menge und Risiko."""
        if column == 4:
            if movement.quantity > 0:
                item.setForeground(QColor("#7ef0b8"))
            else:
                item.setForeground(QColor("#ff9fb4"))

        if column == 3:
            if movement.movement_type == "Wareneingang":
                item.setForeground(QColor("#8df0c4"))
            elif movement.movement_type == "Warenausgang":
                item.setForeground(QColor("#ff9fb4"))
            else:
                item.setForeground(QColor("#ffbb72"))

        if column == 7:
            if movement.risk == "Hoch":
                item.setForeground(QColor("#ff8aa5"))
            elif movement.risk == "Mittel":
                item.setForeground(QColor("#ffbb72"))
            else:
                item.setForeground(QColor("#8df0c4"))

    def _populate_table(self) -> None:
        """Füllt die Tabelle mit allen übergebenen Lagerbewegungen."""
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(self.movements))
        self.table.clearContents()

        for row, movement in enumerate(self.movements):
            values = [
                movement.movement_id,
                movement.date_time,
                movement.product_name,
                movement.movement_type,
                f"{movement.quantity:+d}",
                movement.reason,
                movement.employee,
                movement.risk,
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
                )
                self._apply_item_color(item, col, movement)
                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)


class MovementsPage(QWidget):
    """Seite zur Überwachung und Filterung aller Lagerbewegungen."""

    TABLE_COLUMNS = [
        "ID",
        "Datum / Zeit",
        "Produkt",
        "Typ",
        "Menge",
        "Grund",
        "Mitarbeiter",
        "Risiko",
    ]

    def __init__(self, controller: Any | None = None) -> None:
        """Initialisiert die Bewegungsseite."""
        super().__init__()

        self.controller = controller
        self.movements: list[MovementRecord] = []
        self.filtered_movements: list[MovementRecord] = []

        self._create_ui()
        self.refresh_data()

    def _create_ui(self) -> None:
        """Erstellt die komplette Oberfläche der Seite."""
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.setSpacing(20)

        self._create_stats_section(root_layout)
        self._create_toolbar(root_layout)
        self._create_table_section(root_layout)

    def _create_stats_section(self, layout: QVBoxLayout) -> None:
        """Erstellt den Statistikbereich der Bewegungsseite."""
        stats_grid = QGridLayout()
        stats_grid.setHorizontalSpacing(18)
        stats_grid.setVerticalSpacing(18)

        self.entries_card = StatCard(
            title="Wareneingänge",
            value="0",
            subtitle="Positive Bewegungen",
            icon="📥",
            accent="green",
        )
        self.outputs_card = StatCard(
            title="Warenausgänge",
            value="0",
            subtitle="Negative Bewegungen",
            icon="📤",
            accent="red",
        )
        self.critical_card = StatCard(
            title="Kritische Bewegungen",
            value="0",
            subtitle="Risiko Hoch",
            icon="⚠",
            accent="orange",
        )
        self.netto_card = StatCard(
            title="Netto",
            value="0",
            subtitle="Saldo der Mengen",
            icon="📊",
            accent="blue",
        )

        stats_grid.addWidget(self.entries_card, 0, 0)
        stats_grid.addWidget(self.outputs_card, 0, 1)
        stats_grid.addWidget(self.critical_card, 0, 2)
        stats_grid.addWidget(self.netto_card, 0, 3)

        for col in range(4):
            stats_grid.setColumnStretch(col, 1)

        layout.addLayout(stats_grid)

    def _create_toolbar(self, layout: QVBoxLayout) -> None:
        """Erstellt Suchfeld, Filter und Tabellenaktion."""
        toolbar_card = QFrame()
        toolbar_card.setObjectName("dashboardBottomCard")

        toolbar_layout = QVBoxLayout(toolbar_card)
        toolbar_layout.setContentsMargins(18, 18, 18, 18)
        toolbar_layout.setSpacing(14)

        title = QLabel("Lagerbewegungen")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel(
            "Ein- und Ausgänge, Korrekturen und auffällige Bewegungen überwachen."
        )
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        control_row = QHBoxLayout()
        control_row.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Suche nach Produkt, Grund, Mitarbeiter oder ID ..."
        )
        self.search_input.textChanged.connect(self.apply_filters)

        self.type_filter = QComboBox()
        self.type_filter.addItems(
            ["Alle Typen", "Wareneingang", "Warenausgang", "Korrektur"]
        )
        self.type_filter.currentTextChanged.connect(self.apply_filters)

        self.risk_filter = QComboBox()
        self.risk_filter.addItems(["Alle Risiken", "Niedrig", "Mittel", "Hoch"])
        self.risk_filter.currentTextChanged.connect(self.apply_filters)

        self.expand_button = QPushButton("🔍 Tabelle vergrößern")
        self.expand_button.setObjectName("secondaryButton")
        self.expand_button.clicked.connect(self.open_table_dialog)

        control_row.addWidget(self.search_input, 2)
        control_row.addWidget(self.type_filter, 1)
        control_row.addWidget(self.risk_filter, 1)
        control_row.addWidget(self.expand_button)

        toolbar_layout.addWidget(title)
        toolbar_layout.addWidget(subtitle)
        toolbar_layout.addLayout(control_row)

        layout.addWidget(toolbar_card)

    def _create_table_section(self, layout: QVBoxLayout) -> None:
        """Erstellt die Tabellenansicht der Lagerbewegungen."""
        card = QFrame()
        card.setObjectName("dashboardBottomCard")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(12)

        title = QLabel("Bewegungshistorie")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Alle gefilterten Lagerbewegungen im Überblick.")
        subtitle.setObjectName("dashboardSectionSubtitle")

        self.movements_table = QTableWidget()
        self.movements_table.setColumnCount(len(self.TABLE_COLUMNS))
        self.movements_table.setHorizontalHeaderLabels(self.TABLE_COLUMNS)
        self.movements_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.movements_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.movements_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.movements_table.setAlternatingRowColors(True)
        self.movements_table.setSortingEnabled(True)
        self.movements_table.verticalHeader().setVisible(False)
        self.movements_table.horizontalHeader().setStretchLastSection(True)

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(self.movements_table)

        layout.addWidget(card)

    def _map_movement_to_record(self, movement: Any) -> MovementRecord:
        """Wandelt ein Controller-Objekt in ein MovementRecord um."""
        movement_id = getattr(movement, "id", "") or ""
        timestamp = getattr(movement, "timestamp", "") or ""
        product_name = getattr(movement, "product_name", "") or ""
        quantity_change = getattr(movement, "quantity_change", 0) or 0
        movement_type_backend = getattr(movement, "movement_type", "") or ""
        reason = getattr(movement, "reason", "") or ""
        performed_by = getattr(movement, "performed_by", "") or ""

        movement_type_map = {
            "in": "Wareneingang",
            "out": "Warenausgang",
            "correction": "Korrektur",
            "incoming": "Wareneingang",
            "outgoing": "Warenausgang",
        }

        movement_type = movement_type_map.get(
            str(movement_type_backend).lower(),
            str(movement_type_backend) if movement_type_backend else "-",
        )

        abs_quantity = abs(int(quantity_change))
        if movement_type == "Wareneingang":
            signed_quantity = abs_quantity
        else:
            signed_quantity = -abs_quantity

        if abs_quantity >= 10:
            risk = "Hoch"
        elif abs_quantity >= 5:
            risk = "Mittel"
        else:
            risk = "Niedrig"

        return MovementRecord(
            movement_id=str(movement_id),
            date_time=str(timestamp) if timestamp else "",
            product_name=str(product_name),
            movement_type=movement_type,
            quantity=signed_quantity,
            reason=str(reason),
            employee=str(performed_by),
            risk=risk,
        )

    def refresh_data(self) -> None:
        """Lädt Bewegungsdaten neu und aktualisiert die Ansicht."""
        try:
            if self.controller is not None:
                movements = self.controller.get_movements()
                self.movements = [
                    self._map_movement_to_record(movement) for movement in movements
                ]
            else:
                self.movements = []

            self.apply_filters()
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Lagerbewegungen konnten nicht geladen werden:\n{error}",
            )
            self.movements = []
            self.filtered_movements = []
            self.populate_table()
            self.update_stats()

    def apply_filters(self) -> None:
        """Filtert Lagerbewegungen nach Suche, Typ und Risiko."""
        search_text = self.search_input.text().strip().lower()
        selected_type = self.type_filter.currentText()
        selected_risk = self.risk_filter.currentText()

        result: list[MovementRecord] = []

        for movement in self.movements:
            searchable = " ".join(
                [
                    movement.movement_id,
                    movement.product_name,
                    movement.reason,
                    movement.employee,
                    movement.movement_type,
                    movement.risk,
                ]
            ).lower()

            matches_search = search_text in searchable
            matches_type = (
                selected_type == "Alle Typen" or movement.movement_type == selected_type
            )
            matches_risk = (
                selected_risk == "Alle Risiken" or movement.risk == selected_risk
            )

            if matches_search and matches_type and matches_risk:
                result.append(movement)

        self.filtered_movements = result
        self.populate_table()
        self.update_stats()

    def _apply_item_color(self, item: QTableWidgetItem, column: int, movement: MovementRecord) -> None:
        """Setzt passende Farben für Typ, Menge und Risiko."""
        if column == 4:
            if movement.quantity > 0:
                item.setForeground(QColor("#7ef0b8"))
            else:
                item.setForeground(QColor("#ff9fb4"))

        if column == 3:
            if movement.movement_type == "Wareneingang":
                item.setForeground(QColor("#8df0c4"))
            elif movement.movement_type == "Warenausgang":
                item.setForeground(QColor("#ff9fb4"))
            else:
                item.setForeground(QColor("#ffbb72"))

        if column == 7:
            if movement.risk == "Hoch":
                item.setForeground(QColor("#ff8aa5"))
            elif movement.risk == "Mittel":
                item.setForeground(QColor("#ffbb72"))
            else:
                item.setForeground(QColor("#8df0c4"))

    def populate_table(self) -> None:
        """Füllt die Tabelle mit den gefilterten Lagerbewegungen."""
        self.movements_table.setSortingEnabled(False)
        self.movements_table.setRowCount(len(self.filtered_movements))
        self.movements_table.clearContents()

        for row, movement in enumerate(self.filtered_movements):
            values = [
                movement.movement_id,
                movement.date_time,
                movement.product_name,
                movement.movement_type,
                f"{movement.quantity:+d}",
                movement.reason,
                movement.employee,
                movement.risk,
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
                )
                self._apply_item_color(item, col, movement)
                self.movements_table.setItem(row, col, item)

        self.movements_table.resizeColumnsToContents()
        self.movements_table.setSortingEnabled(True)

        if self.filtered_movements and self.movements_table.rowCount() > 0:
            self.movements_table.selectRow(0)

    def update_stats(self) -> None:
        """Aktualisiert die Kennzahlenkarten."""
        entries = sum(1 for movement in self.filtered_movements if movement.quantity > 0)
        outputs = sum(1 for movement in self.filtered_movements if movement.quantity < 0)
        critical = sum(1 for movement in self.filtered_movements if movement.risk == "Hoch")
        netto = sum(movement.quantity for movement in self.filtered_movements)

        self.entries_card.set_value_animated(entries)
        self.outputs_card.set_value_animated(outputs)
        self.critical_card.set_value_animated(critical)
        self.netto_card.set_value(str(netto))

    def open_table_dialog(self) -> None:
        """Öffnet die vergrößerte Tabellenansicht."""
        dialog = MovementsTableDialog(self, self.filtered_movements)
        dialog.exec()
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDialog,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ui.widgets.stat_card import StatCard


@dataclass
class MovementRecord:
    movement_id: str
    date_time: str
    product_name: str
    movement_type: str
    quantity: int
    reason: str
    employee: str
    risk: str


class MovementDialog(QDialog):
    """Dialog zum Anlegen einer neuen Lagerbewegung."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setWindowTitle("Lagerbewegung hinzufügen")
        self.setModal(True)
        self.setMinimumWidth(520)

        self._create_ui()

    def _create_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(18)

        title = QLabel("Neue Lagerbewegung")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Neue Ein- oder Auslagerung mit Grund und Mitarbeiter erfassen.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        form_card = QFrame()
        form_card.setObjectName("dashboardBottomCard")

        form_layout = QFormLayout(form_card)
        form_layout.setContentsMargins(18, 18, 18, 18)
        form_layout.setSpacing(14)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("z. B. MOV-1010")

        self.datetime_input = QLineEdit()
        self.datetime_input.setPlaceholderText("z. B. 16.04.2026 10:30")

        self.product_input = QLineEdit()
        self.product_input.setPlaceholderText("Produktname")

        self.type_input = QComboBox()
        self.type_input.addItems(["Wareneingang", "Warenausgang", "Korrektur"])

        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(1, 100000)
        self.quantity_input.setValue(1)

        self.reason_input = QLineEdit()
        self.reason_input.setPlaceholderText("z. B. Lieferung, Verkauf, Inventur")

        self.employee_input = QLineEdit()
        self.employee_input.setPlaceholderText("Mitarbeitername")

        self.risk_input = QComboBox()
        self.risk_input.addItems(["Niedrig", "Mittel", "Hoch"])

        form_layout.addRow("Bewegungs-ID:", self.id_input)
        form_layout.addRow("Datum/Zeit:", self.datetime_input)
        form_layout.addRow("Produkt:", self.product_input)
        form_layout.addRow("Typ:", self.type_input)
        form_layout.addRow("Menge:", self.quantity_input)
        form_layout.addRow("Grund:", self.reason_input)
        form_layout.addRow("Mitarbeiter:", self.employee_input)
        form_layout.addRow("Risiko:", self.risk_input)

        button_row = QHBoxLayout()
        button_row.addStretch()

        cancel_button = QPushButton("Abbrechen")
        cancel_button.setObjectName("secondaryButton")
        cancel_button.clicked.connect(self.reject)

        save_button = QPushButton("Speichern")
        save_button.clicked.connect(self._validate_and_accept)

        button_row.addWidget(cancel_button)
        button_row.addWidget(save_button)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(form_card)
        main_layout.addLayout(button_row)

    def _validate_and_accept(self) -> None:
        if not self.id_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte eine Bewegungs-ID eingeben.")
            return

        if not self.product_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte ein Produkt eingeben.")
            return

        if not self.reason_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte einen Grund eingeben.")
            return

        if not self.employee_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte einen Mitarbeiter eingeben.")
            return

        self.accept()

    def get_data(self) -> MovementRecord:
        movement_type = self.type_input.currentText()
        quantity = self.quantity_input.value()

        signed_quantity = quantity
        if movement_type == "Warenausgang":
            signed_quantity = -quantity
        elif movement_type == "Korrektur":
            signed_quantity = -quantity

        return MovementRecord(
            movement_id=self.id_input.text().strip(),
            date_time=self.datetime_input.text().strip(),
            product_name=self.product_input.text().strip(),
            movement_type=movement_type,
            quantity=signed_quantity,
            reason=self.reason_input.text().strip(),
            employee=self.employee_input.text().strip(),
            risk=self.risk_input.currentText(),
        )


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

    def __init__(self, parent: QWidget | None = None, movements: list[MovementRecord] | None = None) -> None:
        super().__init__(parent)
        self.movements = movements or []

        self.setWindowTitle("Lagerbewegungen - vergrößerte Ansicht")
        self.setMinimumSize(1320, 780)
        self.resize(1450, 850)

        self._create_ui()
        self._populate_table()

    def _create_ui(self) -> None:
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

    def _populate_table(self) -> None:
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(self.movements))

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
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                if col == 4:
                    if movement.quantity > 0:
                        item.setForeground(QColor("#7ef0b8"))
                    else:
                        item.setForeground(QColor("#ff9fb4"))

                if col == 7:
                    if movement.risk == "Hoch":
                        item.setForeground(QColor("#ff8aa5"))
                    elif movement.risk == "Mittel":
                        item.setForeground(QColor("#ffbb72"))
                    else:
                        item.setForeground(QColor("#8df0c4"))

                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)


class MovementsPage(QWidget):
    """Kontrollzentrum für Lagerbewegungen."""

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
        super().__init__()
        self.controller = controller
        self.movements: list[MovementRecord] = []
        self.filtered_movements: list[MovementRecord] = []

        self._create_ui()
        self._load_demo_data()
        self.refresh_data()

    # =========================
    # UI
    # =========================
    def _create_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.setSpacing(20)

        self._create_stats_section(root_layout)
        self._create_toolbar(root_layout)
        self._create_table_section(root_layout)

    def _create_stats_section(self, layout: QVBoxLayout) -> None:
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
            title="Netto heute",
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
        toolbar_card = QFrame()
        toolbar_card.setObjectName("dashboardBottomCard")

        toolbar_layout = QVBoxLayout(toolbar_card)
        toolbar_layout.setContentsMargins(18, 18, 18, 18)
        toolbar_layout.setSpacing(14)

        title = QLabel("Lagerbewegungen")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Ein- und Ausgänge, Korrekturen und auffällige Bewegungen überwachen.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        control_row = QHBoxLayout()
        control_row.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Suche nach Produkt, Grund, Mitarbeiter oder ID ...")
        self.search_input.textChanged.connect(self.apply_filters)

        self.type_filter = QComboBox()
        self.type_filter.addItems(["Alle Typen", "Wareneingang", "Warenausgang", "Korrektur"])
        self.type_filter.currentTextChanged.connect(self.apply_filters)

        self.risk_filter = QComboBox()
        self.risk_filter.addItems(["Alle Risiken", "Niedrig", "Mittel", "Hoch"])
        self.risk_filter.currentTextChanged.connect(self.apply_filters)

        self.add_button = QPushButton("➕ Bewegung hinzufügen")
        self.add_button.clicked.connect(self.open_add_dialog)

        self.delete_button = QPushButton("🗑 Löschen")
        self.delete_button.setObjectName("secondaryButton")
        self.delete_button.clicked.connect(self.delete_movement)

        self.expand_button = QPushButton("🔍 Tabelle vergrößern")
        self.expand_button.setObjectName("secondaryButton")
        self.expand_button.clicked.connect(self.open_table_dialog)

        control_row.addWidget(self.search_input, 2)
        control_row.addWidget(self.type_filter, 1)
        control_row.addWidget(self.risk_filter, 1)
        control_row.addWidget(self.add_button)
        control_row.addWidget(self.delete_button)
        control_row.addWidget(self.expand_button)

        toolbar_layout.addWidget(title)
        toolbar_layout.addWidget(subtitle)
        toolbar_layout.addLayout(control_row)

        layout.addWidget(toolbar_card)

    def _create_table_section(self, layout: QVBoxLayout) -> None:
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

    # =========================
    # Data
    # =========================
    def _load_demo_data(self) -> None:
        self.movements = [
            MovementRecord("MOV-1001", "15.04.2026 08:12", "Whey Protein Vanilla", "Wareneingang", 25, "Lieferung", "Markus Steiner", "Niedrig"),
            MovementRecord("MOV-1002", "15.04.2026 09:05", "Protein Bar", "Warenausgang", -8, "Verkauf", "Laura Hofer", "Niedrig"),
            MovementRecord("MOV-1003", "15.04.2026 10:18", "Pre-Workout Booster", "Warenausgang", -12, "Verkauf", "Daniel Fuchs", "Mittel"),
            MovementRecord("MOV-1004", "15.04.2026 11:40", "Isotonic Drink", "Wareneingang", 40, "Lieferung", "Vanessa Moser", "Niedrig"),
            MovementRecord("MOV-1005", "15.04.2026 12:25", "Disinfectant Spray", "Korrektur", -3, "Inventurkorrektur", "Nina Bauer", "Hoch"),
            MovementRecord("MOV-1006", "15.04.2026 13:10", "Gym Towel", "Warenausgang", -5, "Verkauf", "Tobias Leitner", "Niedrig"),
            MovementRecord("MOV-1007", "15.04.2026 14:32", "Shaker Bottle", "Wareneingang", 18, "Nachbestellung", "Julian Kern", "Mittel"),
            MovementRecord("MOV-1008", "15.04.2026 15:02", "Protein Bar", "Korrektur", -2, "Beschädigte Ware", "Sabrina Wolf", "Hoch"),
        ]

    def refresh_data(self) -> None:
        if self.controller is not None:
            try:
                movements = self.controller.get_all_movements()
                self.movements = list(movements)
                self.apply_filters()
                return
            except Exception:
                pass

        self.apply_filters()

    def apply_filters(self) -> None:
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
            matches_type = selected_type == "Alle Typen" or movement.movement_type == selected_type
            matches_risk = selected_risk == "Alle Risiken" or movement.risk == selected_risk

            if matches_search and matches_type and matches_risk:
                result.append(movement)

        self.filtered_movements = result
        self.populate_table()
        self.update_stats()

    def populate_table(self) -> None:
        self.movements_table.setSortingEnabled(False)
        self.movements_table.setRowCount(len(self.filtered_movements))

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
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                if col == 4:
                    if movement.quantity > 0:
                        item.setForeground(QColor("#7ef0b8"))
                    else:
                        item.setForeground(QColor("#ff9fb4"))

                if col == 3:
                    if movement.movement_type == "Wareneingang":
                        item.setForeground(QColor("#8df0c4"))
                    elif movement.movement_type == "Warenausgang":
                        item.setForeground(QColor("#ff9fb4"))
                    else:
                        item.setForeground(QColor("#ffbb72"))

                if col == 7:
                    if movement.risk == "Hoch":
                        item.setForeground(QColor("#ff8aa5"))
                    elif movement.risk == "Mittel":
                        item.setForeground(QColor("#ffbb72"))
                    else:
                        item.setForeground(QColor("#8df0c4"))

                self.movements_table.setItem(row, col, item)

        self.movements_table.resizeColumnsToContents()
        self.movements_table.setSortingEnabled(True)

        if self.filtered_movements and self.movements_table.rowCount() > 0:
            self.movements_table.selectRow(0)

    def update_stats(self) -> None:
        entries = sum(1 for m in self.filtered_movements if m.quantity > 0)
        outputs = sum(1 for m in self.filtered_movements if m.quantity < 0)
        critical = sum(1 for m in self.filtered_movements if m.risk == "Hoch")
        netto = sum(m.quantity for m in self.filtered_movements)

        self.entries_card.set_value_animated(entries)
        self.outputs_card.set_value_animated(outputs)
        self.critical_card.set_value_animated(critical)
        self.netto_card.set_value(str(netto))

    def _get_selected_movement(self) -> MovementRecord | None:
        row = self.movements_table.currentRow()
        if row < 0:
            return None

        id_item = self.movements_table.item(row, 0)
        if id_item is None:
            return None

        movement_id = id_item.text()
        for movement in self.filtered_movements:
            if movement.movement_id == movement_id:
                return movement

        return None

    # =========================
    # Actions
    # =========================
    def open_table_dialog(self) -> None:
        dialog = MovementsTableDialog(self, self.filtered_movements)
        dialog.exec()

    def open_add_dialog(self) -> None:
        dialog = MovementDialog(self)
        if dialog.exec():
            new_movement = dialog.get_data()

            if any(m.movement_id == new_movement.movement_id for m in self.movements):
                QMessageBox.warning(
                    self,
                    "Doppelte ID",
                    "Diese Bewegungs-ID existiert bereits.",
                )
                return

            self.movements.append(new_movement)
            self.apply_filters()

    def delete_movement(self) -> None:
        movement = self._get_selected_movement()
        if movement is None:
            QMessageBox.warning(self, "Löschen", "Bitte zuerst eine Bewegung auswählen.")
            return

        answer = QMessageBox.question(
            self,
            "Bewegung löschen",
            f"Möchtest du die Bewegung '{movement.movement_id}' wirklich löschen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer == QMessageBox.StandardButton.Yes:
            self.movements = [
                m for m in self.movements if m.movement_id != movement.movement_id
            ]
            self.apply_filters()
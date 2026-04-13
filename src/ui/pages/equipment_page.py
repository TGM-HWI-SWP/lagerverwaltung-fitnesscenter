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
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ui.widgets.stat_card import StatCard


@dataclass
class EquipmentRecord:
    equipment_id: str
    name: str
    equipment_type: str
    area: str
    status: str
    assigned_employee: str
    next_maintenance: str
    note: str


class EquipmentUnitCard(QFrame):
    """Große klickbare Gerätekarte."""

    clicked = pyqtSignal(str)

    def __init__(self, equipment: EquipmentRecord, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.equipment = equipment

        self.setObjectName("dashboardBottomCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(210)
        self.setMaximumHeight(240)

        self._create_ui()

    def _create_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        self.id_badge = QLabel(self.equipment.equipment_id)
        self.id_badge.setObjectName("dashboardHealthBadge")

        self.status_badge = QLabel(f"● {self.equipment.status}")
        self._apply_status_style(self.status_badge, self.equipment.status)

        top_row.addWidget(self.id_badge)
        top_row.addStretch()
        top_row.addWidget(self.status_badge)

        self.name_label = QLabel(self.equipment.name)
        self.name_label.setObjectName("dashboardSectionTitle")
        self.name_label.setWordWrap(True)

        self.type_label = QLabel(f"{self.equipment.equipment_type} • {self.equipment.area}")
        self.type_label.setObjectName("dashboardSectionSubtitle")
        self.type_label.setWordWrap(True)

        self.employee_label = QLabel(f"Mitarbeiter: {self.equipment.assigned_employee}")
        self.employee_label.setObjectName("dashboardActivityItem")
        self.employee_label.setWordWrap(True)

        self.maintenance_label = QLabel(
            f"Nächste Wartung: {self.equipment.next_maintenance}"
        )
        self.maintenance_label.setObjectName("dashboardActivityItem")
        self.maintenance_label.setWordWrap(True)

        self.note_label = QLabel(
            f"Notiz: {self.equipment.note if self.equipment.note else '-'}"
        )
        self.note_label.setObjectName("dashboardSectionSubtitle")
        self.note_label.setWordWrap(True)

        layout.addLayout(top_row)
        layout.addWidget(self.name_label)
        layout.addWidget(self.type_label)
        layout.addSpacing(4)
        layout.addWidget(self.employee_label)
        layout.addWidget(self.maintenance_label)
        layout.addWidget(self.note_label)
        layout.addStretch()

    def _apply_status_style(self, label: QLabel, status: str) -> None:
        if status == "Aktiv":
            label.setObjectName("dashboardStatusOk")
        elif status == "Wartung":
            label.setObjectName("dashboardStatusWarn")
        elif status == "Defekt":
            label.setObjectName("dashboardStatusCritical")
        else:
            label.setObjectName("dashboardSectionSubtitle")

    def mouseReleaseEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.equipment.equipment_id)
        super().mouseReleaseEvent(event)


class EquipmentTableDialog(QDialog):
    """Große Tabellenansicht aller Geräte."""

    TABLE_COLUMNS = [
        "Geräte-ID",
        "Name",
        "Typ",
        "Bereich",
        "Status",
        "Mitarbeiter",
        "Nächste Wartung",
        "Notiz",
    ]

    def __init__(self, parent: QWidget | None = None, equipments: list[EquipmentRecord] | None = None) -> None:
        super().__init__(parent)
        self.equipments = equipments or []

        self.setWindowTitle("Geräteübersicht - vergrößerte Ansicht")
        self.setMinimumSize(1350, 800)
        self.resize(1500, 860)

        self._create_ui()
        self._populate_table()

    def _create_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Geräteübersicht")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Große Tabellenansicht für alle gefilterten Geräte.")
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
        self.table.setRowCount(len(self.equipments))

        for row, equipment in enumerate(self.equipments):
            values = [
                equipment.equipment_id,
                equipment.name,
                equipment.equipment_type,
                equipment.area,
                equipment.status,
                equipment.assigned_employee,
                equipment.next_maintenance,
                equipment.note,
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                if col == 4:
                    if equipment.status == "Aktiv":
                        item.setForeground(QColor("#8df0c4"))
                    elif equipment.status == "Wartung":
                        item.setForeground(QColor("#ffbb72"))
                    elif equipment.status == "Defekt":
                        item.setForeground(QColor("#ff8aa5"))
                    else:
                        item.setForeground(QColor("#9cacd4"))

                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)


class EquipmentPage(QWidget):
    """Geräte-Kontrollzentrum mit scrollbarer Geräte-Wall und scrollbarem Steuerpanel."""

    def __init__(self, controller: Any | None = None) -> None:
        super().__init__()
        self.controller = controller
        self.equipments: list[EquipmentRecord] = []
        self.filtered_equipments: list[EquipmentRecord] = []
        self.selected_equipment_id: str | None = None

        self._create_ui()
        self._load_demo_data()
        self.refresh_data()

    # =========================
    # UI
    # =========================
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

        self.page_content_layout.addWidget(self._create_top_control_center())

        content_row = QHBoxLayout()
        content_row.setSpacing(18)

        self.left_panel = self._create_equipment_wall()
        self.right_panel = self._create_control_panel()

        content_row.addWidget(self.left_panel, 3)
        content_row.addWidget(self.right_panel, 2)

        self.page_content_layout.addLayout(content_row)
        self.page_content_layout.addStretch()

        self.page_scroll.setWidget(self.page_content)
        root_layout.addWidget(self.page_scroll)

    def _create_top_control_center(self) -> QWidget:
        card = QFrame()
        card.setObjectName("dashboardBottomCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        title = QLabel("Geräte-Kontrollzentrum")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel(
            "Geräte überwachen, filtern, auswählen und direkt im Steuerpanel verwalten."
        )
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        top_row = QHBoxLayout()
        top_row.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Geräte suchen nach Name, ID, Bereich oder Mitarbeiter ...")
        self.search_input.textChanged.connect(self.apply_filters)

        self.status_filter = QComboBox()
        self.status_filter.addItems(["Alle Status", "Aktiv", "Wartung", "Defekt", "Reserviert"])
        self.status_filter.currentTextChanged.connect(self.apply_filters)

        self.area_filter = QComboBox()
        self.area_filter.addItems(
            ["Alle Bereiche", "Cardio", "Kraft", "Freihantel", "Eingang", "Kursraum"]
        )
        self.area_filter.currentTextChanged.connect(self.apply_filters)

        self.expand_button = QPushButton("🔍 Alle Geräte als Tabelle")
        self.expand_button.setObjectName("secondaryButton")
        self.expand_button.clicked.connect(self.open_table_dialog)

        top_row.addWidget(self.search_input, 2)
        top_row.addWidget(self.status_filter, 1)
        top_row.addWidget(self.area_filter, 1)
        top_row.addWidget(self.expand_button)

        stats_row = QGridLayout()
        stats_row.setHorizontalSpacing(18)
        stats_row.setVerticalSpacing(18)

        self.total_card = StatCard(
            title="Geräte gesamt",
            value="0",
            subtitle="Alle sichtbaren Geräte",
            icon="🏋",
            accent="blue",
        )
        self.active_card = StatCard(
            title="Aktiv",
            value="0",
            subtitle="Derzeit einsatzbereit",
            icon="✅",
            accent="green",
        )
        self.maintenance_card = StatCard(
            title="Wartung",
            value="0",
            subtitle="Benötigen Prüfung",
            icon="🛠",
            accent="orange",
        )
        self.defect_card = StatCard(
            title="Defekt",
            value="0",
            subtitle="Nicht einsatzbereit",
            icon="⚠",
            accent="red",
        )

        stats_row.addWidget(self.total_card, 0, 0)
        stats_row.addWidget(self.active_card, 0, 1)
        stats_row.addWidget(self.maintenance_card, 0, 2)
        stats_row.addWidget(self.defect_card, 0, 3)

        for col in range(4):
            stats_row.setColumnStretch(col, 1)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(top_row)
        layout.addLayout(stats_row)

        return card

    def _create_equipment_wall(self) -> QWidget:
        container = QFrame()
        container.setObjectName("dashboardBottomCard")
        container.setMinimumHeight(640)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Geräte-Wall")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Klicke auf ein Gerät, um rechts das Steuerpanel zu öffnen.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        self.wall_scroll = QScrollArea()
        self.wall_scroll.setWidgetResizable(True)
        self.wall_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.wall_scroll.setMinimumHeight(520)

        self.scroll_content = QWidget()
        self.cards_grid = QGridLayout(self.scroll_content)
        self.cards_grid.setContentsMargins(0, 0, 0, 0)
        self.cards_grid.setHorizontalSpacing(16)
        self.cards_grid.setVerticalSpacing(16)

        self.wall_scroll.setWidget(self.scroll_content)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.wall_scroll, 1)

        return container

    def _create_control_panel(self) -> QWidget:
        outer_container = QFrame()
        outer_container.setObjectName("dashboardBottomCard")
        outer_container.setMinimumHeight(640)

        outer_layout = QVBoxLayout(outer_container)
        outer_layout.setContentsMargins(18, 18, 18, 18)
        outer_layout.setSpacing(12)

        panel_scroll = QScrollArea()
        panel_scroll.setWidgetResizable(True)
        panel_scroll.setFrameShape(QFrame.Shape.NoFrame)
        panel_scroll.setMinimumHeight(520)

        panel_content = QWidget()
        layout = QVBoxLayout(panel_content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        title = QLabel("Geräte-Steuerpanel")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Status prüfen, Wartung planen und Schnellaktionen ausführen.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        self.selected_name = QLabel("Kein Gerät ausgewählt")
        self.selected_name.setObjectName("dashboardSectionTitle")
        self.selected_name.setWordWrap(True)

        self.selected_status = QLabel("● -")
        self.selected_status.setObjectName("dashboardSectionSubtitle")

        self.detail_id = self._build_detail_label("Geräte-ID", "-")
        self.detail_type = self._build_detail_label("Typ", "-")
        self.detail_area = self._build_detail_label("Bereich", "-")
        self.detail_employee = self._build_detail_label("Mitarbeiter", "-")
        self.detail_maintenance = self._build_detail_label("Nächste Wartung", "-")
        self.detail_note = self._build_detail_label("Notiz", "-")


        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(6)
        layout.addWidget(self.selected_name)
        layout.addWidget(self.selected_status)
        layout.addWidget(self.detail_id)
        layout.addWidget(self.detail_type)
        layout.addWidget(self.detail_area)
        layout.addWidget(self.detail_employee)
        layout.addWidget(self.detail_maintenance)
        layout.addWidget(self.detail_note)
        layout.addStretch()

        panel_scroll.setWidget(panel_content)
        outer_layout.addWidget(panel_scroll)

        return outer_container

    def _build_detail_label(self, title: str, value: str) -> QLabel:
        label = QLabel(f"<b>{title}:</b><br>{value}")
        label.setObjectName("dashboardActivityItem")
        label.setWordWrap(True)
        return label

    # =========================
    # Data
    # =========================
    def _load_demo_data(self) -> None:
        self.equipments = [
            EquipmentRecord("EQ-3001", "Treadmill Alpha", "Cardio", "Cardio", "Aktiv", "Markus Steiner", "20.04.2026", "Läuft stabil"),
            EquipmentRecord("EQ-3002", "Bike Pro X", "Cardio", "Cardio", "Wartung", "Laura Hofer", "17.04.2026", "Kette prüfen"),
            EquipmentRecord("EQ-3003", "Leg Press Max", "Kraft", "Kraft", "Aktiv", "Daniel Fuchs", "28.04.2026", ""),
            EquipmentRecord("EQ-3004", "Bench Station", "Kraft", "Freihantel", "Reserviert", "Julian Kern", "02.05.2026", "Für Umbau markiert"),
            EquipmentRecord("EQ-3005", "Cable Tower Z", "Kraft", "Kraft", "Defekt", "Nina Bauer", "16.04.2026", "Seil beschädigt"),
            EquipmentRecord("EQ-3006", "Row Machine R8", "Cardio", "Cardio", "Aktiv", "Tobias Leitner", "24.04.2026", ""),
            EquipmentRecord("EQ-3007", "Smith Machine", "Kraft", "Freihantel", "Wartung", "Vanessa Moser", "18.04.2026", "Schrauben prüfen"),
            EquipmentRecord("EQ-3008", "Welcome Terminal", "Service", "Eingang", "Aktiv", "Sabrina Wolf", "30.04.2026", "Check-in ok"),
            EquipmentRecord("EQ-3009", "Step Platform Set", "Kursmaterial", "Kursraum", "Reserviert", "Laura Hofer", "10.05.2026", "Für Kursblock reserviert"),
        ]

    def refresh_data(self) -> None:
        if self.controller is not None:
            try:
                equipments = self.controller.get_all_equipments()
                self.equipments = list(equipments)
            except Exception:
                pass

        self.apply_filters()

    def apply_filters(self) -> None:
        search_text = self.search_input.text().strip().lower()
        selected_status = self.status_filter.currentText()
        selected_area = self.area_filter.currentText()

        result: list[EquipmentRecord] = []

        for equipment in self.equipments:
            searchable = " ".join(
                [
                    equipment.equipment_id,
                    equipment.name,
                    equipment.equipment_type,
                    equipment.area,
                    equipment.assigned_employee,
                    equipment.status,
                    equipment.note,
                ]
            ).lower()

            matches_search = search_text in searchable
            matches_status = selected_status == "Alle Status" or equipment.status == selected_status
            matches_area = selected_area == "Alle Bereiche" or equipment.area == selected_area

            if matches_search and matches_status and matches_area:
                result.append(equipment)

        self.filtered_equipments = result
        self._rebuild_equipment_wall()
        self._update_stats()
        

        if self.filtered_equipments:
            if self.selected_equipment_id is None or not any(
                eq.equipment_id == self.selected_equipment_id for eq in self.filtered_equipments
            ):
                self.select_equipment(self.filtered_equipments[0].equipment_id)
            else:
                self.select_equipment(self.selected_equipment_id)
        else:
            self._clear_selected_panel()

    # =========================
    # Wall / Panel
    # =========================
    def _rebuild_equipment_wall(self) -> None:
        while self.cards_grid.count():
            item = self.cards_grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        for index, equipment in enumerate(self.filtered_equipments):
            card = EquipmentUnitCard(equipment)
            card.clicked.connect(self.select_equipment)

            row = index // 2
            col = index % 2
            self.cards_grid.addWidget(card, row, col)

        self.cards_grid.setColumnStretch(0, 1)
        self.cards_grid.setColumnStretch(1, 1)

    def select_equipment(self, equipment_id: str) -> None:
        self.selected_equipment_id = equipment_id

        selected = None
        for equipment in self.filtered_equipments:
            if equipment.equipment_id == equipment_id:
                selected = equipment
                break

        if selected is None:
            self._clear_selected_panel()
            return

        self.selected_name.setText(selected.name)
        self.selected_status.setText(f"● {selected.status}")

        if selected.status == "Aktiv":
            self.selected_status.setObjectName("dashboardStatusOk")
        elif selected.status == "Wartung":
            self.selected_status.setObjectName("dashboardStatusWarn")
        elif selected.status == "Defekt":
            self.selected_status.setObjectName("dashboardStatusCritical")
        else:
            self.selected_status.setObjectName("dashboardSectionSubtitle")

        self.selected_status.style().unpolish(self.selected_status)
        self.selected_status.style().polish(self.selected_status)

        self.detail_id.setText(f"<b>Geräte-ID:</b><br>{selected.equipment_id}")
        self.detail_type.setText(f"<b>Typ:</b><br>{selected.equipment_type}")
        self.detail_area.setText(f"<b>Bereich:</b><br>{selected.area}")
        self.detail_employee.setText(f"<b>Mitarbeiter:</b><br>{selected.assigned_employee}")
        self.detail_maintenance.setText(f"<b>Nächste Wartung:</b><br>{selected.next_maintenance}")
        self.detail_note.setText(f"<b>Notiz:</b><br>{selected.note if selected.note else '-'}")

    def _clear_selected_panel(self) -> None:
        self.selected_name.setText("Kein Gerät ausgewählt")
        self.selected_status.setText("● -")
        self.selected_status.setObjectName("dashboardSectionSubtitle")
        self.selected_status.style().unpolish(self.selected_status)
        self.selected_status.style().polish(self.selected_status)

        self.detail_id.setText("<b>Geräte-ID:</b><br>-")
        self.detail_type.setText("<b>Typ:</b><br>-")
        self.detail_area.setText("<b>Bereich:</b><br>-")
        self.detail_employee.setText("<b>Mitarbeiter:</b><br>-")
        self.detail_maintenance.setText("<b>Nächste Wartung:</b><br>-")
        self.detail_note.setText("<b>Notiz:</b><br>-")



    def _update_stats(self) -> None:
        total = len(self.filtered_equipments)
        active = sum(1 for eq in self.filtered_equipments if eq.status == "Aktiv")
        maintenance = sum(1 for eq in self.filtered_equipments if eq.status == "Wartung")
        defect = sum(1 for eq in self.filtered_equipments if eq.status == "Defekt")

        self.total_card.set_value_animated(total)
        self.active_card.set_value_animated(active)
        self.maintenance_card.set_value_animated(maintenance)
        self.defect_card.set_value_animated(defect)

    # =========================
    # Actions
    # =========================
    def change_selected_status(self, new_status: str) -> None:
        if self.selected_equipment_id is None:
            QMessageBox.warning(self, "Kein Gerät", "Bitte zuerst ein Gerät auswählen.")
            return

        for equipment in self.equipments:
            if equipment.equipment_id == self.selected_equipment_id:
                equipment.status = new_status

                if new_status == "Wartung":
                    equipment.note = "Zur Wartung markiert"
                elif new_status == "Defekt":
                    equipment.note = "Als defekt markiert"
                elif new_status == "Aktiv":
                    equipment.note = "Wieder einsatzbereit"
                elif new_status == "Reserviert":
                    equipment.note = "Für späteren Einsatz reserviert"

                break

        self.apply_filters()

    def open_table_dialog(self) -> None:
        dialog = EquipmentTableDialog(self, self.filtered_equipments)
        dialog.exec()
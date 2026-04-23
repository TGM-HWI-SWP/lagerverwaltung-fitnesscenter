from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QMouseEvent
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
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.ui.widgets.stat_card import StatCard


@dataclass
class EquipmentRecord:
    """Speichert die aufbereiteten Daten eines Geräts."""

    equipment_id: str
    name: str
    equipment_type: str
    area: str
    status: str
    assigned_employee: str
    next_maintenance: str
    note: str


class EquipmentDialog(QDialog):
    """Dialog zum Anlegen eines neuen Geräts."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialisiert den Geräte-Dialog."""
        super().__init__(parent)

        self.setWindowTitle("Gerät hinzufügen")
        self.setModal(True)
        self.setMinimumWidth(520)

        self._create_ui()

    def _create_ui(self) -> None:
        """Erstellt die Oberfläche des Dialogs."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Neues Gerät anlegen")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Gerätedaten erfassen und speichern.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        form_card = QFrame()
        form_card.setObjectName("dashboardBottomCard")

        form = QFormLayout(form_card)
        form.setContentsMargins(18, 18, 18, 18)
        form.setSpacing(14)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("z. B. EQ-3010")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("z. B. Bike Pro X")

        self.type_input = QLineEdit()
        self.type_input.setPlaceholderText("z. B. Cardio")

        self.location_input = QComboBox()
        self.location_input.addItems(
            ["Cardio", "Kraft", "Freihantel", "Eingang", "Kursraum"]
        )

        self.status_input = QComboBox()
        self.status_input.addItems(["Aktiv", "Wartung", "Defekt", "Reserviert"])

        self.employee_input = QLineEdit()
        self.employee_input.setPlaceholderText("Mitarbeiter-ID oder leer")

        form.addRow("Geräte-ID:", self.id_input)
        form.addRow("Name:", self.name_input)
        form.addRow("Typ:", self.type_input)
        form.addRow("Bereich:", self.location_input)
        form.addRow("Status:", self.status_input)
        form.addRow("Mitarbeiter-ID:", self.employee_input)

        button_row = QHBoxLayout()
        button_row.addStretch()

        cancel_button = QPushButton("Abbrechen")
        cancel_button.setObjectName("secondaryButton")
        cancel_button.clicked.connect(self.reject)

        save_button = QPushButton("Speichern")
        save_button.setObjectName("primaryButton")
        save_button.clicked.connect(self._validate_and_accept)

        button_row.addWidget(cancel_button)
        button_row.addWidget(save_button)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(form_card)
        layout.addLayout(button_row)

    def _validate_and_accept(self) -> None:
        """Prüft die Eingaben und bestätigt den Dialog."""
        if not self.id_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte eine Geräte-ID eingeben.")
            return

        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte einen Gerätenamen eingeben.")
            return

        if not self.type_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte einen Gerätetyp eingeben.")
            return

        self.accept()

    def get_data(self) -> dict[str, str]:
        """Gibt die eingegebenen Gerätedaten zurück."""
        status_map = {
            "Aktiv": "available",
            "Wartung": "maintenance",
            "Defekt": "defect",
            "Reserviert": "reserved",
        }

        return {
            "equipment_id": self.id_input.text().strip(),
            "name": self.name_input.text().strip(),
            "equipment_type": self.type_input.text().strip(),
            "location": self.location_input.currentText(),
            "status": status_map.get(self.status_input.currentText(), "available"),
            "assigned_employee_id": self.employee_input.text().strip(),
        }


class AssignEmployeeDialog(QDialog):
    """Dialog zum Zuweisen eines Mitarbeiters."""

    def __init__(
        self,
        parent: QWidget | None = None,
        equipment_name: str = "",
        current_employee: str = "",
    ) -> None:
        """Initialisiert den Zuweisungsdialog."""
        super().__init__(parent)

        self.setWindowTitle("Mitarbeiter zuweisen")
        self.setModal(True)
        self.setMinimumWidth(460)

        self.equipment_name = equipment_name
        self.current_employee = current_employee

        self._create_ui()

    def _create_ui(self) -> None:
        """Erstellt die Oberfläche des Dialogs."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Mitarbeiter zuweisen")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel(
            f"Gerät: {self.equipment_name}\nAktuell: {self.current_employee or '-'}"
        )
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        form_card = QFrame()
        form_card.setObjectName("dashboardBottomCard")

        form = QFormLayout(form_card)
        form.setContentsMargins(18, 18, 18, 18)
        form.setSpacing(14)

        self.employee_input = QLineEdit()
        self.employee_input.setPlaceholderText("Mitarbeiter-ID eingeben")
        if self.current_employee and self.current_employee != "-":
            self.employee_input.setText(self.current_employee)

        form.addRow("Mitarbeiter-ID:", self.employee_input)

        button_row = QHBoxLayout()
        button_row.addStretch()

        cancel_button = QPushButton("Abbrechen")
        cancel_button.setObjectName("secondaryButton")
        cancel_button.clicked.connect(self.reject)

        save_button = QPushButton("Zuweisen")
        save_button.setObjectName("primaryButton")
        save_button.clicked.connect(self._validate_and_accept)

        button_row.addWidget(cancel_button)
        button_row.addWidget(save_button)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(form_card)
        layout.addLayout(button_row)

    def _validate_and_accept(self) -> None:
        """Prüft die Eingabe und bestätigt den Dialog."""
        if not self.employee_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte eine Mitarbeiter-ID eingeben.")
            return

        self.accept()

    def get_employee_id(self) -> str:
        """Gibt die eingegebene Mitarbeiter-ID zurück."""
        return self.employee_input.text().strip()


class EquipmentUnitCard(QFrame):
    """Große klickbare Karte für ein Gerät."""

    clicked = pyqtSignal(str)

    def __init__(self, equipment: EquipmentRecord, parent: QWidget | None = None) -> None:
        """Initialisiert die Gerätekarte."""
        super().__init__(parent)

        self.equipment = equipment

        self.setObjectName("dashboardBottomCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(210)
        self.setMaximumHeight(240)

        self._create_ui()

    def _create_ui(self) -> None:
        """Erstellt die Inhalte der Gerätekarte."""
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
        """Setzt den Stil des Status-Badges."""
        if status == "Aktiv":
            label.setObjectName("dashboardStatusOk")
        elif status == "Wartung":
            label.setObjectName("dashboardStatusWarn")
        elif status == "Defekt":
            label.setObjectName("dashboardStatusCritical")
        else:
            label.setObjectName("dashboardSectionSubtitle")

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Sendet das Klicksignal bei linker Maustaste."""
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
        """Initialisiert den Tabellen-Dialog."""
        super().__init__(parent)

        self.equipments = equipments or []

        self.setWindowTitle("Geräteübersicht - vergrößerte Ansicht")
        self.setMinimumSize(1350, 800)
        self.resize(1500, 860)

        self._create_ui()
        self._populate_table()

    def _create_ui(self) -> None:
        """Erstellt die Oberfläche der Tabellenansicht."""
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
        """Füllt die Tabelle mit allen übergebenen Geräten."""
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
    """Seite zur Verwaltung, Überwachung und Steuerung aller Geräte."""

    def __init__(self, controller: Any | None = None) -> None:
        """Initialisiert die Geräteseite."""
        super().__init__()

        self.controller = controller
        self.equipments: list[EquipmentRecord] = []
        self.filtered_equipments: list[EquipmentRecord] = []
        self.selected_equipment_id: str | None = None

        self._create_ui()
        self.refresh_data()

    def _create_ui(self) -> None:
        """Erstellt die komplette Oberfläche der Seite."""
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
        """Erstellt Such-, Filter- und Statistikbereich."""
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
        self.search_input.setPlaceholderText(
            "Geräte suchen nach Name, ID, Bereich oder Mitarbeiter ..."
        )
        self.search_input.textChanged.connect(self.apply_filters)

        self.status_filter = QComboBox()
        self.status_filter.addItems(["Alle Status", "Aktiv", "Wartung", "Defekt", "Reserviert"])
        self.status_filter.currentTextChanged.connect(self.apply_filters)

        self.area_filter = QComboBox()
        self.area_filter.addItems(
            ["Alle Bereiche", "Cardio", "Kraft", "Freihantel", "Eingang", "Kursraum"]
        )
        self.area_filter.currentTextChanged.connect(self.apply_filters)

        self.add_button = QPushButton("➕ Gerät hinzufügen")
        self.add_button.setObjectName("primaryButton")
        self.add_button.clicked.connect(self.create_equipment)

        self.expand_button = QPushButton("🔍 Alle Geräte als Tabelle")
        self.expand_button.setObjectName("secondaryButton")
        self.expand_button.clicked.connect(self.open_table_dialog)

        top_row.addWidget(self.search_input, 2)
        top_row.addWidget(self.status_filter, 1)
        top_row.addWidget(self.area_filter, 1)
        top_row.addWidget(self.add_button)
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
        """Erstellt die Kartenansicht aller gefilterten Geräte."""
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
        """Erstellt das rechte Steuerpanel für das ausgewählte Gerät."""
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

        subtitle = QLabel("Status prüfen, Mitarbeiter zuweisen und Gerätedetails anzeigen.")
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

        status_buttons_row_1 = QHBoxLayout()
        status_buttons_row_1.setSpacing(10)

        self.active_button = QPushButton("✅ Aktiv")
        self.active_button.setObjectName("secondaryButton")
        self.active_button.clicked.connect(lambda: self.change_selected_status("Aktiv"))

        self.maintenance_button = QPushButton("🛠 Wartung")
        self.maintenance_button.setObjectName("secondaryButton")
        self.maintenance_button.clicked.connect(lambda: self.change_selected_status("Wartung"))

        status_buttons_row_1.addWidget(self.active_button)
        status_buttons_row_1.addWidget(self.maintenance_button)

        status_buttons_row_2 = QHBoxLayout()
        status_buttons_row_2.setSpacing(10)

        self.defect_button = QPushButton("⚠ Defekt")
        self.defect_button.setObjectName("secondaryButton")
        self.defect_button.clicked.connect(lambda: self.change_selected_status("Defekt"))

        self.reserved_button = QPushButton("📌 Reserviert")
        self.reserved_button.setObjectName("secondaryButton")
        self.reserved_button.clicked.connect(lambda: self.change_selected_status("Reserviert"))

        status_buttons_row_2.addWidget(self.defect_button)
        status_buttons_row_2.addWidget(self.reserved_button)

        action_row = QHBoxLayout()
        action_row.setSpacing(10)

        self.assign_button = QPushButton("👤 Mitarbeiter zuweisen")
        self.assign_button.setObjectName("secondaryButton")
        self.assign_button.clicked.connect(self.assign_employee_to_selected)

        self.delete_button = QPushButton("🗑 Gerät löschen")
        self.delete_button.setObjectName("secondaryButton")
        self.delete_button.clicked.connect(self.delete_selected_equipment)

        action_row.addWidget(self.assign_button)
        action_row.addWidget(self.delete_button)

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
        layout.addSpacing(8)
        layout.addLayout(status_buttons_row_1)
        layout.addLayout(status_buttons_row_2)
        layout.addLayout(action_row)
        layout.addStretch()

        panel_scroll.setWidget(panel_content)
        outer_layout.addWidget(panel_scroll)

        return outer_container

    def _build_detail_label(self, title: str, value: str) -> QLabel:
        """Erstellt ein Detail-Label für das Steuerpanel."""
        label = QLabel(f"<b>{title}:</b><br>{value}")
        label.setObjectName("dashboardActivityItem")
        label.setWordWrap(True)
        return label

    def _map_equipment_to_record(self, equipment: Any) -> EquipmentRecord:
        """Wandelt ein Controller-Objekt in ein EquipmentRecord um."""
        equipment_id = getattr(equipment, "equipment_id", "") or ""
        name = getattr(equipment, "name", "") or ""
        equipment_type = getattr(equipment, "equipment_type", "") or ""
        location = getattr(equipment, "location", "") or ""
        raw_status = getattr(equipment, "status", "") or ""
        assigned_employee_id = getattr(equipment, "assigned_employee_id", "") or ""

        status_map = {
            "available": "Aktiv",
            "active": "Aktiv",
            "maintenance": "Wartung",
            "defect": "Defekt",
            "reserved": "Reserviert",
        }

        status = status_map.get(
            str(raw_status).lower(),
            str(raw_status) if raw_status else "-"
        )

        return EquipmentRecord(
            equipment_id=equipment_id,
            name=name,
            equipment_type=equipment_type,
            area=location,
            status=status,
            assigned_employee=assigned_employee_id if assigned_employee_id else "-",
            next_maintenance="-",
            note="",
        )

    def _get_selected_equipment(self) -> EquipmentRecord | None:
        """Gibt das aktuell ausgewählte Gerät zurück."""
        if self.selected_equipment_id is None:
            return None

        for equipment in self.filtered_equipments:
            if equipment.equipment_id == self.selected_equipment_id:
                return equipment

        return None

    def refresh_data(self) -> None:
        """Lädt Gerätedaten neu und aktualisiert die Ansicht."""
        try:
            if self.controller is not None:
                equipments = self.controller.get_all_equipment()
                self.equipments = [self._map_equipment_to_record(eq) for eq in equipments]
            else:
                self.equipments = []

            self.apply_filters()
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Geräte konnten nicht geladen werden:\n{error}",
            )
            self.equipments = []
            self.filtered_equipments = []
            self._rebuild_equipment_wall()
            self._update_stats()
            self._clear_selected_panel()

    def apply_filters(self) -> None:
        """Filtert Geräte nach Suche, Status und Bereich."""
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

    def _rebuild_equipment_wall(self) -> None:
        """Erstellt die Kartenansicht der Geräte neu."""
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
        """Wählt ein Gerät aus und aktualisiert das Steuerpanel."""
        self.selected_equipment_id = equipment_id
        selected = self._get_selected_equipment()

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
        """Setzt das Steuerpanel auf den Standardzustand zurück."""
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
        """Aktualisiert die Kennzahlenkarten."""
        total = len(self.filtered_equipments)
        active = sum(1 for eq in self.filtered_equipments if eq.status == "Aktiv")
        maintenance = sum(1 for eq in self.filtered_equipments if eq.status == "Wartung")
        defect = sum(1 for eq in self.filtered_equipments if eq.status == "Defekt")

        self.total_card.set_value_animated(total)
        self.active_card.set_value_animated(active)
        self.maintenance_card.set_value_animated(maintenance)
        self.defect_card.set_value_animated(defect)

    def create_equipment(self) -> None:
        """Erstellt ein neues Gerät."""
        dialog = EquipmentDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.get_data()

        try:
            if self.controller is None:
                QMessageBox.warning(self, "Fehler", "Kein Controller vorhanden.")
                return

            self.controller.create_equipment(
                equipment_id=data["equipment_id"],
                name=data["name"],
                equipment_type=data["equipment_type"],
                location=data["location"],
                status=data["status"],
                assigned_employee_id=data["assigned_employee_id"],
            )

            self.refresh_data()
            QMessageBox.information(
                self,
                "Erfolg",
                f"Gerät '{data['name']}' wurde erfolgreich erstellt.",
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Gerät konnte nicht erstellt werden:\n{error}",
            )

    def change_selected_status(self, new_status: str) -> None:
        """Ändert den Status des ausgewählten Geräts."""
        if self.selected_equipment_id is None:
            QMessageBox.warning(self, "Kein Gerät", "Bitte zuerst ein Gerät auswählen.")
            return

        if self.controller is None:
            QMessageBox.warning(self, "Fehler", "Kein Controller vorhanden.")
            return

        status_map = {
            "Aktiv": "available",
            "Wartung": "maintenance",
            "Defekt": "defect",
            "Reserviert": "reserved",
        }

        backend_status = status_map.get(new_status, new_status)

        try:
            self.controller.update_equipment_status(self.selected_equipment_id, backend_status)
            self.refresh_data()
            QMessageBox.information(
                self,
                "Erfolg",
                f"Status wurde auf '{new_status}' geändert.",
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Gerätestatus konnte nicht geändert werden:\n{error}",
            )

    def assign_employee_to_selected(self) -> None:
        """Weist dem ausgewählten Gerät einen Mitarbeiter zu."""
        selected = self._get_selected_equipment()
        if selected is None:
            QMessageBox.warning(self, "Kein Gerät", "Bitte zuerst ein Gerät auswählen.")
            return

        dialog = AssignEmployeeDialog(
            self,
            equipment_name=selected.name,
            current_employee=selected.assigned_employee,
        )

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        employee_id = dialog.get_employee_id()

        try:
            if self.controller is None:
                QMessageBox.warning(self, "Fehler", "Kein Controller vorhanden.")
                return

            self.controller.assign_employee_to_equipment(
                self.selected_equipment_id,
                employee_id,
            )
            self.refresh_data()
            QMessageBox.information(
                self,
                "Erfolg",
                f"Mitarbeiter '{employee_id}' wurde zugewiesen.",
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Mitarbeiter konnte nicht zugewiesen werden:\n{error}",
            )

    def delete_selected_equipment(self) -> None:
        """Löscht das ausgewählte Gerät."""
        selected = self._get_selected_equipment()
        if selected is None:
            QMessageBox.warning(self, "Kein Gerät", "Bitte zuerst ein Gerät auswählen.")
            return

        answer = QMessageBox.question(
            self,
            "Gerät löschen",
            (
                f"Möchtest du das Gerät '{selected.name}' "
                f"mit der ID '{selected.equipment_id}' wirklich löschen?"
            ),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            if self.controller is None:
                QMessageBox.warning(self, "Fehler", "Kein Controller vorhanden.")
                return

            self.controller.delete_equipment(self.selected_equipment_id)
            self.selected_equipment_id = None
            self.refresh_data()
            QMessageBox.information(
                self,
                "Erfolg",
                f"Gerät '{selected.name}' wurde gelöscht.",
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Gerät konnte nicht gelöscht werden:\n{error}",
            )

    def open_table_dialog(self) -> None:
        """Öffnet die große Tabellenansicht der Geräte."""
        dialog = EquipmentTableDialog(self, self.filtered_equipments)
        dialog.exec()
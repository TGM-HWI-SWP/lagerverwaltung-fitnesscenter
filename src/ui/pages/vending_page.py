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
class VendingMachineRecord:
    """Speichert die aufbereiteten Daten eines Automaten."""

    machine_id: str
    location: str
    machine_type: str
    assigned_employee: str
    status: str
    note: str


class VendingMachineDialog(QDialog):
    """Dialog zum Anlegen eines neuen Automaten."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialisiert den Automaten-Dialog."""
        super().__init__(parent)

        self.setWindowTitle("Automat hinzufügen")
        self.setModal(True)
        self.setMinimumWidth(520)

        self._create_ui()

    def _create_ui(self) -> None:
        """Erstellt die Oberfläche des Dialogs."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Neuen Automaten anlegen")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Standort, Typ und Mitarbeiterzuweisung erfassen.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        form_card = QFrame()
        form_card.setObjectName("dashboardBottomCard")

        form = QFormLayout(form_card)
        form.setContentsMargins(18, 18, 18, 18)
        form.setSpacing(14)

        self.machine_id_input = QLineEdit()
        self.machine_id_input.setPlaceholderText("z. B. VM-1004")

        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("z. B. Eingang, Lounge, Obergeschoss")

        self.type_input = QComboBox()
        self.type_input.addItems(["Snack", "Getränke", "Combo", "Sonstiges"])

        self.employee_input = QLineEdit()
        self.employee_input.setPlaceholderText("Mitarbeiter-ID optional")

        form.addRow("Maschinen-ID:", self.machine_id_input)
        form.addRow("Standort:", self.location_input)
        form.addRow("Typ:", self.type_input)
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
        if not self.machine_id_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte eine Maschinen-ID eingeben.")
            return

        if not self.location_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte einen Standort eingeben.")
            return

        self.accept()

    def get_data(self) -> dict[str, str]:
        """Gibt die eingegebenen Automatendaten zurück."""
        return {
            "machine_id": self.machine_id_input.text().strip(),
            "location": self.location_input.text().strip(),
            "machine_type": self.type_input.currentText(),
            "assigned_employee_id": self.employee_input.text().strip(),
        }


class AssignMachineEmployeeDialog(QDialog):
    """Dialog zum Zuweisen eines Mitarbeiters an einen Automaten."""

    def __init__(
        self,
        parent: QWidget | None = None,
        machine_name: str = "",
        current_employee: str = "",
    ) -> None:
        """Initialisiert den Zuweisungsdialog."""
        super().__init__(parent)

        self.setWindowTitle("Mitarbeiter zuweisen")
        self.setModal(True)
        self.setMinimumWidth(460)

        self.machine_name = machine_name
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
            f"Automat: {self.machine_name}\nAktuell: {self.current_employee or '-'}"
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


class VendingMachineCard(QFrame):
    """Große klickbare Karte für einen Automaten."""

    clicked = pyqtSignal(str)

    def __init__(self, machine: VendingMachineRecord, parent: QWidget | None = None) -> None:
        """Initialisiert die Automaten-Karte."""
        super().__init__(parent)

        self.machine = machine
        self.is_selected = False

        self.setObjectName("dashboardBottomCard")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(220)
        self.setMaximumHeight(240)
        self.setProperty("selectedMachine", False)

        self._create_ui()
        self._refresh_style()

    def _create_ui(self) -> None:
        """Erstellt die Inhalte der Karte."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        top_row = QHBoxLayout()
        top_row.setSpacing(10)

        self.id_badge = QLabel(self.machine.machine_id)
        self.id_badge.setObjectName("dashboardHealthBadge")

        self.status_badge = QLabel(f"● {self.machine.status}")
        self._apply_status_style(self.status_badge, self.machine.status)

        top_row.addWidget(self.id_badge)
        top_row.addStretch()
        top_row.addWidget(self.status_badge)

        self.icon_label = QLabel(self._get_machine_icon())
        self.icon_label.setObjectName("dashboardSectionTitle")
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.location_label = QLabel(self.machine.location)
        self.location_label.setObjectName("dashboardSectionTitle")
        self.location_label.setWordWrap(True)
        self.location_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.type_label = QLabel(self.machine.machine_type)
        self.type_label.setObjectName("dashboardSectionSubtitle")
        self.type_label.setWordWrap(True)
        self.type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.employee_label = QLabel(f"Mitarbeiter: {self.machine.assigned_employee}")
        self.employee_label.setObjectName("dashboardActivityItem")
        self.employee_label.setWordWrap(True)
        self.employee_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.note_label = QLabel(
            f"Notiz: {self.machine.note if self.machine.note else '-'}"
        )
        self.note_label.setObjectName("dashboardSectionSubtitle")
        self.note_label.setWordWrap(True)
        self.note_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(top_row)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.location_label)
        layout.addWidget(self.type_label)
        layout.addSpacing(4)
        layout.addWidget(self.employee_label)
        layout.addWidget(self.note_label)
        layout.addStretch()

    def _get_machine_icon(self) -> str:
        """Liefert ein passendes Symbol für den Automatentyp."""
        machine_type = self.machine.machine_type.lower()
        if "drink" in machine_type or "getränk" in machine_type:
            return "🥤"
        if "snack" in machine_type:
            return "🍫"
        if "combo" in machine_type or "mixed" in machine_type:
            return "🥤"
        return "🏧"

    def _apply_status_style(self, label: QLabel, status: str) -> None:
        """Setzt den Stil des Status-Badges."""
        if status == "Aktiv":
            label.setObjectName("dashboardStatusOk")
        else:
            label.setObjectName("dashboardStatusCritical")

    def set_selected(self, selected: bool) -> None:
        """Markiert die Karte als ausgewählt oder nicht ausgewählt."""
        self.is_selected = selected
        self.setProperty("selectedMachine", selected)
        self._refresh_style()

    def _refresh_style(self) -> None:
        """Aktualisiert den Stil der Karte."""
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        """Sendet das Klicksignal bei linker Maustaste."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.machine.machine_id)
        super().mouseReleaseEvent(event)


class VendingTableDialog(QDialog):
    """Große Tabellenansicht für Automaten."""

    TABLE_COLUMNS = [
        "Maschinen-ID",
        "Standort",
        "Typ",
        "Zugewiesener Mitarbeiter",
        "Status",
        "Notiz",
    ]

    def __init__(
        self,
        parent: QWidget | None = None,
        machines: list[VendingMachineRecord] | None = None,
    ) -> None:
        """Initialisiert den Tabellen-Dialog."""
        super().__init__(parent)

        self.machines = machines or []

        self.setWindowTitle("Automaten-Übersicht - vergrößerte Ansicht")
        self.setMinimumSize(1250, 760)
        self.resize(1380, 820)

        self._create_ui()
        self._populate_table()

    def _create_ui(self) -> None:
        """Erstellt die Oberfläche der großen Tabellenansicht."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Automaten-Übersicht")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Große Tabellenansicht aller gefilterten Automaten.")
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
        """Füllt die Tabelle mit allen übergebenen Automaten."""
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(self.machines))
        self.table.clearContents()

        for row, machine in enumerate(self.machines):
            values = [
                machine.machine_id,
                machine.location,
                machine.machine_type,
                machine.assigned_employee,
                machine.status,
                machine.note,
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                if col == 4:
                    if machine.status == "Aktiv":
                        item.setForeground(QColor("#8df0c4"))
                    else:
                        item.setForeground(QColor("#ff8aa5"))

                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)


class VendingPage(QWidget):
    """Seite zur Verwaltung und Übersicht aller Automaten."""

    TABLE_COLUMNS = [
        "Maschinen-ID",
        "Standort",
        "Typ",
        "Zugewiesener Mitarbeiter",
        "Status",
        "Notiz",
    ]

    def __init__(self, controller: Any | None = None) -> None:
        """Initialisiert die Automatenseite."""
        super().__init__()

        self.controller = controller
        self.machines: list[VendingMachineRecord] = []
        self.filtered_machines: list[VendingMachineRecord] = []
        self.selected_machine_id: str | None = None
        self.machine_cards: dict[str, VendingMachineCard] = {}

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
        """Erstellt Suchbereich, Filter und Kennzahlen."""
        card = QFrame()
        card.setObjectName("dashboardBottomCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        title = QLabel("Automatenverwaltung")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel(
            "Verwaltung der vorhandenen Automaten mit Standort, Typ, Zuständigkeit und Aktivstatus."
        )
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        controls = QHBoxLayout()
        controls.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Suche nach Maschinen-ID, Standort, Typ oder Mitarbeiter ..."
        )
        self.search_input.textChanged.connect(self.apply_filters)

        self.status_filter = QComboBox()
        self.status_filter.addItems(["Alle Status", "Aktiv", "Inaktiv"])
        self.status_filter.currentTextChanged.connect(self.apply_filters)

        self.type_filter = QComboBox()
        self.type_filter.addItems(
            ["Alle Typen", "Snack", "Getränke", "Combo", "Sonstiges"]
        )
        self.type_filter.currentTextChanged.connect(self.apply_filters)

        self.add_button = QPushButton("➕ Automat hinzufügen")
        self.add_button.setObjectName("primaryButton")
        self.add_button.clicked.connect(self.create_machine)

        self.expand_button = QPushButton("🔍 Tabelle vergrößern")
        self.expand_button.setObjectName("secondaryButton")
        self.expand_button.clicked.connect(self.open_table_dialog)

        controls.addWidget(self.search_input, 2)
        controls.addWidget(self.status_filter, 1)
        controls.addWidget(self.type_filter, 1)
        controls.addWidget(self.add_button)
        controls.addWidget(self.expand_button)

        stats = QGridLayout()
        stats.setHorizontalSpacing(18)
        stats.setVerticalSpacing(18)

        self.machine_count_card = StatCard(
            title="Automaten gesamt",
            value="0",
            subtitle="Alle sichtbaren Automaten",
            icon="🥤",
            accent="blue",
        )
        self.active_card = StatCard(
            title="Aktiv",
            value="0",
            subtitle="Aktiv geschaltete Automaten",
            icon="✅",
            accent="green",
        )
        self.inactive_card = StatCard(
            title="Inaktiv",
            value="0",
            subtitle="Deaktivierte Automaten",
            icon="⚠",
            accent="red",
        )
        self.assigned_card = StatCard(
            title="Zugewiesen",
            value="0",
            subtitle="Mit Mitarbeiter-Zuordnung",
            icon="👤",
            accent="orange",
        )

        stats.addWidget(self.machine_count_card, 0, 0)
        stats.addWidget(self.active_card, 0, 1)
        stats.addWidget(self.inactive_card, 0, 2)
        stats.addWidget(self.assigned_card, 0, 3)

        for col in range(4):
            stats.setColumnStretch(col, 1)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(controls)
        layout.addLayout(stats)

        return card

    def _create_machine_visual(self) -> QWidget:
        """Erstellt die Kartenansicht der Automaten."""
        container = QFrame()
        container.setObjectName("dashboardBottomCard")
        container.setMinimumHeight(620)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Automatenübersicht")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Klicke auf einen Automaten, um rechts die Details zu sehen.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        self.machine_scroll = QScrollArea()
        self.machine_scroll.setWidgetResizable(True)
        self.machine_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.machine_scroll.setMinimumHeight(500)

        self.machine_content = QWidget()
        self.machine_grid = QGridLayout(self.machine_content)
        self.machine_grid.setContentsMargins(0, 0, 0, 0)
        self.machine_grid.setHorizontalSpacing(16)
        self.machine_grid.setVerticalSpacing(16)

        self.machine_scroll.setWidget(self.machine_content)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.machine_scroll, 1)

        return container

    def _create_detail_panel(self) -> QWidget:
        """Erstellt das rechte Detailpanel."""
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

        title = QLabel("Automaten-Details")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Detailansicht des aktuell ausgewählten Automaten.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        self.selected_machine = QLabel("Kein Automat ausgewählt")
        self.selected_machine.setObjectName("dashboardSectionTitle")
        self.selected_machine.setWordWrap(True)

        self.selected_status = QLabel("● -")
        self.selected_status.setObjectName("dashboardSectionSubtitle")

        self.detail_id = self._build_detail_label("Maschinen-ID", "-")
        self.detail_location = self._build_detail_label("Standort", "-")
        self.detail_type = self._build_detail_label("Typ", "-")
        self.detail_employee = self._build_detail_label("Zugewiesener Mitarbeiter", "-")
        self.detail_status = self._build_detail_label("Status", "-")
        self.detail_note = self._build_detail_label("Notiz", "-")

        button_row_1 = QHBoxLayout()
        button_row_1.setSpacing(10)

        self.activate_button = QPushButton("✅ Aktivieren")
        self.activate_button.setObjectName("secondaryButton")
        self.activate_button.clicked.connect(self.activate_selected_machine)

        self.deactivate_button = QPushButton("⛔ Deaktivieren")
        self.deactivate_button.setObjectName("secondaryButton")
        self.deactivate_button.clicked.connect(self.deactivate_selected_machine)

        button_row_1.addWidget(self.activate_button)
        button_row_1.addWidget(self.deactivate_button)

        button_row_2 = QHBoxLayout()
        button_row_2.setSpacing(10)

        self.assign_button = QPushButton("👤 Mitarbeiter zuweisen")
        self.assign_button.setObjectName("secondaryButton")
        self.assign_button.clicked.connect(self.assign_employee_to_selected_machine)

        self.delete_button = QPushButton("🗑 Löschen")
        self.delete_button.setObjectName("secondaryButton")
        self.delete_button.clicked.connect(self.delete_selected_machine)

        button_row_2.addWidget(self.assign_button)
        button_row_2.addWidget(self.delete_button)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(8)
        layout.addWidget(self.selected_machine)
        layout.addWidget(self.selected_status)
        layout.addWidget(self.detail_id)
        layout.addWidget(self.detail_location)
        layout.addWidget(self.detail_type)
        layout.addWidget(self.detail_employee)
        layout.addWidget(self.detail_status)
        layout.addWidget(self.detail_note)
        layout.addSpacing(8)
        layout.addLayout(button_row_1)
        layout.addLayout(button_row_2)
        layout.addStretch()

        panel_scroll.setWidget(panel_content)
        outer_layout.addWidget(panel_scroll)

        return outer_container

    def _create_table_section(self) -> QWidget:
        """Erstellt die tabellarische Übersicht der Automaten."""
        card = QFrame()
        card.setObjectName("dashboardBottomCard")
        card.setMinimumHeight(360)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Automaten-Tabelle")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Klassische Tabellenansicht aller gefilterten Automaten.")
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
        """Erstellt ein Detail-Label für das rechte Panel."""
        label = QLabel(f"<b>{title}:</b><br>{value}")
        label.setObjectName("dashboardActivityItem")
        label.setWordWrap(True)
        return label

    def _map_machine_to_record(self, machine: Any) -> VendingMachineRecord:
        """Wandelt ein Controller-Objekt in ein VendingMachineRecord um."""
        machine_id = getattr(machine, "machine_id", "") or ""
        location = getattr(machine, "location", "") or ""
        machine_type = getattr(machine, "machine_type", "") or ""
        assigned_employee_id = getattr(machine, "assigned_employee_id", "") or ""
        active = getattr(machine, "active", False)

        status = "Aktiv" if active else "Inaktiv"

        return VendingMachineRecord(
            machine_id=machine_id,
            location=location,
            machine_type=machine_type if machine_type else "Sonstiges",
            assigned_employee=assigned_employee_id if assigned_employee_id else "-",
            status=status,
            note="",
        )

    def _find_machine(self, machine_id: str | None) -> VendingMachineRecord | None:
        """Sucht einen Automaten anhand seiner ID."""
        if machine_id is None:
            return None

        for machine in self.filtered_machines:
            if machine.machine_id == machine_id:
                return machine

        return None

    def refresh_data(self) -> None:
        """Lädt Automatendaten neu und aktualisiert die Ansicht."""
        try:
            if self.controller is not None:
                machines = self.controller.get_all_machines()
                self.machines = [self._map_machine_to_record(machine) for machine in machines]
            else:
                self.machines = []

            self.apply_filters()
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Automaten konnten nicht geladen werden:\n{error}",
            )
            self.machines = []
            self.apply_filters()

    def apply_filters(self) -> None:
        """Filtert Automaten nach Suche, Status und Typ."""
        search_text = self.search_input.text().strip().lower()
        selected_status = self.status_filter.currentText()
        selected_type = self.type_filter.currentText()

        result: list[VendingMachineRecord] = []

        for machine in self.machines:
            searchable = " ".join(
                [
                    machine.machine_id,
                    machine.location,
                    machine.machine_type,
                    machine.assigned_employee,
                    machine.status,
                    machine.note,
                ]
            ).lower()

            matches_search = search_text in searchable
            matches_status = selected_status == "Alle Status" or machine.status == selected_status
            matches_type = selected_type == "Alle Typen" or machine.machine_type == selected_type

            if matches_search and matches_status and matches_type:
                result.append(machine)

        self.filtered_machines = result
        self._rebuild_machine_visual()
        self._populate_table()
        self._update_stats()

        if self.filtered_machines:
            current = self._find_machine(self.selected_machine_id)
            if current is None:
                self.select_machine(self.filtered_machines[0].machine_id)
            else:
                self.select_machine(current.machine_id)
        else:
            self._clear_detail_panel()

    def _rebuild_machine_visual(self) -> None:
        """Erstellt die Kartenansicht der gefilterten Automaten neu."""
        while self.machine_grid.count():
            item = self.machine_grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.machine_cards.clear()

        for index, machine in enumerate(self.filtered_machines):
            card = VendingMachineCard(machine)
            card.clicked.connect(self.select_machine)
            self.machine_cards[machine.machine_id] = card

            row = index // 2
            col = index % 2
            self.machine_grid.addWidget(card, row, col)

        self.machine_grid.setColumnStretch(0, 1)
        self.machine_grid.setColumnStretch(1, 1)

    def _populate_table(self) -> None:
        """Füllt die Tabelle mit den gefilterten Automaten."""
        self.vending_table.setSortingEnabled(False)
        self.vending_table.setRowCount(len(self.filtered_machines))
        self.vending_table.clearContents()

        for row, machine in enumerate(self.filtered_machines):
            values = [
                machine.machine_id,
                machine.location,
                machine.machine_type,
                machine.assigned_employee,
                machine.status,
                machine.note,
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                if col == 4:
                    if machine.status == "Aktiv":
                        item.setForeground(QColor("#8df0c4"))
                    else:
                        item.setForeground(QColor("#ff8aa5"))

                self.vending_table.setItem(row, col, item)

        self.vending_table.resizeColumnsToContents()
        self.vending_table.setSortingEnabled(True)

        if self.filtered_machines and self.vending_table.rowCount() > 0:
            self.vending_table.selectRow(0)

    def _select_from_table(self) -> None:
        """Übernimmt die Auswahl aus der Tabelle."""
        row = self.vending_table.currentRow()
        if row < 0:
            return

        machine_item = self.vending_table.item(row, 0)
        if machine_item is None:
            return

        self.select_machine(machine_item.text())

    def select_machine(self, machine_id: str) -> None:
        """Wählt einen Automaten aus und aktualisiert die Detailansicht."""
        self.selected_machine_id = machine_id
        selected = self._find_machine(machine_id)

        if selected is None:
            self._clear_detail_panel()
            return

        self.selected_machine.setText(f"Automat {selected.machine_id}")
        self.selected_status.setText(f"● {selected.status}")

        if selected.status == "Aktiv":
            self.selected_status.setObjectName("dashboardStatusOk")
        else:
            self.selected_status.setObjectName("dashboardStatusCritical")

        self.selected_status.style().unpolish(self.selected_status)
        self.selected_status.style().polish(self.selected_status)

        self.detail_id.setText(f"<b>Maschinen-ID:</b><br>{selected.machine_id}")
        self.detail_location.setText(f"<b>Standort:</b><br>{selected.location}")
        self.detail_type.setText(f"<b>Typ:</b><br>{selected.machine_type}")
        self.detail_employee.setText(f"<b>Zugewiesener Mitarbeiter:</b><br>{selected.assigned_employee}")
        self.detail_status.setText(f"<b>Status:</b><br>{selected.status}")
        self.detail_note.setText(f"<b>Notiz:</b><br>{selected.note if selected.note else '-'}")

        for current_id, card in self.machine_cards.items():
            card.set_selected(current_id == machine_id)

    def _clear_detail_panel(self) -> None:
        """Setzt die Detailansicht auf den Standardzustand zurück."""
        self.selected_machine.setText("Kein Automat ausgewählt")
        self.selected_status.setText("● -")
        self.selected_status.setObjectName("dashboardSectionSubtitle")
        self.selected_status.style().unpolish(self.selected_status)
        self.selected_status.style().polish(self.selected_status)

        self.detail_id.setText("<b>Maschinen-ID:</b><br>-")
        self.detail_location.setText("<b>Standort:</b><br>-")
        self.detail_type.setText("<b>Typ:</b><br>-")
        self.detail_employee.setText("<b>Zugewiesener Mitarbeiter:</b><br>-")
        self.detail_status.setText("<b>Status:</b><br>-")
        self.detail_note.setText("<b>Notiz:</b><br>-")

        for card in self.machine_cards.values():
            card.set_selected(False)

    def _update_stats(self) -> None:
        """Aktualisiert die Kennzahlenkarten."""
        machines_total = len(self.filtered_machines)
        active = sum(1 for machine in self.filtered_machines if machine.status == "Aktiv")
        inactive = sum(1 for machine in self.filtered_machines if machine.status == "Inaktiv")
        assigned = sum(
            1 for machine in self.filtered_machines
            if machine.assigned_employee and machine.assigned_employee != "-"
        )

        self.machine_count_card.set_value_animated(machines_total)
        self.active_card.set_value_animated(active)
        self.inactive_card.set_value_animated(inactive)
        self.assigned_card.set_value_animated(assigned)

    def create_machine(self) -> None:
        """Erstellt einen neuen Automaten."""
        dialog = VendingMachineDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.get_data()

        try:
            if self.controller is None:
                QMessageBox.warning(self, "Fehler", "Kein Controller vorhanden.")
                return

            self.controller.create_machine(
                machine_id=data["machine_id"],
                location=data["location"],
                machine_type=data["machine_type"],
                assigned_employee_id=data["assigned_employee_id"],
            )
            self.refresh_data()
            QMessageBox.information(
                self,
                "Erfolg",
                f"Automat '{data['machine_id']}' wurde erfolgreich erstellt.",
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Automat konnte nicht erstellt werden:\n{error}",
            )

    def assign_employee_to_selected_machine(self) -> None:
        """Weist dem ausgewählten Automaten einen Mitarbeiter zu."""
        selected = self._find_machine(self.selected_machine_id)
        if selected is None:
            QMessageBox.warning(self, "Kein Automat", "Bitte zuerst einen Automaten auswählen.")
            return

        if self.controller is None:
            QMessageBox.warning(self, "Fehler", "Kein Controller vorhanden.")
            return

        dialog = AssignMachineEmployeeDialog(
            self,
            machine_name=selected.machine_id,
            current_employee=selected.assigned_employee,
        )

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        employee_id = dialog.get_employee_id()

        try:
            self.controller.assign_employee_to_machine(
                selected.machine_id,
                employee_id,
            )
            self.refresh_data()
            QMessageBox.information(
                self,
                "Erfolg",
                f"Mitarbeiter '{employee_id}' wurde dem Automaten zugewiesen.",
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Mitarbeiter konnte nicht zugewiesen werden:\n{error}",
            )

    def activate_selected_machine(self) -> None:
        """Aktiviert den ausgewählten Automaten."""
        selected = self._find_machine(self.selected_machine_id)
        if selected is None:
            QMessageBox.warning(self, "Kein Automat", "Bitte zuerst einen Automaten auswählen.")
            return

        if self.controller is None:
            QMessageBox.warning(self, "Fehler", "Kein Controller vorhanden.")
            return

        try:
            self.controller.activate_machine(selected.machine_id)
            self.refresh_data()
            QMessageBox.information(
                self,
                "Erfolg",
                f"Automat '{selected.machine_id}' wurde aktiviert.",
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Automat konnte nicht aktiviert werden:\n{error}",
            )

    def deactivate_selected_machine(self) -> None:
        """Deaktiviert den ausgewählten Automaten."""
        selected = self._find_machine(self.selected_machine_id)
        if selected is None:
            QMessageBox.warning(self, "Kein Automat", "Bitte zuerst einen Automaten auswählen.")
            return

        if self.controller is None:
            QMessageBox.warning(self, "Fehler", "Kein Controller vorhanden.")
            return

        try:
            self.controller.deactivate_machine(selected.machine_id)
            self.refresh_data()
            QMessageBox.information(
                self,
                "Erfolg",
                f"Automat '{selected.machine_id}' wurde deaktiviert.",
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Automat konnte nicht deaktiviert werden:\n{error}",
            )

    def delete_selected_machine(self) -> None:
        """Löscht den ausgewählten Automaten."""
        selected = self._find_machine(self.selected_machine_id)
        if selected is None:
            QMessageBox.warning(self, "Kein Automat", "Bitte zuerst einen Automaten auswählen.")
            return

        if self.controller is None:
            QMessageBox.warning(self, "Fehler", "Kein Controller vorhanden.")
            return

        answer = QMessageBox.question(
            self,
            "Automat löschen",
            (
                f"Möchtest du den Automaten '{selected.machine_id}' "
                f"am Standort '{selected.location}' wirklich löschen?"
            ),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            self.controller.delete_machine(selected.machine_id)
            self.selected_machine_id = None
            self.refresh_data()
            QMessageBox.information(
                self,
                "Erfolg",
                f"Automat '{selected.machine_id}' wurde gelöscht.",
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Automat konnte nicht gelöscht werden:\n{error}",
            )

    def open_table_dialog(self) -> None:
        """Öffnet die vergrößerte Tabellenansicht."""
        dialog = VendingTableDialog(self, self.filtered_machines)
        dialog.exec()
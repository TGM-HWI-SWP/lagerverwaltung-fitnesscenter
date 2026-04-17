from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from PyQt6.QtCore import Qt
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

from ui.widgets.stat_card import StatCard


@dataclass
class EmployeeRecord:
    employee_id: str
    full_name: str
    role: str
    department: str
    phone: str
    email: str
    status: str
    hire_date: str


class EmployeesTableDialog(QDialog):
    """Große Tabellenansicht für Mitarbeiter."""

    def __init__(self, parent: QWidget | None = None, employees: list[EmployeeRecord] | None = None) -> None:
        super().__init__(parent)
        self.employees = employees or []

        self.setWindowTitle("Mitarbeiterliste - vergrößerte Ansicht")
        self.setMinimumSize(1250, 720)
        self.resize(1380, 800)

        self._create_ui()
        self._populate_table()

    def _create_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Mitarbeiterliste")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Große Ansicht für eine bessere Übersicht.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["Mitarbeiter-ID", "Name", "Rolle", "Abteilung", "Telefon", "E-Mail", "Status", "Eintritt"]
        )
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
        self.table.setRowCount(len(self.employees))

        for row, employee in enumerate(self.employees):
            values = [
                employee.employee_id,
                employee.full_name,
                employee.role,
                employee.department,
                employee.phone,
                employee.email,
                employee.status,
                employee.hire_date,
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)


class EmployeesPage(QWidget):
    """Professionelle Mitarbeiter-Verwaltungsseite mit großer Tabellenansicht."""

    TABLE_COLUMNS = [
        "Mitarbeiter-ID",
        "Name",
        "Rolle",
        "Abteilung",
        "Telefon",
        "E-Mail",
        "Status",
        "Eintritt",
    ]

    def __init__(self, controller: Any | None = None) -> None:
        super().__init__()
        self.controller = controller
        self.employees: list[EmployeeRecord] = []
        self.filtered_employees: list[EmployeeRecord] = []

        self._create_ui()
        self._load_demo_data()
        self.refresh_data()

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

        self.total_card = StatCard(
            title="Gesamtmitarbeiter",
            value="0",
            subtitle="Alle erfassten Mitarbeiter",
            icon="🧑‍💼",
            accent="blue",
        )
        self.active_card = StatCard(
            title="Aktiv",
            value="0",
            subtitle="Derzeit aktiv im System",
            icon="✅",
            accent="green",
        )
        self.admin_card = StatCard(
            title="Administratoren",
            value="0",
            subtitle="Mitarbeiter mit Admin-Rolle",
            icon="🛡",
            accent="purple",
        )
        self.inactive_card = StatCard(
            title="Inaktiv",
            value="0",
            subtitle="Nicht derzeit im Einsatz",
            icon="⚠",
            accent="red",
        )

        stats_grid.addWidget(self.total_card, 0, 0)
        stats_grid.addWidget(self.active_card, 0, 1)
        stats_grid.addWidget(self.admin_card, 0, 2)
        stats_grid.addWidget(self.inactive_card, 0, 3)

        for col in range(4):
            stats_grid.setColumnStretch(col, 1)

        layout.addLayout(stats_grid)

    def _create_toolbar(self, layout: QVBoxLayout) -> None:
        toolbar_card = QFrame()
        toolbar_card.setObjectName("dashboardBottomCard")

        toolbar_layout = QVBoxLayout(toolbar_card)
        toolbar_layout.setContentsMargins(18, 18, 18, 18)
        toolbar_layout.setSpacing(14)

        title = QLabel("Mitarbeiterverwaltung")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Mitarbeiter suchen, filtern und verwalten.")
        subtitle.setObjectName("dashboardSectionSubtitle")

        control_row = QHBoxLayout()
        control_row.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Suche nach Name, E-Mail oder Mitarbeiter-ID ...")
        self.search_input.textChanged.connect(self.apply_filters)

        self.role_filter = QComboBox()
        self.role_filter.addItems(
            ["Alle Rollen", "Admin", "Trainer", "Empfang", "Lager", "Management"]
        )
        self.role_filter.currentTextChanged.connect(self.apply_filters)

        self.status_filter = QComboBox()
        self.status_filter.addItems(["Alle Status", "Aktiv", "Inaktiv", "Urlaub"])
        self.status_filter.currentTextChanged.connect(self.apply_filters)

        self.new_button = QPushButton("➕ Neuer Mitarbeiter")
        self.new_button.clicked.connect(self.create_employee)

        self.edit_button = QPushButton("✏ Bearbeiten")
        self.edit_button.setObjectName("secondaryButton")
        self.edit_button.clicked.connect(self.edit_employee)

        self.delete_button = QPushButton("🗑 Löschen")
        self.delete_button.setObjectName("secondaryButton")
        self.delete_button.clicked.connect(self.delete_employee)

        self.expand_button = QPushButton("🔍 Tabelle vergrößern")
        self.expand_button.setObjectName("secondaryButton")
        self.expand_button.clicked.connect(self.open_table_dialog)

        control_row.addWidget(self.search_input, 2)
        control_row.addWidget(self.role_filter, 1)
        control_row.addWidget(self.status_filter, 1)
        control_row.addWidget(self.new_button)
        control_row.addWidget(self.edit_button)
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

        title = QLabel("Mitarbeiterliste")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Alle passenden Mitarbeiter entsprechend deiner Suche und Filter.")
        subtitle.setObjectName("dashboardSectionSubtitle")

        self.employee_table = QTableWidget()
        self.employee_table.setColumnCount(len(self.TABLE_COLUMNS))
        self.employee_table.setHorizontalHeaderLabels(self.TABLE_COLUMNS)
        self.employee_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.employee_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.employee_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.employee_table.setAlternatingRowColors(True)
        self.employee_table.setSortingEnabled(True)
        self.employee_table.verticalHeader().setVisible(False)
        self.employee_table.horizontalHeader().setStretchLastSection(True)

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(self.employee_table)

        layout.addWidget(card)

    def _load_demo_data(self) -> None:
        self.employees = [
            EmployeeRecord("E-2001", "Markus Steiner", "Admin", "Verwaltung", "+43 660 111222", "markus.steiner@fit.at", "Aktiv", "12.01.2023"),
            EmployeeRecord("E-2002", "Laura Hofer", "Trainer", "Training", "+43 676 123999", "laura.hofer@fit.at", "Aktiv", "04.03.2024"),
            EmployeeRecord("E-2003", "Daniel Fuchs", "Empfang", "Service", "+43 664 555888", "daniel.fuchs@fit.at", "Aktiv", "17.05.2024"),
            EmployeeRecord("E-2004", "Nina Bauer", "Lager", "Logistik", "+43 699 212121", "nina.bauer@fit.at", "Inaktiv", "09.07.2023"),
            EmployeeRecord("E-2005", "Julian Kern", "Management", "Leitung", "+43 681 777444", "julian.kern@fit.at", "Aktiv", "01.11.2022"),
            EmployeeRecord("E-2006", "Sabrina Wolf", "Trainer", "Training", "+43 680 818181", "sabrina.wolf@fit.at", "Urlaub", "13.09.2024"),
            EmployeeRecord("E-2007", "Tobias Leitner", "Empfang", "Service", "+43 677 222666", "tobias.leitner@fit.at", "Aktiv", "22.10.2024"),
            EmployeeRecord("E-2008", "Vanessa Moser", "Lager", "Logistik", "+43 650 444333", "vanessa.moser@fit.at", "Aktiv", "15.12.2024"),
        ]

    def refresh_data(self) -> None:
        self.apply_filters()
        self.update_stats()

    def apply_filters(self) -> None:
        search_text = self.search_input.text().strip().lower()
        selected_role = self.role_filter.currentText()
        selected_status = self.status_filter.currentText()

        result: list[EmployeeRecord] = []

        for employee in self.employees:
            matches_search = (
                search_text in employee.full_name.lower()
                or search_text in employee.email.lower()
                or search_text in employee.employee_id.lower()
            )

            matches_role = (
                selected_role == "Alle Rollen" or employee.role == selected_role
            )

            matches_status = (
                selected_status == "Alle Status" or employee.status == selected_status
            )

            if matches_search and matches_role and matches_status:
                result.append(employee)

        self.filtered_employees = result
        self.populate_table()
        self.update_stats()

    def populate_table(self) -> None:
        self.employee_table.setSortingEnabled(False)
        self.employee_table.setRowCount(len(self.filtered_employees))

        for row, employee in enumerate(self.filtered_employees):
            values = [
                employee.employee_id,
                employee.full_name,
                employee.role,
                employee.department,
                employee.phone,
                employee.email,
                employee.status,
                employee.hire_date,
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.employee_table.setItem(row, col, item)

        self.employee_table.resizeColumnsToContents()
        self.employee_table.setSortingEnabled(True)

        if self.filtered_employees and self.employee_table.rowCount() > 0:
            self.employee_table.selectRow(0)

    def update_stats(self) -> None:
        total = len(self.filtered_employees)
        active = sum(1 for employee in self.filtered_employees if employee.status == "Aktiv")
        admins = sum(1 for employee in self.filtered_employees if employee.role == "Admin")
        inactive = sum(1 for employee in self.filtered_employees if employee.status == "Inaktiv")

        self.total_card.set_value_animated(total)
        self.active_card.set_value_animated(active)
        self.admin_card.set_value_animated(admins)
        self.inactive_card.set_value_animated(inactive)

    def _get_selected_employee(self) -> EmployeeRecord | None:
        row = self.employee_table.currentRow()
        if row < 0:
            return None

        id_item = self.employee_table.item(row, 0)
        if id_item is None:
            return None

        employee_id = id_item.text()
        for employee in self.filtered_employees:
            if employee.employee_id == employee_id:
                return employee

        return None

    def open_table_dialog(self) -> None:
        dialog = EmployeesTableDialog(self, self.filtered_employees)
        dialog.exec()

    def create_employee(self) -> None:
        QMessageBox.information(
            self,
            "Neuer Mitarbeiter",
            "Hier kann später ein Dialog zum Erstellen eines neuen Mitarbeiters geöffnet werden.",
        )

    def edit_employee(self) -> None:
        employee = self._get_selected_employee()
        if employee is None:
            QMessageBox.warning(self, "Bearbeiten", "Bitte zuerst einen Mitarbeiter auswählen.")
            return

        QMessageBox.information(
            self,
            "Mitarbeiter bearbeiten",
            f"Bearbeitungsdialog für {employee.full_name} kann hier später geöffnet werden.",
        )

    def delete_employee(self) -> None:
        employee = self._get_selected_employee()
        if employee is None:
            QMessageBox.warning(self, "Löschen", "Bitte zuerst einen Mitarbeiter auswählen.")
            return

        answer = QMessageBox.question(
            self,
            "Mitarbeiter löschen",
            f"Möchtest du {employee.full_name} wirklich löschen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer == QMessageBox.StandardButton.Yes:
            self.employees = [
                emp for emp in self.employees if emp.employee_id != employee.employee_id
            ]
            self.apply_filters()
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from PyQt6.QtCore import Qt
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
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.ui.widgets.stat_card import StatCard


@dataclass
class EmployeeRecord:
    """Speichert die aufbereiteten Daten eines Mitarbeiters."""

    employee_id: str
    full_name: str
    first_name: str
    last_name: str
    role: str
    department: str
    phone: str
    email: str
    status: str
    hire_date: str


class EmployeeDialog(QDialog):
    """Dialog zum Erstellen oder Bearbeiten eines Mitarbeiters."""

    ROLE_OPTIONS = ["Admin", "Trainer", "Empfang", "Lager", "Management", "Coach"]

    def __init__(self, parent: QWidget | None = None, employee: EmployeeRecord | None = None) -> None:
        """Initialisiert den Mitarbeiter-Dialog."""
        super().__init__(parent)

        self.employee = employee
        self.is_edit_mode = employee is not None

        self.setWindowTitle("Mitarbeiter bearbeiten" if self.is_edit_mode else "Neuer Mitarbeiter")
        self.setMinimumWidth(520)
        self.setModal(True)

        self._create_ui()
        self._fill_data_if_needed()

    def _create_ui(self) -> None:
        """Erstellt die Oberfläche des Dialogs."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Mitarbeiter bearbeiten" if self.is_edit_mode else "Neuen Mitarbeiter anlegen")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Mitarbeiterdaten erfassen und verwalten.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        form_card = QFrame()
        form_card.setObjectName("dashboardBottomCard")

        form = QFormLayout(form_card)
        form.setContentsMargins(18, 18, 18, 18)
        form.setSpacing(14)

        self.employee_id_input = QLineEdit()
        self.employee_id_input.setPlaceholderText("z. B. E-2001")

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Vorname")

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Nachname")

        self.role_input = QComboBox()
        self.role_input.addItems(self.ROLE_OPTIONS)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-Mail")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Telefon")

        form.addRow("Mitarbeiter-ID:", self.employee_id_input)
        form.addRow("Vorname:", self.first_name_input)
        form.addRow("Nachname:", self.last_name_input)
        form.addRow("Rolle:", self.role_input)
        form.addRow("E-Mail:", self.email_input)
        form.addRow("Telefon:", self.phone_input)

        button_row = QHBoxLayout()
        button_row.addStretch()

        cancel_button = QPushButton("Abbrechen")
        cancel_button.setObjectName("secondaryButton")
        cancel_button.clicked.connect(self.reject)

        save_button = QPushButton("Speichern")
        save_button.clicked.connect(self._validate_and_accept)

        button_row.addWidget(cancel_button)
        button_row.addWidget(save_button)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(form_card)
        layout.addLayout(button_row)

    def _fill_data_if_needed(self) -> None:
        """Füllt den Dialog im Bearbeitungsmodus mit vorhandenen Daten."""
        if self.employee is None:
            return

        self.employee_id_input.setText(self.employee.employee_id)
        self.employee_id_input.setReadOnly(True)
        self.first_name_input.setText(self.employee.first_name)
        self.last_name_input.setText(self.employee.last_name)
        self.email_input.setText(self.employee.email)
        self.phone_input.setText(self.employee.phone)

        index = self.role_input.findText(self.employee.role)
        if index >= 0:
            self.role_input.setCurrentIndex(index)

    def _validate_and_accept(self) -> None:
        """Prüft die Eingaben und bestätigt den Dialog."""
        employee_id = self.employee_id_input.text().strip()
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()

        if not employee_id:
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte eine Mitarbeiter-ID eingeben.")
            return

        if not first_name:
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte einen Vornamen eingeben.")
            return

        if not last_name:
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte einen Nachnamen eingeben.")
            return

        if not email:
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte eine E-Mail eingeben.")
            return

        if "@" not in email or "." not in email:
            QMessageBox.warning(self, "Ungültige E-Mail", "Bitte eine gültige E-Mail-Adresse eingeben.")
            return

        if not phone:
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte eine Telefonnummer eingeben.")
            return

        self.accept()

    def get_data(self) -> dict[str, str]:
        """Gibt die eingegebenen Mitarbeiterdaten zurück."""
        first_name = self.first_name_input.text().strip()
        last_name = self.last_name_input.text().strip()
        role = self.role_input.currentText()

        return {
            "employee_id": self.employee_id_input.text().strip(),
            "first_name": first_name,
            "last_name": last_name,
            "full_name": f"{first_name} {last_name}".strip(),
            "role": role,
            "department": role,
            "email": self.email_input.text().strip(),
            "phone": self.phone_input.text().strip(),
            "active": "true",
            "status": "Aktiv",
        }


class EmployeesTableDialog(QDialog):
    """Große Tabellenansicht für Mitarbeiter."""

    def __init__(self, parent: QWidget | None = None, employees: list[EmployeeRecord] | None = None) -> None:
        """Initialisiert den Tabellen-Dialog."""
        super().__init__(parent)

        self.employees = employees or []

        self.setWindowTitle("Mitarbeiterliste - vergrößerte Ansicht")
        self.setMinimumSize(1250, 720)
        self.resize(1380, 800)

        self._create_ui()
        self._populate_table()

    def _create_ui(self) -> None:
        """Erstellt die Oberfläche der großen Tabellenansicht."""
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
        """Füllt die Tabelle mit allen übergebenen Mitarbeitern."""
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
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)


class EmployeesPage(QWidget):
    """Seite zur Verwaltung von Mitarbeitern mit Filter-, Tabellen- und Dialogfunktionen."""

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
        """Initialisiert die Mitarbeiterseite."""
        super().__init__()

        self.controller = controller
        self.employees: list[EmployeeRecord] = []
        self.filtered_employees: list[EmployeeRecord] = []

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
        """Erstellt den Statistikbereich der Mitarbeiterseite."""
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
        """Erstellt Suchfeld, Filter und Aktionsbuttons."""
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
            ["Alle Rollen", "Admin", "Trainer", "Empfang", "Lager", "Management", "Coach"]
        )
        self.role_filter.currentTextChanged.connect(self.apply_filters)

        self.status_filter = QComboBox()
        self.status_filter.addItems(["Alle Status", "Aktiv", "Inaktiv"])
        self.status_filter.currentTextChanged.connect(self.apply_filters)

        self.new_button = QPushButton("➕ Neuer Mitarbeiter")
        self.new_button.clicked.connect(self.create_employee)

        self.edit_button = QPushButton("✏ Bearbeiten")
        self.edit_button.setObjectName("secondaryButton")
        self.edit_button.clicked.connect(self.edit_employee)

        self.delete_button = QPushButton("🗑 Deaktivieren")
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
        """Erstellt die Tabellenansicht der Mitarbeiter."""
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

    def _map_employee_to_record(self, employee: Any) -> EmployeeRecord:
        """Wandelt ein Controller-Objekt in ein EmployeeRecord um."""
        first_name = getattr(employee, "first_name", "") or ""
        last_name = getattr(employee, "last_name", "") or ""
        full_name = f"{first_name} {last_name}".strip()

        if not full_name:
            full_name = getattr(employee, "full_name", "") or getattr(employee, "name", "") or ""

        active = getattr(employee, "active", False)
        status = "Aktiv" if active else "Inaktiv"

        explicit_status = getattr(employee, "status", None)
        if explicit_status:
            status_text = str(explicit_status).strip().lower()
            if status_text in ("aktiv", "active", "1", "true"):
                status = "Aktiv"
            elif status_text in ("inaktiv", "inactive", "0", "false"):
                status = "Inaktiv"

        created_at = getattr(employee, "created_at", "") or getattr(employee, "hire_date", "")
        hire_date = str(created_at) if created_at else ""

        role = getattr(employee, "role", "") or ""
        department = getattr(employee, "department", "") or role

        return EmployeeRecord(
            employee_id=getattr(employee, "employee_id", "") or "",
            full_name=full_name,
            first_name=first_name,
            last_name=last_name,
            role=role,
            department=department,
            phone=getattr(employee, "phone", "") or "",
            email=getattr(employee, "email", "") or "",
            status=status,
            hire_date=hire_date,
        )

    def _call_controller_method(self, possible_names: list[str], *args: Any) -> Any:
        """Ruft die erste passende Methode des Controllers auf."""
        if self.controller is None:
            raise RuntimeError("Kein Controller vorhanden.")

        for method_name in possible_names:
            method = getattr(self.controller, method_name, None)
            if callable(method):
                return method(*args)

        raise AttributeError(
            f"Keine passende Controller-Methode gefunden. Erwartet eine von: {', '.join(possible_names)}"
        )

    def _employee_id_exists(self, employee_id: str, exclude_id: str | None = None) -> bool:
        """Prüft, ob eine Mitarbeiter-ID bereits existiert."""
        normalized_id = employee_id.strip().lower()
        excluded_id = exclude_id.strip().lower() if exclude_id else None

        for employee in self.employees:
            current_id = employee.employee_id.strip().lower()
            if current_id == normalized_id and current_id != excluded_id:
                return True

        return False

    def refresh_data(self) -> None:
        """Lädt Mitarbeiterdaten neu und aktualisiert die Ansicht."""
        try:
            if self.controller is not None:
                employees = self._call_controller_method(
                    ["get_all_employees", "list_employees", "fetch_employees"]
                )
                self.employees = [self._map_employee_to_record(employee) for employee in employees]
            else:
                self.employees = []

            self.apply_filters()
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Mitarbeiter konnten nicht geladen werden:\n{error}",
            )
            self.employees = []
            self.filtered_employees = []
            self.populate_table()
            self.update_stats()

    def apply_filters(self) -> None:
        """Filtert Mitarbeiter nach Suche, Rolle und Status."""
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

            matches_role = selected_role == "Alle Rollen" or employee.role == selected_role
            matches_status = selected_status == "Alle Status" or employee.status == selected_status

            if matches_search and matches_role and matches_status:
                result.append(employee)

        self.filtered_employees = result
        self.populate_table()
        self.update_stats()

    def populate_table(self) -> None:
        """Füllt die Tabelle mit den gefilterten Mitarbeitern."""
        self.employee_table.setSortingEnabled(False)
        self.employee_table.setRowCount(len(self.filtered_employees))
        self.employee_table.clearContents()

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
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.employee_table.setItem(row, col, item)

        self.employee_table.resizeColumnsToContents()
        self.employee_table.setSortingEnabled(True)

        if self.filtered_employees and self.employee_table.rowCount() > 0:
            self.employee_table.selectRow(0)

    def update_stats(self) -> None:
        """Aktualisiert die Kennzahlenkarten."""
        total_all = len(self.employees)
        active = sum(1 for employee in self.employees if employee.status == "Aktiv")
        admins = sum(1 for employee in self.employees if employee.role == "Admin")
        inactive = sum(1 for employee in self.employees if employee.status == "Inaktiv")

        self.total_card.set_value_animated(total_all)
        self.active_card.set_value_animated(active)
        self.admin_card.set_value_animated(admins)
        self.inactive_card.set_value_animated(inactive)

    def _get_selected_employee(self) -> EmployeeRecord | None:
        """Gibt den aktuell ausgewählten Mitarbeiter zurück."""
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
        """Öffnet die Tabelle in einer vergrößerten Ansicht."""
        dialog = EmployeesTableDialog(self, self.filtered_employees)
        dialog.exec()

    def create_employee(self) -> None:
        """Erstellt einen neuen Mitarbeiter."""
        dialog = EmployeeDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.get_data()

        if self._employee_id_exists(data["employee_id"]):
            QMessageBox.warning(
                self,
                "Doppelte Mitarbeiter-ID",
                f"Die Mitarbeiter-ID '{data['employee_id']}' existiert bereits.",
            )
            return

        try:
            self._call_controller_method(
                ["create_employee", "add_employee", "insert_employee"],
                data["employee_id"],
                data["first_name"],
                data["last_name"],
                data["role"],
                data["email"],
                data["phone"],
            )
            self.refresh_data()
            QMessageBox.information(
                self,
                "Erfolg",
                f"Mitarbeiter '{data['full_name']}' wurde erfolgreich angelegt.",
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Mitarbeiter konnte nicht erstellt werden:\n{error}",
            )

    def edit_employee(self) -> None:
        """Bearbeitet den ausgewählten Mitarbeiter."""
        employee = self._get_selected_employee()
        if employee is None:
            QMessageBox.warning(self, "Bearbeiten", "Bitte zuerst einen Mitarbeiter auswählen.")
            return

        dialog = EmployeeDialog(self, employee)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.get_data()

        if self._employee_id_exists(data["employee_id"], exclude_id=employee.employee_id):
            QMessageBox.warning(
                self,
                "Doppelte Mitarbeiter-ID",
                f"Die Mitarbeiter-ID '{data['employee_id']}' existiert bereits.",
            )
            return

        try:
            self._call_controller_method(
                ["update_employee", "edit_employee", "save_employee"],
                data["employee_id"],
                data["first_name"],
                data["last_name"],
                data["role"],
                data["email"],
                data["phone"],
            )
            self.refresh_data()
            QMessageBox.information(
                self,
                "Erfolg",
                f"Mitarbeiter '{data['full_name']}' wurde erfolgreich aktualisiert.",
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Mitarbeiter konnte nicht bearbeitet werden:\n{error}",
            )

    def delete_employee(self) -> None:
        """Deaktiviert den ausgewählten Mitarbeiter."""
        employee = self._get_selected_employee()
        if employee is None:
            QMessageBox.warning(self, "Löschen", "Bitte zuerst einen Mitarbeiter auswählen.")
            return

        answer = QMessageBox.question(
            self,
            "Mitarbeiter deaktivieren",
            f"Möchtest du {employee.full_name} wirklich deaktivieren?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            self._call_controller_method(
                ["deactivate_employee", "delete_employee", "remove_employee"],
                employee.employee_id,
            )
            self.refresh_data()
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Mitarbeiter konnte nicht deaktiviert werden:\n{error}",
            )
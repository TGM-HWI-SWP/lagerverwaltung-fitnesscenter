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
class MemberRecord:
    """Speichert die aufbereiteten Daten eines Mitglieds."""

    member_id: str
    full_name: str
    first_name: str
    last_name: str
    phone: str
    email: str
    plan: str
    status: str
    start_date: str


class MemberDialog(QDialog):
    """Dialog zum Erstellen oder Bearbeiten eines Mitglieds."""

    def __init__(self, parent: QWidget | None = None, member: MemberRecord | None = None) -> None:
        """Initialisiert den Mitgliederdialog."""
        super().__init__(parent)

        self.member = member
        self.is_edit_mode = member is not None

        self.setWindowTitle("Mitglied bearbeiten" if self.is_edit_mode else "Neues Mitglied")
        self.setMinimumWidth(520)
        self.setModal(True)

        self._create_ui()
        self._fill_data_if_needed()

    def _create_ui(self) -> None:
        """Erstellt die Oberfläche des Dialogs."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Mitglied bearbeiten" if self.is_edit_mode else "Neues Mitglied anlegen")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Mitgliedsdaten erfassen und verwalten.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        form_card = QFrame()
        form_card.setObjectName("dashboardBottomCard")

        form = QFormLayout(form_card)
        form.setContentsMargins(18, 18, 18, 18)
        form.setSpacing(14)

        self.member_id_input = QLineEdit()
        self.member_id_input.setPlaceholderText("z. B. M-1001")

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("Vorname")

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Nachname")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-Mail")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Telefon")

        self.plan_input = QComboBox()
        self.plan_input.addItems(["Standard", "Basic", "Premium", "Student", "VIP"])

        form.addRow("Mitgliedsnummer:", self.member_id_input)
        form.addRow("Vorname:", self.first_name_input)
        form.addRow("Nachname:", self.last_name_input)
        form.addRow("E-Mail:", self.email_input)
        form.addRow("Telefon:", self.phone_input)
        form.addRow("Tarif:", self.plan_input)

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

    def _fill_data_if_needed(self) -> None:
        """Füllt den Dialog im Bearbeitungsmodus mit vorhandenen Daten."""
        if self.member is None:
            return

        self.member_id_input.setText(self.member.member_id)
        self.member_id_input.setReadOnly(True)
        self.first_name_input.setText(self.member.first_name)
        self.last_name_input.setText(self.member.last_name)
        self.email_input.setText(self.member.email)
        self.phone_input.setText(self.member.phone)

        index = self.plan_input.findText(self.member.plan)
        if index >= 0:
            self.plan_input.setCurrentIndex(index)

    def _validate_and_accept(self) -> None:
        """Prüft die Eingaben und bestätigt den Dialog."""
        if not self.member_id_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte eine Mitgliedsnummer eingeben.")
            return

        if not self.first_name_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte einen Vornamen eingeben.")
            return

        if not self.last_name_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte einen Nachnamen eingeben.")
            return

        if not self.email_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte eine E-Mail eingeben.")
            return

        self.accept()

    def get_data(self) -> dict[str, str]:
        """Gibt die eingegebenen Mitgliedsdaten zurück."""
        return {
            "member_id": self.member_id_input.text().strip(),
            "first_name": self.first_name_input.text().strip(),
            "last_name": self.last_name_input.text().strip(),
            "email": self.email_input.text().strip(),
            "phone": self.phone_input.text().strip(),
            "membership_type": self.plan_input.currentText(),
        }


class MembersTableDialog(QDialog):
    """Große Tabellenansicht für Mitglieder."""

    def __init__(self, parent: QWidget | None = None, members: list[MemberRecord] | None = None) -> None:
        """Initialisiert den Tabellen-Dialog."""
        super().__init__(parent)

        self.members = members or []

        self.setWindowTitle("Mitgliederliste - vergrößerte Ansicht")
        self.setMinimumSize(1200, 700)
        self.resize(1350, 780)

        self._create_ui()
        self._populate_table()

    def _create_ui(self) -> None:
        """Erstellt die Oberfläche der großen Tabellenansicht."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Mitgliederliste")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Große Ansicht zur besseren Übersicht und zum bequemeren Lesen.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["Mitgliedsnummer", "Name", "Telefon", "E-Mail", "Tarif", "Status", "Startdatum"]
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
        """Füllt die Tabelle mit allen übergebenen Mitgliedern."""
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(self.members))
        self.table.clearContents()

        for row, member in enumerate(self.members):
            values = [
                member.member_id,
                member.full_name,
                member.phone,
                member.email,
                member.plan,
                member.status,
                member.start_date,
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)


class MembersPage(QWidget):
    """Seite zur Verwaltung von Mitgliedern mit Suche, Filtern und Tabellenansicht."""

    TABLE_COLUMNS = [
        "Mitgliedsnummer",
        "Name",
        "Telefon",
        "E-Mail",
        "Tarif",
        "Status",
        "Startdatum",
    ]

    def __init__(self, controller: Any | None = None) -> None:
        """Initialisiert die Mitgliederseite."""
        super().__init__()

        self.controller = controller
        self.members: list[MemberRecord] = []
        self.filtered_members: list[MemberRecord] = []

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
        """Erstellt den Statistikbereich der Mitgliederseite."""
        stats_grid = QGridLayout()
        stats_grid.setHorizontalSpacing(18)
        stats_grid.setVerticalSpacing(18)

        self.total_card = StatCard(
            title="Gesamtmitglieder",
            value="0",
            subtitle="Alle geladenen Mitglieder",
            icon="👥",
            accent="blue",
        )
        self.active_card = StatCard(
            title="Aktiv",
            value="0",
            subtitle="Derzeit aktive Mitglieder",
            icon="✅",
            accent="green",
        )
        self.paused_card = StatCard(
            title="Inaktiv",
            value="0",
            subtitle="Derzeit deaktivierte Mitglieder",
            icon="⏸",
            accent="orange",
        )
        self.expired_card = StatCard(
            title="Gefiltert",
            value="0",
            subtitle="Aktuell angezeigte Datensätze",
            icon="📋",
            accent="red",
        )

        stats_grid.addWidget(self.total_card, 0, 0)
        stats_grid.addWidget(self.active_card, 0, 1)
        stats_grid.addWidget(self.paused_card, 0, 2)
        stats_grid.addWidget(self.expired_card, 0, 3)

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

        title = QLabel("Mitgliederverwaltung")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Mitglieder durchsuchen, filtern und verwalten.")
        subtitle.setObjectName("dashboardSectionSubtitle")

        control_row = QHBoxLayout()
        control_row.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Suche nach Name, E-Mail oder Mitgliedsnummer ...")
        self.search_input.textChanged.connect(self.apply_filters)

        self.status_filter = QComboBox()
        self.status_filter.addItems(["Alle Status", "Aktiv", "Inaktiv"])
        self.status_filter.currentTextChanged.connect(self.apply_filters)

        self.plan_filter = QComboBox()
        self.plan_filter.addItems(["Alle Tarife", "Standard", "Basic", "Premium", "Student", "VIP"])
        self.plan_filter.currentTextChanged.connect(self.apply_filters)

        self.new_button = QPushButton("➕ Neues Mitglied")
        self.new_button.setObjectName("primaryButton")
        self.new_button.clicked.connect(self.create_member)

        self.edit_button = QPushButton("✏ Bearbeiten")
        self.edit_button.setObjectName("secondaryButton")
        self.edit_button.clicked.connect(self.edit_member)

        self.delete_button = QPushButton("🗑 Deaktivieren")
        self.delete_button.setObjectName("secondaryButton")
        self.delete_button.clicked.connect(self.delete_member)

        self.expand_button = QPushButton("🔍 Tabelle vergrößern")
        self.expand_button.setObjectName("secondaryButton")
        self.expand_button.clicked.connect(self.open_table_dialog)

        control_row.addWidget(self.search_input, 2)
        control_row.addWidget(self.status_filter, 1)
        control_row.addWidget(self.plan_filter, 1)
        control_row.addWidget(self.new_button)
        control_row.addWidget(self.edit_button)
        control_row.addWidget(self.delete_button)
        control_row.addWidget(self.expand_button)

        toolbar_layout.addWidget(title)
        toolbar_layout.addWidget(subtitle)
        toolbar_layout.addLayout(control_row)

        layout.addWidget(toolbar_card)

    def _create_table_section(self, layout: QVBoxLayout) -> None:
        """Erstellt die Tabellenansicht der Mitglieder."""
        card = QFrame()
        card.setObjectName("dashboardBottomCard")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(12)

        title = QLabel("Mitgliederliste")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Alle passenden Mitglieder entsprechend deiner Suche und Filter.")
        subtitle.setObjectName("dashboardSectionSubtitle")

        self.member_table = QTableWidget()
        self.member_table.setColumnCount(len(self.TABLE_COLUMNS))
        self.member_table.setHorizontalHeaderLabels(self.TABLE_COLUMNS)
        self.member_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.member_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.member_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.member_table.setAlternatingRowColors(True)
        self.member_table.setSortingEnabled(True)
        self.member_table.verticalHeader().setVisible(False)
        self.member_table.horizontalHeader().setStretchLastSection(True)

        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(self.member_table)

        layout.addWidget(card)

    def _map_member_to_record(self, member: Any) -> MemberRecord:
        """Wandelt ein Controller-Objekt in ein MemberRecord um."""
        first_name = getattr(member, "first_name", "") or ""
        last_name = getattr(member, "last_name", "") or ""
        full_name = f"{first_name} {last_name}".strip()

        member_id = getattr(member, "member_id", "") or ""
        phone = getattr(member, "phone", "") or ""
        email = getattr(member, "email", "") or ""
        plan = getattr(member, "membership_type", "") or ""

        active = getattr(member, "active", True)
        status = "Aktiv" if active else "Inaktiv"

        created_at = getattr(member, "created_at", "")
        start_date = str(created_at) if created_at else ""

        return MemberRecord(
            member_id=member_id,
            full_name=full_name,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            plan=plan,
            status=status,
            start_date=start_date,
        )

    def refresh_data(self) -> None:
        """Lädt Mitgliederdaten neu und aktualisiert die Ansicht."""
        try:
            if self.controller is not None:
                members = self.controller.get_all_members()
                self.members = [self._map_member_to_record(member) for member in members]
            else:
                self.members = []

            self.apply_filters()
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Mitglieder konnten nicht geladen werden:\n{error}",
            )
            self.members = []
            self.filtered_members = []
            self.populate_table()
            self.update_stats()

    def apply_filters(self) -> None:
        """Filtert Mitglieder nach Suche, Status und Tarif."""
        search_text = self.search_input.text().strip().lower()
        selected_status = self.status_filter.currentText()
        selected_plan = self.plan_filter.currentText()

        result: list[MemberRecord] = []

        for member in self.members:
            matches_search = (
                search_text in member.full_name.lower()
                or search_text in member.email.lower()
                or search_text in member.member_id.lower()
            )
            matches_status = selected_status == "Alle Status" or member.status == selected_status
            matches_plan = selected_plan == "Alle Tarife" or member.plan == selected_plan

            if matches_search and matches_status and matches_plan:
                result.append(member)

        self.filtered_members = result
        self.populate_table()
        self.update_stats()

    def populate_table(self) -> None:
        """Füllt die Tabelle mit den gefilterten Mitgliedern."""
        self.member_table.setSortingEnabled(False)
        self.member_table.setRowCount(len(self.filtered_members))
        self.member_table.clearContents()

        for row, member in enumerate(self.filtered_members):
            values = [
                member.member_id,
                member.full_name,
                member.phone,
                member.email,
                member.plan,
                member.status,
                member.start_date,
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.member_table.setItem(row, col, item)

        self.member_table.resizeColumnsToContents()
        self.member_table.setSortingEnabled(True)

        if self.filtered_members and self.member_table.rowCount() > 0:
            self.member_table.selectRow(0)

    def update_stats(self) -> None:
        """Aktualisiert die Kennzahlenkarten."""
        total_all = len(self.members)
        active = sum(1 for member in self.members if member.status == "Aktiv")
        inactive = sum(1 for member in self.members if member.status == "Inaktiv")
        filtered = len(self.filtered_members)

        self.total_card.set_value_animated(total_all)
        self.active_card.set_value_animated(active)
        self.paused_card.set_value_animated(inactive)
        self.expired_card.set_value_animated(filtered)

    def _get_selected_member(self) -> MemberRecord | None:
        """Gibt das aktuell ausgewählte Mitglied zurück."""
        row = self.member_table.currentRow()
        if row < 0:
            return None

        id_item = self.member_table.item(row, 0)
        if id_item is None:
            return None

        member_id = id_item.text()
        for member in self.filtered_members:
            if member.member_id == member_id:
                return member

        return None

    def open_table_dialog(self) -> None:
        """Öffnet die vergrößerte Tabellenansicht."""
        dialog = MembersTableDialog(self, self.filtered_members)
        dialog.exec()

    def create_member(self) -> None:
        """Erstellt ein neues Mitglied."""
        dialog = MemberDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.get_data()

        try:
            if self.controller is None:
                QMessageBox.warning(self, "Fehler", "Kein Controller vorhanden.")
                return

            self.controller.create_member(
                member_id=data["member_id"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                phone=data["phone"],
                membership_type=data["membership_type"],
            )
            self.refresh_data()
            QMessageBox.information(
                self,
                "Erfolg",
                f"Mitglied '{data['first_name']} {data['last_name']}' wurde erfolgreich erstellt.",
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Mitglied konnte nicht erstellt werden:\n{error}",
            )

    def edit_member(self) -> None:
        """Bearbeitet das ausgewählte Mitglied."""
        member = self._get_selected_member()
        if member is None:
            QMessageBox.warning(self, "Bearbeiten", "Bitte zuerst ein Mitglied auswählen.")
            return

        dialog = MemberDialog(self, member)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.get_data()

        try:
            if self.controller is None:
                QMessageBox.warning(self, "Fehler", "Kein Controller vorhanden.")
                return

            self.controller.update_member(
                member_id=member.member_id,
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                phone=data["phone"],
                membership_type=data["membership_type"],
            )
            self.refresh_data()
            QMessageBox.information(
                self,
                "Erfolg",
                f"Mitglied '{member.full_name}' wurde erfolgreich aktualisiert.",
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Mitglied konnte nicht aktualisiert werden:\n{error}",
            )

    def delete_member(self) -> None:
        """Deaktiviert das ausgewählte Mitglied."""
        member = self._get_selected_member()
        if member is None:
            QMessageBox.warning(self, "Deaktivieren", "Bitte zuerst ein Mitglied auswählen.")
            return

        answer = QMessageBox.question(
            self,
            "Mitglied deaktivieren",
            f"Möchtest du {member.full_name} wirklich deaktivieren?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            if self.controller is None:
                QMessageBox.warning(self, "Fehler", "Kein Controller vorhanden.")
                return

            self.controller.deactivate_member(member.member_id)
            self.refresh_data()
            QMessageBox.information(
                self,
                "Erfolg",
                f"Mitglied '{member.full_name}' wurde deaktiviert.",
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Mitglied konnte nicht deaktiviert werden:\n{error}",
            )
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

from src.ui.widgets.stat_card import StatCard


@dataclass
class MemberRecord:
    member_id: str
    full_name: str
    phone: str
    email: str
    plan: str
    status: str
    start_date: str


class MembersTableDialog(QDialog):
    """Große Tabellenansicht für Mitglieder."""

    def __init__(self, parent: QWidget | None = None, members: list[MemberRecord] | None = None) -> None:
        super().__init__(parent)
        self.members = members or []

        self.setWindowTitle("Mitgliederliste - vergrößerte Ansicht")
        self.setMinimumSize(1200, 700)
        self.resize(1350, 780)

        self._create_ui()
        self._populate_table()

    def _create_ui(self) -> None:
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
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(self.members))

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
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)


class MembersPage(QWidget):
    """Mitglieder-Verwaltungsseite mit Suche, Filtern und großer Tabellenansicht."""

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
        super().__init__()
        self.controller = controller
        self.members: list[MemberRecord] = []
        self.filtered_members: list[MemberRecord] = []

        self._create_ui()
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
            title="Gesamtmitglieder",
            value="0",
            subtitle="Alle registrierten Mitglieder",
            icon="👥",
            accent="blue",
        )
        self.active_card = StatCard(
            title="Aktiv",
            value="0",
            subtitle="Derzeit aktive Mitgliedschaften",
            icon="✅",
            accent="green",
        )
        self.paused_card = StatCard(
            title="Inaktiv",
            value="0",
            subtitle="Derzeit inaktive Mitgliedschaften",
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
        self.plan_filter.addItems(["Alle Tarife", "Basic", "Premium", "Student", "VIP"])
        self.plan_filter.currentTextChanged.connect(self.apply_filters)

        self.new_button = QPushButton("➕ Neues Mitglied")
        self.new_button.clicked.connect(self.create_member)

        self.edit_button = QPushButton("✏ Bearbeiten")
        self.edit_button.setObjectName("secondaryButton")
        self.edit_button.clicked.connect(self.edit_member)

        self.delete_button = QPushButton("🗑 Löschen")
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

    def _load_demo_data(self) -> None:
        self.members = [
            MemberRecord("M-1001", "Luca Gruber", "+43 660 123456", "luca.gruber@mail.com", "Premium", "Aktiv", "12.01.2024"),
            MemberRecord("M-1002", "Anna Weiss", "+43 676 555123", "anna.weiss@mail.com", "Basic", "Aktiv", "03.03.2024"),
            MemberRecord("M-1003", "David Huber", "+43 664 908172", "david.huber@mail.com", "Student", "Pausiert", "21.06.2024"),
            MemberRecord("M-1004", "Mia Berger", "+43 650 122334", "mia.berger@mail.com", "VIP", "Aktiv", "08.09.2023"),
            MemberRecord("M-1005", "Noah Leitner", "+43 681 777888", "noah.leitner@mail.com", "Premium", "Abgelaufen", "14.02.2023"),
            MemberRecord("M-1006", "Sophie Kern", "+43 699 333444", "sophie.kern@mail.com", "Basic", "Aktiv", "19.10.2024"),
            MemberRecord("M-1007", "Paul Moser", "+43 677 111222", "paul.moser@mail.com", "Student", "Pausiert", "27.11.2024"),
            MemberRecord("M-1008", "Emma Eder", "+43 680 444999", "emma.eder@mail.com", "Premium", "Aktiv", "05.12.2024"),
        ]
    
    def _map_member_to_record(self, member: Any) -> MemberRecord:
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
            phone=phone,
            email=email,
            plan=plan,
            status=status,
            start_date=start_date,
        )

    def refresh_data(self) -> None:
        self.apply_filters()
        self.update_stats()

    def apply_filters(self) -> None:
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

            matches_status = (
                selected_status == "Alle Status" or member.status == selected_status
            )

            matches_plan = (
                selected_plan == "Alle Tarife" or member.plan == selected_plan
            )

            if matches_search and matches_status and matches_plan:
                result.append(member)

        self.filtered_members = result
        self.populate_table()
        self.update_stats()

    def populate_table(self) -> None:
        self.member_table.setSortingEnabled(False)
        self.member_table.setRowCount(len(self.filtered_members))

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
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                self.member_table.setItem(row, col, item)

        self.member_table.resizeColumnsToContents()
        self.member_table.setSortingEnabled(True)

        if self.filtered_members and self.member_table.rowCount() > 0:
            self.member_table.selectRow(0)

    def update_stats(self) -> None:
        total = len(self.filtered_members)
        active = sum(1 for member in self.filtered_members if member.status == "Aktiv")
        paused = sum(1 for member in self.filtered_members if member.status == "Pausiert")
        expired = sum(1 for member in self.filtered_members if member.status == "Abgelaufen")

        self.total_card.set_value_animated(total)
        self.active_card.set_value_animated(active)
        self.paused_card.set_value_animated(paused)
        self.expired_card.set_value_animated(expired)

    def _get_selected_member(self) -> MemberRecord | None:
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
        dialog = MembersTableDialog(self, self.filtered_members)
        dialog.exec()

    def create_member(self) -> None:
        QMessageBox.information(
            self,
            "Neues Mitglied",
            "Hier kann später ein Dialog zum Erstellen eines neuen Mitglieds geöffnet werden.",
        )

    def edit_member(self) -> None:
        member = self._get_selected_member()
        if member is None:
            QMessageBox.warning(self, "Bearbeiten", "Bitte zuerst ein Mitglied auswählen.")
            return

        QMessageBox.information(
            self,
            "Mitglied bearbeiten",
            f"Bearbeitungsdialog für {member.full_name} kann hier später geöffnet werden.",
        )

    def delete_member(self) -> None:
        member = self._get_selected_member()
        if member is None:
            QMessageBox.warning(self, "Löschen", "Bitte zuerst ein Mitglied auswählen.")
            return

        answer = QMessageBox.question(
            self,
            "Mitglied löschen",
            f"Möchtest du {member.full_name} wirklich löschen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer == QMessageBox.StandardButton.Yes:
            self.members = [m for m in self.members if m.member_id != member.member_id]
            self.apply_filters()
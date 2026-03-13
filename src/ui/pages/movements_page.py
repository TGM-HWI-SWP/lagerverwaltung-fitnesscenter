from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class MovementsPage(QWidget):
    """Seite für Lagerbewegungen."""

    def __init__(self) -> None:
        super().__init__()
        self._create_ui()
        self._load_demo_data()

    def _create_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)

        action_card = QFrame()
        action_card.setObjectName("toolbarCard")

        action_layout = QHBoxLayout(action_card)
        action_layout.setContentsMargins(18, 18, 18, 18)
        action_layout.setSpacing(12)

        self.in_button = QPushButton("Wareneingang")
        self.in_button.setObjectName("primaryButton")

        self.out_button = QPushButton("Warenausgang")
        self.out_button.setObjectName("secondaryButton")

        self.inventory_button = QPushButton("Inventurkorrektur")
        self.inventory_button.setObjectName("secondaryButton")

        action_layout.addWidget(self.in_button)
        action_layout.addWidget(self.out_button)
        action_layout.addWidget(self.inventory_button)
        action_layout.addStretch()

        table_card = QFrame()
        table_card.setObjectName("tableCard")

        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(18, 18, 18, 18)
        table_layout.setSpacing(12)

        title = QLabel("Letzte Lagerbewegungen")
        title.setObjectName("sectionTitle")

        self.movements_table = QTableWidget()
        self.movements_table.setColumnCount(5)
        self.movements_table.setHorizontalHeaderLabels(
            [
                "Zeitpunkt",
                "Artikel",
                "Typ",
                "Menge",
                "Grund",
            ]
        )
        self.movements_table.verticalHeader().setVisible(False)
        self.movements_table.setAlternatingRowColors(True)
        self.movements_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.movements_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.movements_table.horizontalHeader().setStretchLastSection(True)

        table_layout.addWidget(title)
        table_layout.addWidget(self.movements_table)

        main_layout.addWidget(action_card)
        main_layout.addWidget(table_card)

    def _load_demo_data(self) -> None:
        demo_data = [
            ["13.03.2026 08:15", "Protein Powder Vanilla", "Eingang", "+20", "Lieferung"],
            ["13.03.2026 09:10", "Gym Towel Black", "Ausgang", "-5", "Shopverkauf"],
            ["13.03.2026 09:45", "Disinfectant Spray", "Ausgang", "-2", "Reinigung"],
            ["13.03.2026 10:30", "Isotonic Drink", "Eingang", "+30", "Nachlieferung"],
            ["13.03.2026 11:20", "Resistance Bands Set", "Korrektur", "+1", "Inventur"],
        ]

        self.movements_table.setRowCount(len(demo_data))

        for row, item in enumerate(demo_data):
            for col, value in enumerate(item):
                self.movements_table.setItem(row, col, QTableWidgetItem(value))
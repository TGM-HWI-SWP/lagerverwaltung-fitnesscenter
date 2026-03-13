from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui.tables.inventory_table import InventoryTable


class InventoryPage(QWidget):
    """Seite für den Lagerbestand."""

    def __init__(self, controller=None) -> None:
        super().__init__()
        self.controller = controller
        self._create_ui()
        self._load_initial_data()

    def _create_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)

        top_bar = self._create_top_bar()
        table_card = self._create_table_card()

        main_layout.addWidget(top_bar)
        main_layout.addWidget(table_card)

    def _create_top_bar(self) -> QWidget:
        widget = QFrame()
        widget.setObjectName("toolbarCard")

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Artikel suchen ...")

        self.category_filter = QComboBox()
        self.category_filter.addItems(
            [
                "Alle Kategorien",
                "Supplements",
                "Getränke",
                "Merchandise",
                "Hygiene",
                "Geräte-Zubehör",
            ]
        )

        self.status_filter = QComboBox()
        self.status_filter.addItems(["Alle Status", "OK", "Kritisch", "Leer"])

        self.add_button = QPushButton("Artikel hinzufügen")
        self.add_button.setObjectName("primaryButton")

        layout.addWidget(self.search_input, 1)
        layout.addWidget(self.category_filter)
        layout.addWidget(self.status_filter)
        layout.addWidget(self.add_button)

        return widget

    def _create_table_card(self) -> QWidget:
        card = QFrame()
        card.setObjectName("tableCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Lagerbestand")
        title.setObjectName("sectionTitle")

        self.inventory_table = InventoryTable()

        layout.addWidget(title)
        layout.addWidget(self.inventory_table)

        return card

    def _load_initial_data(self) -> None:
        """
        Lädt beim Start Daten.
        Später hier Controller-Anbindung einbauen.
        """
        if self.controller is not None:
            try:
                items = self.controller.get_all_inventory_items()
                self.inventory_table.load_data(items)
                return
            except Exception:
                pass

        self.inventory_table.load_demo_data()
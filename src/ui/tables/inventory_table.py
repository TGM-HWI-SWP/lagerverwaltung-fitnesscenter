from typing import Iterable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem


class InventoryTable(QTableWidget):
    """Spezialisierte Tabelle zur Anzeige des Lagerbestands."""

    COLUMN_HEADERS = [
        "Artikel-Nr.",
        "Name",
        "Kategorie",
        "Bestand",
        "Mindestbestand",
        "Lagerort",
        "Status",
    ]

    def __init__(self) -> None:
        super().__init__()
        self._setup_table()

    def _setup_table(self) -> None:
        """Grundkonfiguration der Tabelle."""
        self.setObjectName("inventoryTable")
        self.setColumnCount(len(self.COLUMN_HEADERS))
        self.setHorizontalHeaderLabels(self.COLUMN_HEADERS)

        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSortingEnabled(True)

        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)

        self.setColumnWidth(0, 110)
        self.setColumnWidth(1, 240)
        self.setColumnWidth(2, 150)
        self.setColumnWidth(3, 90)
        self.setColumnWidth(4, 130)
        self.setColumnWidth(5, 140)
        self.setColumnWidth(6, 110)

    def load_data(self, items: Iterable[dict]) -> None:
        """
        Lädt Daten in die Tabelle.

        Erwartet pro Element ein Dictionary, z. B.:
        {
            "article_no": "FG001",
            "name": "Protein Powder Vanilla",
            "category": "Supplements",
            "stock": 42,
            "min_stock": 15,
            "location": "Regal A1"
        }
        """
        items = list(items)
        self.setSortingEnabled(False)
        self.setRowCount(len(items))

        for row, item in enumerate(items):
            article_no = str(item.get("article_no", ""))
            name = str(item.get("name", ""))
            category = str(item.get("category", ""))
            stock = int(item.get("stock", 0))
            min_stock = int(item.get("min_stock", 0))
            location = str(item.get("location", ""))

            status = self._get_status(stock, min_stock)

            values = [
                article_no,
                name,
                category,
                str(stock),
                str(min_stock),
                location,
                status,
            ]

            for column, value in enumerate(values):
                table_item = QTableWidgetItem(value)

                if column in (3, 4, 6):
                    table_item.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                        | Qt.AlignmentFlag.AlignVCenter
                    )

                self.setItem(row, column, table_item)

            self._apply_row_style(row, status)

        self.setSortingEnabled(True)

    def load_demo_data(self) -> None:
        """Lädt Demo-Daten für den ersten Start."""
        demo_items = [
            {
                "article_no": "FG001",
                "name": "Protein Powder Vanilla",
                "category": "Supplements",
                "stock": 42,
                "min_stock": 15,
                "location": "Regal A1",
            },
            {
                "article_no": "FG002",
                "name": "Pre-Workout Booster",
                "category": "Supplements",
                "stock": 8,
                "min_stock": 10,
                "location": "Regal A2",
            },
            {
                "article_no": "FG003",
                "name": "Gym Towel Black",
                "category": "Merchandise",
                "stock": 25,
                "min_stock": 10,
                "location": "Shop B1",
            },
            {
                "article_no": "FG004",
                "name": "Isotonic Drink",
                "category": "Getränke",
                "stock": 0,
                "min_stock": 12,
                "location": "Kühlregal C1",
            },
            {
                "article_no": "FG005",
                "name": "Disinfectant Spray",
                "category": "Hygiene",
                "stock": 6,
                "min_stock": 8,
                "location": "Lager D2",
            },
            {
                "article_no": "FG006",
                "name": "Resistance Bands Set",
                "category": "Geräte-Zubehör",
                "stock": 14,
                "min_stock": 5,
                "location": "Regal E1",
            },
        ]

        self.load_data(demo_items)

    def get_selected_article_no(self) -> str | None:
        """Gibt die Artikelnummer der ausgewählten Zeile zurück."""
        current_row = self.currentRow()
        if current_row < 0:
            return None

        item = self.item(current_row, 0)
        if item is None:
            return None

        return item.text()

    @staticmethod
    def _get_status(stock: int, min_stock: int) -> str:
        """Ermittelt den Status eines Artikels."""
        if stock <= 0:
            return "Leer"
        if stock <= min_stock:
            return "Kritisch"
        return "OK"

    def _apply_row_style(self, row: int, status: str) -> None:
        """Färbt Status und wichtige Werte passend ein."""
        stock_item = self.item(row, 3)
        min_stock_item = self.item(row, 4)
        status_item = self.item(row, 6)

        if stock_item is None or min_stock_item is None or status_item is None:
            return

        if status == "OK":
            color = QColor("#22C55E")
        elif status == "Kritisch":
            color = QColor("#F59E0B")
        else:
            color = QColor("#EF4444")

        stock_item.setForeground(QBrush(color))
        min_stock_item.setForeground(QBrush(QColor("#CBD5E1")))
        status_item.setForeground(QBrush(color))
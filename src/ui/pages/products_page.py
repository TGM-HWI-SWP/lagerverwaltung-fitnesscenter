from __future__ import annotations

from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class ProductDialog(QDialog):
    """Dialog zum Hinzufügen oder Bearbeiten eines Produkts."""

    def __init__(self, parent=None, product_data: dict[str, Any] | None = None) -> None:
        super().__init__(parent)
        self.product_data = product_data
        self.is_edit_mode = product_data is not None

        self.setWindowTitle(
            "Produkt bearbeiten" if self.is_edit_mode else "Produkt hinzufügen"
        )
        self.setModal(True)
        self.setMinimumWidth(520)
        self.setObjectName("productDialog")

        self._create_ui()
        self._fill_data_if_needed()

    def _create_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(18)

        title = QLabel(
            "Produkt bearbeiten" if self.is_edit_mode else "Neues Produkt anlegen"
        )
        title.setObjectName("dialogTitle")

        subtitle = QLabel(
            "Produktdaten, Lagerbestand und weitere Informationen verwalten."
        )
        subtitle.setObjectName("dialogSubtitle")
        subtitle.setWordWrap(True)

        form_card = QFrame()
        form_card.setObjectName("dialogFormCard")

        form_layout = QFormLayout(form_card)
        form_layout.setContentsMargins(18, 18, 18, 18)
        form_layout.setSpacing(14)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("z. B. PROD-001")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("z. B. Whey Protein Chocolate")

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Kurze Beschreibung")

        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0.0, 999999.99)
        self.price_input.setDecimals(2)
        self.price_input.setSuffix(" €")

        self.quantity_input = QSpinBox()
        self.quantity_input.setRange(0, 100000)

        self.sku_input = QLineEdit()
        self.sku_input.setPlaceholderText("z. B. SKU-4451")

        self.category_input = QComboBox()
        self.category_input.addItems(
            [
                "Supplements",
                "Getränke",
                "Merchandise",
                "Snacks",
                "Hygiene",
                "Sonstiges",
            ]
        )

        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Zusätzliche Notizen")

        form_layout.addRow("Produkt-ID:", self.id_input)
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Beschreibung:", self.description_input)
        form_layout.addRow("Preis:", self.price_input)
        form_layout.addRow("Bestand:", self.quantity_input)
        form_layout.addRow("SKU:", self.sku_input)
        form_layout.addRow("Kategorie:", self.category_input)
        form_layout.addRow("Notizen:", self.notes_input)

        button_row = QHBoxLayout()
        button_row.addStretch()

        cancel_button = QPushButton("Abbrechen")
        cancel_button.setObjectName("secondaryButton")
        cancel_button.clicked.connect(self.reject)

        save_button = QPushButton(
            "Speichern" if not self.is_edit_mode else "Änderungen speichern"
        )
        save_button.setObjectName("primaryButton")
        save_button.clicked.connect(self._validate_and_accept)

        button_row.addWidget(cancel_button)
        button_row.addWidget(save_button)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(form_card)
        main_layout.addLayout(button_row)

    def _fill_data_if_needed(self) -> None:
        if not self.product_data:
            return

        self.id_input.setText(str(self.product_data.get("id", "")))
        self.name_input.setText(str(self.product_data.get("name", "")))
        self.description_input.setText(str(self.product_data.get("description", "")))
        self.price_input.setValue(float(self.product_data.get("price", 0.0)))
        self.quantity_input.setValue(int(self.product_data.get("quantity", 0)))
        self.sku_input.setText(str(self.product_data.get("sku", "")))
        self.notes_input.setText(str(self.product_data.get("notes", "")))

        category = str(self.product_data.get("category", "Sonstiges"))
        index = self.category_input.findText(category)
        if index >= 0:
            self.category_input.setCurrentIndex(index)

        if self.is_edit_mode:
            self.id_input.setReadOnly(True)

    def _validate_and_accept(self) -> None:
        if not self.id_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte eine Produkt-ID angeben.")
            self.id_input.setFocus()
            return

        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte einen Produktnamen angeben.")
            self.name_input.setFocus()
            return

        self.accept()

    def get_data(self) -> dict[str, Any]:
        return {
            "id": self.id_input.text().strip(),
            "name": self.name_input.text().strip(),
            "description": self.description_input.text().strip(),
            "price": self.price_input.value(),
            "quantity": self.quantity_input.value(),
            "sku": self.sku_input.text().strip(),
            "category": self.category_input.currentText(),
            "notes": self.notes_input.text().strip(),
        }


class StockDialog(QDialog):
    """Dialog zur schnellen Bestandsänderung eines Produkts."""

    def __init__(
        self,
        parent=None,
        product_id: str = "",
        product_name: str = "",
        current_quantity: int = 0,
    ) -> None:
        super().__init__(parent)

        self.product_id = product_id
        self.product_name = product_name
        self.current_quantity = current_quantity

        self.setWindowTitle("Bestand ändern")
        self.setModal(True)
        self.setMinimumWidth(460)

        self._create_ui()

    def _create_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(18)

        info = QLabel(
            f"Produkt: {self.product_name} ({self.product_id})\n"
            f"Aktueller Bestand: {self.current_quantity}"
        )
        info.setObjectName("dialogSubtitle")
        info.setWordWrap(True)

        form_card = QFrame()
        form_card.setObjectName("dialogFormCard")

        form_layout = QFormLayout(form_card)
        form_layout.setContentsMargins(18, 18, 18, 18)
        form_layout.setSpacing(14)

        self.mode_input = QComboBox()
        self.mode_input.addItems(["Wareneingang", "Warenausgang"])

        self.amount_input = QSpinBox()
        self.amount_input.setRange(1, 100000)
        self.amount_input.setValue(1)

        self.reason_input = QLineEdit()
        self.reason_input.setPlaceholderText("z. B. Lieferung, Verkauf, Korrektur")

        form_layout.addRow("Aktion:", self.mode_input)
        form_layout.addRow("Menge:", self.amount_input)
        form_layout.addRow("Grund:", self.reason_input)

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

        main_layout.addWidget(info)
        main_layout.addWidget(form_card)
        main_layout.addLayout(button_row)

    def _validate_and_accept(self) -> None:
        if not self.reason_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte einen Grund angeben.")
            self.reason_input.setFocus()
            return

        if self.mode_input.currentText() == "Warenausgang":
            if self.amount_input.value() > self.current_quantity:
                QMessageBox.warning(
                    self,
                    "Ungültiger Bestand",
                    "Es können nicht mehr Produkte entfernt werden als vorhanden sind.",
                )
                return

        self.accept()

    def get_data(self) -> dict[str, Any]:
        mode = self.mode_input.currentText()
        amount = self.amount_input.value()
        signed_amount = amount if mode == "Wareneingang" else -amount

        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "current_quantity": self.current_quantity,
            "mode": mode,
            "amount": amount,
            "signed_amount": signed_amount,
            "reason": self.reason_input.text().strip(),
            "new_quantity": self.current_quantity + signed_amount,
        }


class ProductsPage(QWidget):
    """Seite zur Verwaltung aller Produkte."""

    TABLE_COLUMNS = [
        "ID",
        "Name",
        "Beschreibung",
        "Preis",
        "Bestand",
        "SKU",
        "Kategorie",
        "Notizen",
    ]

    def __init__(self, controller=None) -> None:
        super().__init__()
        self.controller = controller
        self._all_products: list[dict[str, Any]] = []

        self._create_ui()
        self.refresh_data()

    def _create_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(18)

        main_layout.addWidget(self._create_top_bar())
        main_layout.addWidget(self._create_stats_row())
        main_layout.addWidget(self._create_table_card(), 1)

    def _create_top_bar(self) -> QWidget:
        card = QFrame()
        card.setObjectName("toolbarCard")

        layout = QHBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Produkte suchen ...")
        self.search_input.textChanged.connect(self._apply_filters)

        self.category_filter = QComboBox()
        self.category_filter.addItem("Alle Kategorien")
        self.category_filter.addItems(
            ["Supplements", "Getränke", "Merchandise", "Snacks", "Hygiene", "Sonstiges"]
        )
        self.category_filter.currentTextChanged.connect(self._apply_filters)

        self.stock_filter = QComboBox()
        self.stock_filter.addItems(
            ["Alle Bestände", "Nur kritisch", "Nur leer", "Nur verfügbar"]
        )
        self.stock_filter.currentTextChanged.connect(self._apply_filters)

        self.add_button = QPushButton("Produkt hinzufügen")
        self.add_button.setObjectName("primaryButton")
        self.add_button.clicked.connect(self._open_add_dialog)

        self.edit_button = QPushButton("Bearbeiten")
        self.edit_button.setObjectName("secondaryButton")
        self.edit_button.clicked.connect(self._open_edit_dialog)

        self.stock_button = QPushButton("Bestand ändern")
        self.stock_button.setObjectName("secondaryButton")
        self.stock_button.clicked.connect(self._open_stock_dialog)

        layout.addWidget(self.search_input, 1)
        layout.addWidget(self.category_filter)
        layout.addWidget(self.stock_filter)
        layout.addWidget(self.add_button)
        layout.addWidget(self.edit_button)
        layout.addWidget(self.stock_button)

        return card

    def _create_stats_row(self) -> QWidget:
        wrapper = QWidget()
        layout = QGridLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)

        self.total_products_card = self._create_stat_card("Produkte gesamt", "0")
        self.total_stock_card = self._create_stat_card("Gesamtbestand", "0")
        self.low_stock_card = self._create_stat_card("Kritische Produkte", "0")
        self.value_card = self._create_stat_card("Lagerwert", "0.00 €")

        layout.addWidget(self.total_products_card, 0, 0)
        layout.addWidget(self.total_stock_card, 0, 1)
        layout.addWidget(self.low_stock_card, 0, 2)
        layout.addWidget(self.value_card, 0, 3)

        return wrapper

    def _create_stat_card(self, title: str, value: str) -> QFrame:
        card = QFrame()
        card.setObjectName("statCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setObjectName("statTitle")

        value_label = QLabel(value)
        value_label.setObjectName("statValue")

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        card.value_label = value_label
        return card

    def _create_table_card(self) -> QWidget:
        card = QFrame()
        card.setObjectName("tableCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Produktübersicht")
        title.setObjectName("sectionTitle")

        self.products_table = QTableWidget()
        self.products_table.setObjectName("productsTable")
        self.products_table.setColumnCount(len(self.TABLE_COLUMNS))
        self.products_table.setHorizontalHeaderLabels(self.TABLE_COLUMNS)
        self.products_table.verticalHeader().setVisible(False)
        self.products_table.setAlternatingRowColors(True)
        self.products_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.products_table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )
        self.products_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.products_table.horizontalHeader().setStretchLastSection(True)

        layout.addWidget(title)
        layout.addWidget(self.products_table)

        return card

    def refresh_data(self) -> None:
        """Lädt Daten neu. Erst Demo, später Controller."""
        if self.controller is not None:
            try:
                products = self.controller.get_all_products()
                self._all_products = list(products)
                self._apply_filters()
                return
            except Exception:
                pass

        self._all_products = self._get_demo_products()
        self._apply_filters()

    def _get_demo_products(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "PROD-001",
                "name": "Whey Protein Vanilla",
                "description": "Proteinpulver 1kg",
                "price": 34.90,
                "quantity": 28,
                "sku": "WP-1001",
                "category": "Supplements",
                "notes": "Bestseller",
            },
            {
                "id": "PROD-002",
                "name": "Pre-Workout Booster",
                "description": "Energie vor dem Training",
                "price": 24.50,
                "quantity": 7,
                "sku": "PWB-210",
                "category": "Supplements",
                "notes": "Niedriger Bestand",
            },
            {
                "id": "PROD-003",
                "name": "Isotonic Drink",
                "description": "0,5L Getränk",
                "price": 2.99,
                "quantity": 0,
                "sku": "ISO-500",
                "category": "Getränke",
                "notes": "Leer",
            },
            {
                "id": "PROD-004",
                "name": "Gym Towel",
                "description": "Handtuch schwarz",
                "price": 12.00,
                "quantity": 18,
                "sku": "GT-001",
                "category": "Merchandise",
                "notes": "",
            },
            {
                "id": "PROD-005",
                "name": "Protein Bar",
                "description": "Snack Riegel",
                "price": 2.49,
                "quantity": 54,
                "sku": "PB-890",
                "category": "Snacks",
                "notes": "",
            },
        ]

    def _apply_filters(self) -> None:
        search_text = self.search_input.text().strip().lower()
        category = self.category_filter.currentText()
        stock_mode = self.stock_filter.currentText()

        filtered_products: list[dict[str, Any]] = []

        for product in self._all_products:
            product_text = " ".join(
                [
                    str(product.get("id", "")),
                    str(product.get("name", "")),
                    str(product.get("description", "")),
                    str(product.get("sku", "")),
                    str(product.get("category", "")),
                ]
            ).lower()

            # --- Suche ---
            if search_text and search_text not in product_text:
                continue

            # --- Kategorie Filter ---
            if category != "Alle Kategorien":
                if product.get("category") != category:
                    continue

            # --- Bestand Filter ---
            quantity = int(product.get("quantity", 0))

            if stock_mode == "Nur kritisch" and quantity > 10:
                continue
            if stock_mode == "Nur leer" and quantity != 0:
                continue
            if stock_mode == "Nur verfügbar" and quantity <= 0:
                continue

            filtered_products.append(product)

        self._populate_table(filtered_products)
        self._update_stats(filtered_products)


    def _populate_table(self, products: list[dict[str, Any]]) -> None:
        self.products_table.setRowCount(len(products))

        for row, product in enumerate(products):
            values = [
                product.get("id"),
                product.get("name"),
                product.get("description"),
                f"{product.get('price', 0):.2f} €",
                product.get("quantity"),
                product.get("sku"),
                product.get("category"),
                product.get("notes"),
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))

                if col == 4:
                    quantity = int(product.get("quantity", 0))
                    if quantity == 0:
                        item.setBackground(QColor("#ff4d4d"))
                    elif quantity < 10:
                        item.setBackground(QColor("#ffcc00"))

                self.products_table.setItem(row, col, item)


    def _update_stats(self, products: list[dict[str, Any]]) -> None:
        total_products = len(products)
        total_stock = sum(int(p.get("quantity", 0)) for p in products)
        low_stock = sum(1 for p in products if int(p.get("quantity", 0)) < 10)
        total_value = sum(
            float(p.get("price", 0)) * int(p.get("quantity", 0)) for p in products
        )

        self.total_products_card.value_label.setText(str(total_products))
        self.total_stock_card.value_label.setText(str(total_stock))
        self.low_stock_card.value_label.setText(str(low_stock))
        self.value_card.value_label.setText(f"{total_value:.2f} €")


    def _get_selected_product(self) -> dict[str, Any] | None:
        row = self.products_table.currentRow()
        if row < 0:
            return None
        return self._all_products[row]


    def _open_add_dialog(self) -> None:
        dialog = ProductDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            self._all_products.append(data)
            self._apply_filters()


    def _open_edit_dialog(self) -> None:
        product = self._get_selected_product()
        if not product:
            QMessageBox.warning(self, "Fehler", "Bitte ein Produkt auswählen.")
            return

        dialog = ProductDialog(self, product)
        if dialog.exec():
            updated = dialog.get_data()
            index = self._all_products.index(product)
            self._all_products[index] = updated
            self._apply_filters()


    def _open_stock_dialog(self) -> None:
        product = self._get_selected_product()
        if not product:
            QMessageBox.warning(self, "Fehler", "Bitte ein Produkt auswählen.")
            return

        dialog = StockDialog(
            self,
            product_id=product["id"],
            product_name=product["name"],
            current_quantity=product["quantity"],
        )

        if dialog.exec():
            result = dialog.get_data()
            product["quantity"] = result["new_quantity"]
            self._apply_filters()
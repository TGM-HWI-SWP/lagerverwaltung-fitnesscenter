from __future__ import annotations

from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QAbstractItemView,
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

from ui.widgets.stat_card import StatCard


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


class ProductsTableDialog(QDialog):
    """Große Tabellenansicht für Produkte."""

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

    def __init__(self, parent: QWidget | None = None, products: list[dict[str, Any]] | None = None) -> None:
        super().__init__(parent)
        self.products = products or []

        self.setWindowTitle("Produktübersicht - vergrößerte Ansicht")
        self.setMinimumSize(1300, 760)
        self.resize(1450, 820)

        self._create_ui()
        self._populate_table()

    def _create_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Produktübersicht")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Große Tabellenansicht zur besseren Betrachtung.")
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
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(self.products))

        for row, product in enumerate(self.products):
            values = [
                product.get("id"),
                product.get("name"),
                product.get("description"),
                f"{float(product.get('price', 0)):.2f} €",
                product.get("quantity"),
                product.get("sku"),
                product.get("category"),
                product.get("notes"),
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                if col == 4:
                    quantity = int(product.get("quantity", 0))
                    if quantity == 0:
                        item.setBackground(QColor("#ff4d4d"))
                    elif quantity < 10:
                        item.setBackground(QColor("#ffcc00"))

                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)


class ProductsPage(QWidget):
    """Professionelle Produktseite mit großer Tabellenansicht."""

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
        self._filtered_products: list[dict[str, Any]] = []

        self._create_ui()
        self.refresh_data()

    def _create_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        main_layout.addWidget(self._create_top_bar())
        main_layout.addWidget(self._create_stats_row())
        main_layout.addWidget(self._create_table_card(), 1)

    def _create_top_bar(self) -> QWidget:
        card = QFrame()
        card.setObjectName("dashboardBottomCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)

        title = QLabel("Produktverwaltung")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Produkte suchen, filtern, bearbeiten und den Bestand verwalten.")
        subtitle.setObjectName("dashboardSectionSubtitle")
        subtitle.setWordWrap(True)

        controls = QHBoxLayout()
        controls.setSpacing(12)

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

        self.add_button = QPushButton("➕ Produkt hinzufügen")
        self.add_button.clicked.connect(self._open_add_dialog)

        self.edit_button = QPushButton("✏ Bearbeiten")
        self.edit_button.setObjectName("secondaryButton")
        self.edit_button.clicked.connect(self._open_edit_dialog)

        self.stock_button = QPushButton("🔄 Bestand ändern")
        self.stock_button.setObjectName("secondaryButton")
        self.stock_button.clicked.connect(self._open_stock_dialog)

        self.delete_button = QPushButton("🗑 Löschen")
        self.delete_button.setObjectName("secondaryButton")
        self.delete_button.clicked.connect(self._delete_product)

        self.expand_button = QPushButton("🔍 Tabelle vergrößern")
        self.expand_button.setObjectName("secondaryButton")
        self.expand_button.clicked.connect(self.open_table_dialog)

        controls.addWidget(self.search_input, 2)
        controls.addWidget(self.category_filter, 1)
        controls.addWidget(self.stock_filter, 1)
        controls.addWidget(self.add_button)
        controls.addWidget(self.edit_button)
        controls.addWidget(self.stock_button)
        controls.addWidget(self.delete_button)
        controls.addWidget(self.expand_button)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addLayout(controls)

        return card

    def _create_stats_row(self) -> QWidget:
        wrapper = QWidget()
        layout = QGridLayout(wrapper)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        self.total_products_card = StatCard(
            title="Produkte gesamt",
            value="0",
            subtitle="Alle sichtbaren Produkte",
            icon="📦",
            accent="blue",
        )
        self.total_stock_card = StatCard(
            title="Gesamtbestand",
            value="0",
            subtitle="Alle Einheiten im Lager",
            icon="📚",
            accent="green",
        )
        self.low_stock_card = StatCard(
            title="Kritische Produkte",
            value="0",
            subtitle="Bestand unter 10",
            icon="⚠",
            accent="red",
        )
        self.value_card = StatCard(
            title="Lagerwert",
            value="0",
            subtitle="Gesamter Warenwert",
            icon="💶",
            accent="purple",
        )

        layout.addWidget(self.total_products_card, 0, 0)
        layout.addWidget(self.total_stock_card, 0, 1)
        layout.addWidget(self.low_stock_card, 0, 2)
        layout.addWidget(self.value_card, 0, 3)

        for col in range(4):
            layout.setColumnStretch(col, 1)

        return wrapper

    def _create_table_card(self) -> QWidget:
        card = QFrame()
        card.setObjectName("dashboardBottomCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Produktübersicht")
        title.setObjectName("dashboardSectionTitle")

        subtitle = QLabel("Alle Produkte passend zu Suche und Filtern.")
        subtitle.setObjectName("dashboardSectionSubtitle")

        self.products_table = QTableWidget()
        self.products_table.setObjectName("productsTable")
        self.products_table.setColumnCount(len(self.TABLE_COLUMNS))
        self.products_table.setHorizontalHeaderLabels(self.TABLE_COLUMNS)
        self.products_table.verticalHeader().setVisible(False)
        self.products_table.setAlternatingRowColors(True)
        self.products_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.products_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.products_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.products_table.horizontalHeader().setStretchLastSection(True)
        self.products_table.setSortingEnabled(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.products_table)

        return card

    def refresh_data(self) -> None:
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
            {
                "id": "PROD-006",
                "name": "Shaker Bottle",
                "description": "600ml Shaker",
                "price": 7.90,
                "quantity": 14,
                "sku": "SHK-600",
                "category": "Merchandise",
                "notes": "",
            },
            {
                "id": "PROD-007",
                "name": "Disinfectant Spray",
                "description": "Flächendesinfektion",
                "price": 5.20,
                "quantity": 6,
                "sku": "HYG-101",
                "category": "Hygiene",
                "notes": "Nachbestellen",
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

            if search_text and search_text not in product_text:
                continue

            if category != "Alle Kategorien" and product.get("category") != category:
                continue

            quantity = int(product.get("quantity", 0))

            if stock_mode == "Nur kritisch" and quantity >= 10:
                continue
            if stock_mode == "Nur leer" and quantity != 0:
                continue
            if stock_mode == "Nur verfügbar" and quantity <= 0:
                continue

            filtered_products.append(product)

        self._filtered_products = filtered_products
        self._populate_table(filtered_products)
        self._update_stats(filtered_products)

    def _populate_table(self, products: list[dict[str, Any]]) -> None:
        self.products_table.setSortingEnabled(False)
        self.products_table.setRowCount(len(products))

        for row, product in enumerate(products):
            values = [
                product.get("id"),
                product.get("name"),
                product.get("description"),
                f"{float(product.get('price', 0)):.2f} €",
                product.get("quantity"),
                product.get("sku"),
                product.get("category"),
                product.get("notes"),
            ]

            for col, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

                if col == 4:
                    quantity = int(product.get("quantity", 0))
                    if quantity == 0:
                        item.setBackground(QColor("#ff4d4d"))
                    elif quantity < 10:
                        item.setBackground(QColor("#ffcc00"))

                self.products_table.setItem(row, col, item)

        self.products_table.resizeColumnsToContents()
        self.products_table.setSortingEnabled(True)

        if products and self.products_table.rowCount() > 0:
            self.products_table.selectRow(0)

    def _update_stats(self, products: list[dict[str, Any]]) -> None:
        total_products = len(products)
        total_stock = sum(int(p.get("quantity", 0)) for p in products)
        low_stock = sum(1 for p in products if int(p.get("quantity", 0)) < 10)
        total_value = sum(
            float(p.get("price", 0)) * int(p.get("quantity", 0)) for p in products
        )

        self.total_products_card.set_value_animated(total_products)
        self.total_stock_card.set_value_animated(total_stock)
        self.low_stock_card.set_value_animated(low_stock)
        self.value_card.set_value(f"{total_value:.2f} €")

    def _get_selected_product(self) -> dict[str, Any] | None:
        row = self.products_table.currentRow()
        if row < 0:
            return None

        id_item = self.products_table.item(row, 0)
        if id_item is None:
            return None

        product_id = id_item.text()
        for product in self._filtered_products:
            if str(product.get("id")) == product_id:
                return product

        return None

    def open_table_dialog(self) -> None:
        dialog = ProductsTableDialog(self, self._filtered_products)
        dialog.exec()

    def _open_add_dialog(self) -> None:
        dialog = ProductDialog(self)
        if dialog.exec():
            data = dialog.get_data()

            if any(p.get("id") == data["id"] for p in self._all_products):
                QMessageBox.warning(
                    self,
                    "Doppelte Produkt-ID",
                    "Diese Produkt-ID existiert bereits.",
                )
                return

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

            for index, existing_product in enumerate(self._all_products):
                if existing_product.get("id") == product.get("id"):
                    self._all_products[index] = updated
                    break

            self._apply_filters()

    def _open_stock_dialog(self) -> None:
        product = self._get_selected_product()
        if not product:
            QMessageBox.warning(self, "Fehler", "Bitte ein Produkt auswählen.")
            return

        dialog = StockDialog(
            self,
            product_id=str(product["id"]),
            product_name=str(product["name"]),
            current_quantity=int(product["quantity"]),
        )

        if dialog.exec():
            result = dialog.get_data()

            for existing_product in self._all_products:
                if existing_product.get("id") == product.get("id"):
                    existing_product["quantity"] = result["new_quantity"]
                    note = result["reason"]
                    existing_product["notes"] = (
                        f"{existing_product.get('notes', '')} | {note}".strip(" |")
                    )
                    break

            self._apply_filters()

    def _delete_product(self) -> None:
        product = self._get_selected_product()
        if not product:
            QMessageBox.warning(self, "Fehler", "Bitte ein Produkt auswählen.")
            return

        answer = QMessageBox.question(
            self,
            "Produkt löschen",
            f"Möchtest du das Produkt '{product.get('name', '')}' wirklich löschen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer == QMessageBox.StandardButton.Yes:
            self._all_products = [
                p for p in self._all_products if p.get("id") != product.get("id")
            ]
            self._apply_filters()
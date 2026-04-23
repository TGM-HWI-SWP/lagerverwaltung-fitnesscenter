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

from src.ui.widgets.stat_card import StatCard


class ProductDialog(QDialog):
    """Dialog zum Hinzufügen oder Bearbeiten eines Produkts."""

    def __init__(self, parent: QWidget | None = None, product_data: dict[str, Any] | None = None) -> None:
        """Initialisiert den Produktdialog."""
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
        """Erstellt die Oberfläche des Dialogs."""
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
        """Füllt den Dialog im Bearbeitungsmodus mit vorhandenen Daten."""
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
            self.quantity_input.setEnabled(False)

    def _validate_and_accept(self) -> None:
        """Prüft die Eingaben und bestätigt den Dialog."""
        if not self.id_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte eine Produkt-ID angeben.")
            self.id_input.setFocus()
            return

        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte einen Produktnamen angeben.")
            self.name_input.setFocus()
            return

        if not self.description_input.text().strip():
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte eine Beschreibung angeben.")
            self.description_input.setFocus()
            return

        if self.price_input.value() <= 0:
            QMessageBox.warning(self, "Ungültiger Preis", "Bitte einen Preis größer als 0 eingeben.")
            self.price_input.setFocus()
            return

        self.accept()

    def get_data(self) -> dict[str, Any]:
        """Gibt die eingegebenen Produktdaten zurück."""
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
        parent: QWidget | None = None,
        product_id: str = "",
        product_name: str = "",
        current_quantity: int = 0,
    ) -> None:
        """Initialisiert den Bestandsdialog."""
        super().__init__(parent)

        self.product_id = product_id
        self.product_name = product_name
        self.current_quantity = current_quantity

        self.setWindowTitle("Bestand ändern")
        self.setModal(True)
        self.setMinimumWidth(460)

        self._create_ui()

    def _create_ui(self) -> None:
        """Erstellt die Oberfläche des Bestandsdialogs."""
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
        """Prüft die Eingaben und bestätigt den Dialog."""
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
        """Gibt die Daten der Bestandsänderung zurück."""
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
        """Initialisiert den Tabellen-Dialog."""
        super().__init__(parent)

        self.products = products or []

        self.setWindowTitle("Produktübersicht - vergrößerte Ansicht")
        self.setMinimumSize(1300, 760)
        self.resize(1450, 820)

        self._create_ui()
        self._populate_table()

    def _create_ui(self) -> None:
        """Erstellt die Oberfläche der großen Tabellenansicht."""
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
        """Füllt die Tabelle mit allen übergebenen Produkten."""
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(self.products))
        self.table.clearContents()

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
    """Seite zur Verwaltung von Produkten und Lagerbeständen."""

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

    def __init__(self, controller: Any | None = None) -> None:
        """Initialisiert die Produktseite."""
        super().__init__()

        self.controller = controller
        self._all_products: list[dict[str, Any]] = []
        self._filtered_products: list[dict[str, Any]] = []

        self._create_ui()
        self.refresh_data()

    def _create_ui(self) -> None:
        """Erstellt die komplette Oberfläche der Seite."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        main_layout.addWidget(self._create_top_bar())
        main_layout.addWidget(self._create_stats_row())
        main_layout.addWidget(self._create_table_card(), 1)

    def _create_top_bar(self) -> QWidget:
        """Erstellt Suche, Filter und Aktionsbuttons."""
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
        self.add_button.setObjectName("primaryButton")
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
        """Erstellt die Kennzahlenkarten."""
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
        """Erstellt die Tabellenkarte der Produktansicht."""
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

    def _map_product_to_dict(self, product: Any) -> dict[str, Any]:
        """Wandelt ein Produktobjekt in ein Dictionary um."""
        return {
            "id": getattr(product, "id", "") or "",
            "name": getattr(product, "name", "") or "",
            "description": getattr(product, "description", "") or "",
            "price": getattr(product, "price", 0.0) or 0.0,
            "quantity": getattr(product, "quantity", 0) or 0,
            "sku": getattr(product, "sku", "") or "",
            "category": getattr(product, "category", "") or "",
            "notes": getattr(product, "notes", "") or "",
        }

    def refresh_data(self) -> None:
        """Lädt Produktdaten neu und aktualisiert die Ansicht."""
        try:
            if self.controller is not None:
                products = self.controller.get_all_products()
                self._all_products = [
                    self._map_product_to_dict(product) for product in products
                ]
            else:
                self._all_products = []

            self._apply_filters()
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Produkte konnten nicht geladen werden:\n{error}",
            )
            self._all_products = []
            self._filtered_products = []
            self._populate_table([])
            self._update_stats([])

    def _apply_filters(self) -> None:
        """Filtert Produkte nach Suche, Kategorie und Bestandsstatus."""
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
                    str(product.get("notes", "")),
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
        """Füllt die Tabelle mit den gefilterten Produkten."""
        self.products_table.setSortingEnabled(False)
        self.products_table.setRowCount(len(products))
        self.products_table.clearContents()

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
        """Aktualisiert die Kennzahlenkarten."""
        total_products = len(products)
        total_stock = sum(int(product.get("quantity", 0)) for product in products)
        low_stock = sum(1 for product in products if 0 < int(product.get("quantity", 0)) < 10)
        total_value = sum(
            float(product.get("price", 0)) * int(product.get("quantity", 0))
            for product in products
        )

        self.total_products_card.set_value_animated(total_products)
        self.total_stock_card.set_value_animated(total_stock)
        self.low_stock_card.set_value_animated(low_stock)
        self.value_card.set_value(f"{total_value:.2f} €")

    def _get_selected_product(self) -> dict[str, Any] | None:
        """Gibt das aktuell ausgewählte Produkt zurück."""
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
        """Öffnet die vergrößerte Tabellenansicht."""
        dialog = ProductsTableDialog(self, self._filtered_products)
        dialog.exec()

    def _create_product_via_controller(self, data: dict[str, Any]) -> None:
        """Erstellt ein Produkt über den Controller."""
        if self.controller is None:
            raise ValueError("Kein Controller vorhanden.")

        self.controller.create_product(
            product_id=data["id"],
            name=data["name"],
            description=data["description"],
            price=data["price"],
            initial_quantity=data["quantity"],
            sku=data["sku"],
            category=data["category"],
            notes=data["notes"],
        )

    def _update_product_via_controller(
        self,
        product_id: str,
        updated: dict[str, Any],
    ) -> None:
        """Aktualisiert ein Produkt über den Controller."""
        if self.controller is None:
            raise ValueError("Kein Controller vorhanden.")

        self.controller.update_product(
            product_id=product_id,
            name=updated["name"],
            description=updated["description"],
            price=updated["price"],
            sku=updated["sku"],
            category=updated["category"],
            notes=updated["notes"],
        )

    def _delete_product_via_controller(self, product_id: str) -> None:
        """Löscht ein Produkt über den Controller."""
        if self.controller is None:
            raise ValueError("Kein Controller vorhanden.")

        if not hasattr(self.controller, "delete_product"):
            raise AttributeError(
                "Dein Controller hat keine Methode 'delete_product(product_id)'."
            )

        self.controller.delete_product(product_id)

    def _open_add_dialog(self) -> None:
        """Öffnet den Dialog zum Hinzufügen eines Produkts."""
        dialog = ProductDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.get_data()

        try:
            self._create_product_via_controller(data)
            self.refresh_data()
            QMessageBox.information(
                self,
                "Erfolg",
                f"Produkt '{data['name']}' wurde erfolgreich erstellt.",
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Produkt konnte nicht erstellt werden:\n{error}",
            )

    def _open_edit_dialog(self) -> None:
        """Öffnet den Dialog zum Bearbeiten eines Produkts."""
        product = self._get_selected_product()
        if not product:
            QMessageBox.warning(self, "Fehler", "Bitte ein Produkt auswählen.")
            return

        dialog = ProductDialog(self, product)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        updated = dialog.get_data()

        try:
            self._update_product_via_controller(str(product["id"]), updated)
            self.refresh_data()
            QMessageBox.information(
                self,
                "Erfolg",
                f"Produkt '{updated['name']}' wurde erfolgreich aktualisiert.",
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Produkt konnte nicht aktualisiert werden:\n{error}",
            )

    def _open_stock_dialog(self) -> None:
        """Öffnet den Dialog zur Bestandsänderung."""
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

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        result = dialog.get_data()

        try:
            if self.controller is None:
                QMessageBox.warning(self, "Fehler", "Kein Controller vorhanden.")
                return

            if result["mode"] == "Wareneingang":
                self.controller.add_stock(
                    product["id"],
                    result["amount"],
                    result["reason"],
                    "ui",
                )
            else:
                self.controller.remove_stock(
                    product["id"],
                    result["amount"],
                    result["reason"],
                    "ui",
                )

            self.refresh_data()
            QMessageBox.information(
                self,
                "Erfolg",
                f"Der Bestand von '{product['name']}' wurde erfolgreich geändert.",
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Bestand konnte nicht geändert werden:\n{error}",
            )

    def _delete_product(self) -> None:
        """Löscht das ausgewählte Produkt."""
        product = self._get_selected_product()
        if not product:
            QMessageBox.warning(self, "Fehler", "Bitte ein Produkt auswählen.")
            return

        answer = QMessageBox.question(
            self,
            "Produkt löschen",
            (
                f"Möchtest du das Produkt '{product.get('name', '')}' "
                f"mit der ID '{product.get('id', '')}' wirklich löschen?"
            ),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            self._delete_product_via_controller(str(product["id"]))
            self.refresh_data()
            QMessageBox.information(
                self,
                "Erfolg",
                f"Produkt '{product.get('name', '')}' wurde gelöscht.",
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Fehler",
                f"Produkt konnte nicht gelöscht werden:\n{error}",
            )
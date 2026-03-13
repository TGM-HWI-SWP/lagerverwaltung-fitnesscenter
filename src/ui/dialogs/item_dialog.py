from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class ItemDialog(QDialog):
    """Dialog zum Hinzufügen oder Bearbeiten eines Lagerartikels."""

    def __init__(self, parent=None, item_data: dict | None = None) -> None:
        super().__init__(parent)
        self.item_data = item_data
        self.is_edit_mode = item_data is not None

        self.setWindowTitle(
            "Artikel bearbeiten" if self.is_edit_mode else "Artikel hinzufügen"
        )
        self.setModal(True)
        self.setMinimumWidth(520)
        self.setObjectName("itemDialog")

        self._create_ui()
        self._fill_data_if_needed()

    def _create_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(18)

        header_widget = self._create_header()
        form_widget = self._create_form()
        button_widget = self._create_buttons()

        main_layout.addWidget(header_widget)
        main_layout.addWidget(form_widget)
        main_layout.addWidget(button_widget)

    def _create_header(self) -> QWidget:
        header = QWidget()
        layout = QVBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        self.title_label = QLabel(
            "Lagerartikel bearbeiten"
            if self.is_edit_mode
            else "Neuen Lagerartikel anlegen"
        )
        self.title_label.setObjectName("dialogTitle")

        self.subtitle_label = QLabel(
            "Erfasse alle wichtigen Informationen für den Lagerbestand."
        )
        self.subtitle_label.setObjectName("dialogSubtitle")
        self.subtitle_label.setWordWrap(True)

        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)

        return header

    def _create_form(self) -> QWidget:
        form_container = QWidget()
        form_container.setObjectName("dialogFormCard")

        form_layout = QFormLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(14)
        form_layout.setLabelAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )

        self.article_no_input = QLineEdit()
        self.article_no_input.setPlaceholderText("z. B. FG007")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("z. B. Whey Protein Chocolate")

        self.category_input = QComboBox()
        self.category_input.addItems(
            [
                "Supplements",
                "Getränke",
                "Merchandise",
                "Hygiene",
                "Geräte-Zubehör",
            ]
        )

        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 100000)
        self.stock_input.setValue(0)

        self.min_stock_input = QSpinBox()
        self.min_stock_input.setRange(0, 100000)
        self.min_stock_input.setValue(5)

        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("z. B. Regal A1")

        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0.0, 100000.0)
        self.price_input.setDecimals(2)
        self.price_input.setSuffix(" €")
        self.price_input.setValue(0.0)

        form_layout.addRow("Artikelnummer:", self.article_no_input)
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Kategorie:", self.category_input)
        form_layout.addRow("Bestand:", self.stock_input)
        form_layout.addRow("Mindestbestand:", self.min_stock_input)
        form_layout.addRow("Lagerort:", self.location_input)
        form_layout.addRow("Preis:", self.price_input)

        return form_container

    def _create_buttons(self) -> QWidget:
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(12)

        button_layout.addStretch()

        self.cancel_button = QPushButton("Abbrechen")
        self.cancel_button.setObjectName("secondaryButton")
        self.cancel_button.clicked.connect(self.reject)

        self.save_button = QPushButton(
            "Änderungen speichern" if self.is_edit_mode else "Artikel speichern"
        )
        self.save_button.setObjectName("primaryButton")
        self.save_button.clicked.connect(self._validate_and_accept)

        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)

        return button_widget

    def _fill_data_if_needed(self) -> None:
        """Füllt Felder, falls ein bestehender Artikel bearbeitet wird."""
        if not self.item_data:
            return

        self.article_no_input.setText(str(self.item_data.get("article_no", "")))
        self.name_input.setText(str(self.item_data.get("name", "")))
        self.location_input.setText(str(self.item_data.get("location", "")))

        category = str(self.item_data.get("category", "Supplements"))
        index = self.category_input.findText(category)
        if index >= 0:
            self.category_input.setCurrentIndex(index)

        self.stock_input.setValue(int(self.item_data.get("stock", 0)))
        self.min_stock_input.setValue(int(self.item_data.get("min_stock", 0)))
        self.price_input.setValue(float(self.item_data.get("price", 0.0)))

        if self.is_edit_mode:
            self.article_no_input.setReadOnly(True)

    def _validate_and_accept(self) -> None:
        """Prüft die Eingaben und schließt den Dialog bei gültigen Daten."""
        article_no = self.article_no_input.text().strip()
        name = self.name_input.text().strip()
        location = self.location_input.text().strip()

        if not article_no:
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte eine Artikelnummer angeben.")
            self.article_no_input.setFocus()
            return

        if not name:
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte einen Artikelnamen angeben.")
            self.name_input.setFocus()
            return

        if not location:
            QMessageBox.warning(self, "Fehlende Eingabe", "Bitte einen Lagerort angeben.")
            self.location_input.setFocus()
            return

        if self.min_stock_input.value() > self.stock_input.value():
            reply = QMessageBox.question(
                self,
                "Mindestbestand höher als Bestand",
                "Der Mindestbestand ist höher als der aktuelle Bestand.\n"
                "Soll der Artikel trotzdem gespeichert werden?",
            )
            if reply != QMessageBox.StandardButton.Yes:
                return

        self.accept()

    def get_data(self) -> dict:
        """Gibt die eingegebenen Artikeldaten zurück."""
        return {
            "article_no": self.article_no_input.text().strip(),
            "name": self.name_input.text().strip(),
            "category": self.category_input.currentText(),
            "stock": self.stock_input.value(),
            "min_stock": self.min_stock_input.value(),
            "location": self.location_input.text().strip(),
            "price": self.price_input.value(),
        }
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class StockDialog(QDialog):
    """Dialog zum Ändern des Lagerbestands eines Artikels."""

    def __init__(
        self,
        parent=None,
        article_no: str = "",
        article_name: str = "",
        current_stock: int = 0,
    ) -> None:
        super().__init__(parent)

        self.article_no = article_no
        self.article_name = article_name
        self.current_stock = current_stock

        self.setWindowTitle("Bestand ändern")
        self.setModal(True)
        self.setMinimumWidth(520)
        self.setObjectName("stockDialog")

        self._create_ui()

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

        self.title_label = QLabel("Lagerbestand anpassen")
        self.title_label.setObjectName("dialogTitle")

        subtitle_text = (
            f"Artikel: {self.article_name or '-'} "
            f"({self.article_no or '-'})\n"
            f"Aktueller Bestand: {self.current_stock}"
        )
        self.subtitle_label = QLabel(subtitle_text)
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

        self.action_input = QComboBox()
        self.action_input.addItems(
            [
                "Wareneingang",
                "Warenausgang",
                "Inventurkorrektur (+)",
                "Inventurkorrektur (-)",
            ]
        )
        self.action_input.currentIndexChanged.connect(self._update_preview)

        self.amount_input = QSpinBox()
        self.amount_input.setRange(1, 100000)
        self.amount_input.setValue(1)
        self.amount_input.valueChanged.connect(self._update_preview)

        self.reason_input = QTextEdit()
        self.reason_input.setPlaceholderText(
            "Grund eingeben, z. B. Lieferung, Verkauf, Reinigung, Inventur ..."
        )
        self.reason_input.setMinimumHeight(100)

        self.preview_label = QLabel()
        self.preview_label.setObjectName("stockPreviewLabel")
        self.preview_label.setWordWrap(True)

        form_layout.addRow("Aktion:", self.action_input)
        form_layout.addRow("Menge:", self.amount_input)
        form_layout.addRow("Grund:", self.reason_input)
        form_layout.addRow("Vorschau:", self.preview_label)

        self._update_preview()

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

        self.save_button = QPushButton("Bestandsänderung speichern")
        self.save_button.setObjectName("primaryButton")
        self.save_button.clicked.connect(self._validate_and_accept)

        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)

        return button_widget

    def _update_preview(self) -> None:
        """Aktualisiert die Vorschau des neuen Bestands."""
        amount = self.amount_input.value()
        action = self.action_input.currentText()

        if action in ("Wareneingang", "Inventurkorrektur (+)"):
            new_stock = self.current_stock + amount
            prefix = "+"
        else:
            new_stock = self.current_stock - amount
            prefix = "-"

        self.preview_label.setText(
            f"Aktueller Bestand: {self.current_stock}\n"
            f"Änderung: {prefix}{amount}\n"
            f"Neuer Bestand: {new_stock}"
        )

    def _validate_and_accept(self) -> None:
        """Validiert die Eingaben vor dem Speichern."""
        amount = self.amount_input.value()
        action = self.action_input.currentText()
        reason = self.reason_input.toPlainText().strip()

        if not reason:
            QMessageBox.warning(
                self,
                "Fehlende Eingabe",
                "Bitte gib einen Grund für die Bestandsänderung an.",
            )
            self.reason_input.setFocus()
            return

        if action in ("Warenausgang", "Inventurkorrektur (-)"):
            new_stock = self.current_stock - amount
            if new_stock < 0:
                QMessageBox.warning(
                    self,
                    "Ungültige Bestandsänderung",
                    "Der Bestand darf nicht negativ werden.",
                )
                return

        self.accept()

    def get_data(self) -> dict:
        """Gibt die eingegebenen Bestandsdaten zurück."""
        action = self.action_input.currentText()
        amount = self.amount_input.value()

        if action in ("Wareneingang", "Inventurkorrektur (+)"):
            signed_amount = amount
            movement_type = "IN"
        else:
            signed_amount = -amount
            movement_type = "OUT"

        return {
            "article_no": self.article_no,
            "article_name": self.article_name,
            "current_stock": self.current_stock,
            "action": action,
            "amount": amount,
            "signed_amount": signed_amount,
            "movement_type": movement_type,
            "reason": self.reason_input.toPlainText().strip(),
            "new_stock": self.current_stock + signed_amount,
        }
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class EquipmentPage(QWidget):
    def __init__(self, controller=None) -> None:
        super().__init__()
        self.controller = controller

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Geräte-Seite"))
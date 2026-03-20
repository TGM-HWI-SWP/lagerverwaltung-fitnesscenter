from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class VendingPage(QWidget):
    def __init__(self, controller=None) -> None:
        super().__init__()
        self.controller = controller

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Automaten-Seite"))
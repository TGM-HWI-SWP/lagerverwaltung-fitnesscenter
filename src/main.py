import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow


def load_stylesheet(app: QApplication) -> None:
    """Lädt das QSS-Stylesheet der Anwendung."""
    qss_path = Path(__file__).parent / "ui" / "styles" / "main.qss"

    if qss_path.exists():
        with qss_path.open("r", encoding="utf-8") as file:
            app.setStyleSheet(file.read())
    else:
        print(f"Warnung: Stylesheet nicht gefunden: {qss_path}")


def main() -> None:
    """Startpunkt der Anwendung."""
    app = QApplication(sys.argv)

    app.setApplicationName("FitnessCenter Lagerverwaltung")
    app.setOrganizationName("HTL Projektteam")

    load_stylesheet(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
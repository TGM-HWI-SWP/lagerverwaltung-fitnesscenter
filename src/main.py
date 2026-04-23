import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from src.adapters.report import ConsoleReportAdapter
from src.adapters.supabase_repository import (
    SupabaseEmployeeRepository,
    SupabaseEquipmentRepository,
    SupabaseMemberRepository,
    SupabaseMovementRepository,
    SupabaseProductRepository,
    SupabaseVendingMachineRepository,
)
from src.services import FitnessCenterService
from src.ui.auth.login_window import LoginWindow


def load_stylesheet(app: QApplication) -> None:
    """Lädt das globale QSS-Stylesheet der Anwendung."""
    qss_path = Path(__file__).parent / "ui" / "styles" / "main.qss"

    if qss_path.exists():
        with qss_path.open("r", encoding="utf-8") as file:
            app.setStyleSheet(file.read())
    else:
        print(f"Warnung: Stylesheet nicht gefunden: {qss_path}")


def build_service() -> FitnessCenterService:
    """Erstellt den zentralen Service mit allen benötigten Adaptern."""
    product_repository = SupabaseProductRepository()
    movement_repository = SupabaseMovementRepository()
    member_repository = SupabaseMemberRepository()
    employee_repository = SupabaseEmployeeRepository()
    equipment_repository = SupabaseEquipmentRepository()
    vending_machine_repository = SupabaseVendingMachineRepository()
    report_adapter = ConsoleReportAdapter()

    return FitnessCenterService(
        product_repository=product_repository,
        movement_repository=movement_repository,
        member_repository=member_repository,
        employee_repository=employee_repository,
        equipment_repository=equipment_repository,
        vending_machine_repository=vending_machine_repository,
        report_adapter=report_adapter,
    )


def main() -> None:
    """Startet die GUI-Anwendung."""
    app = QApplication(sys.argv)

    app.setApplicationName("FitnessCenter Lagerverwaltung")
    app.setOrganizationName("HTL Projektteam")

    load_stylesheet(app)

    service = build_service()

    window = LoginWindow(controller=service)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
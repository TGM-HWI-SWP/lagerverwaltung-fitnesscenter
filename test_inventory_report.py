from src.adapters.report import ConsoleReportAdapter
from src.adapters.repository import InMemoryRepository
from src.services import FitnessCenterService


def main():
    # Repositories
    repo = InMemoryRepository()

    # Report Adapter
    report_adapter = ConsoleReportAdapter()

    # Service
    service = FitnessCenterService(
        product_repository=repo,
        movement_repository=repo,
        member_repository=repo,
        employee_repository=repo,
        equipment_repository=repo,
        vending_machine_repository=repo,
        report_adapter=report_adapter,
    )

    # Testdaten erstellen
    service.create_product(
        product_id="P1",
        name="Protein Bar",
        description="Chocolate protein bar",
        price=2.5,
        category="Food",
        initial_quantity=0,
    )

    service.create_product(
        product_id="P2",
        name="Energy Drink",
        description="Sugar free drink",
        price=3.0,
        category="Drink",
        initial_quantity=0,
    )

    # Lagerbestand hinzufügen
    service.add_stock("P1", 50, "Initial stock")
    service.add_stock("P2", 30, "Initial stock")

    # Report generieren
    report = service.generate_inventory_report()
    print(report)


if __name__ == "__main__":
    main()
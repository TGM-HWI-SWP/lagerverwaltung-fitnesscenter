from src.adapters.report import ConsoleReportAdapter
from src.adapters.repository import (
    InMemoryProductRepository,
    InMemoryMovementRepository,
    InMemoryMemberRepository,
    InMemoryEmployeeRepository,
    InMemoryEquipmentRepository,
    InMemoryVendingMachineRepository,
)
from src.services import FitnessCenterService


def main():
    # Repositories erstellen
    product_repo = InMemoryProductRepository()
    movement_repo = InMemoryMovementRepository()
    member_repo = InMemoryMemberRepository()
    employee_repo = InMemoryEmployeeRepository()
    equipment_repo = InMemoryEquipmentRepository()
    machine_repo = InMemoryVendingMachineRepository()

    # Report Adapter
    report_adapter = ConsoleReportAdapter()

    # Service
    service = FitnessCenterService(
        product_repository=product_repo,
        movement_repository=movement_repo,
        member_repository=member_repo,
        employee_repository=employee_repo,
        equipment_repository=equipment_repo,
        vending_machine_repository=machine_repo,
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
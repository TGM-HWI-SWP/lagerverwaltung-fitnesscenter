"""Einfacher Test für die Erstellung eines Produkts.

Dieses Modul enthält einen grundlegenden Test für den FitnessCenterService,
um sicherzustellen, dass Produkte korrekt erstellt und geladen werden können.
"""

from src.services import FitnessCenterService
from src.adapters.repository import (
    InMemoryProductRepository,
    InMemoryMovementRepository,
    InMemoryMemberRepository,
    InMemoryEmployeeRepository,
    InMemoryEquipmentRepository,
    InMemoryVendingMachineRepository,
)
from src.adapters.report import ConsoleReportAdapter


def create_service():
    """Erstellt eine Instanz des FitnessCenterService mit In-Memory-Repositories.

    Wird verwendet, um eine isolierte Testumgebung ohne Datenbank zu schaffen.
    """
    return FitnessCenterService(
        product_repository=InMemoryProductRepository(),
        movement_repository=InMemoryMovementRepository(),
        member_repository=InMemoryMemberRepository(),
        employee_repository=InMemoryEmployeeRepository(),
        equipment_repository=InMemoryEquipmentRepository(),
        vending_machine_repository=InMemoryVendingMachineRepository(),
        report_adapter=ConsoleReportAdapter(),
    )


def test_create_product():
    """Testet, ob ein Produkt erfolgreich erstellt und wieder geladen werden kann."""
    service = create_service()

    service.create_product("p1", "Energy Drink", "Refreshing drink", 2.99)

    product = service.get_product("p1")

    assert product is not None
    assert product.name == "Energy Drink"
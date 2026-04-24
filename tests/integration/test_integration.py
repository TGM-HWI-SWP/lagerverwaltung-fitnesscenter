"""Integration Tests

Dieses Modul enthält Integrationstests für das gesamte System.
Es überprüft das Zusammenspiel von Repositories, Services und Report-Adapter.
"""

import pytest
from src.adapters.repository import (
    InMemoryProductRepository,
    InMemoryMovementRepository,
    InMemoryMemberRepository,
    InMemoryEmployeeRepository,
    InMemoryEquipmentRepository,
    InMemoryVendingMachineRepository,
)
from src.adapters.report import ConsoleReportAdapter
from src.services import FitnessCenterService


class TestIntegration:
    """Integrationstests für das Fitnesscenter-System."""

    def test_full_workflow(self):
        """Testet den kompletten Workflow:
        
        - Erstellen von Produkten
        - Durchführen von Lagerbewegungen
        - Überprüfung von Beständen
        - Validierung der Bewegungen und des Gesamtwerts
        """

        # Repositories
        product_repo = InMemoryProductRepository()
        movement_repo = InMemoryMovementRepository()
        member_repo = InMemoryMemberRepository()
        employee_repo = InMemoryEmployeeRepository()
        equipment_repo = InMemoryEquipmentRepository()
        machine_repo = InMemoryVendingMachineRepository()

        # Service
        service = FitnessCenterService(
            product_repository=product_repo,
            movement_repository=movement_repo,
            member_repository=member_repo,
            employee_repository=employee_repo,
            equipment_repository=equipment_repo,
            vending_machine_repository=machine_repo,
            report_adapter=ConsoleReportAdapter(),
        )

        # Produkte erstellen
        service.create_product(
            "P1", "Protein Bar", "Test Produkt", 2.5, category="Food", initial_quantity=10
        )
        service.create_product(
            "P2", "Energy Drink", "Test Produkt", 3.0, category="Drink", initial_quantity=20
        )

        # Lagerbewegungen
        service.add_stock("P1", 5, "Nachlieferung")
        service.remove_stock("P1", 3, "Verkauf")
        service.add_stock("P2", 10, "Nachlieferung")

        # Assertions
        product = service.get_product("P1")
        assert product.quantity == 12  # 10 + 5 - 3

        movements = service.get_movements()
        assert len(movements) == 3

        total_value = service.get_total_inventory_value()
        assert total_value > 0


    def test_report_generation(self):
        """Testet die Generierung des Lagerbestandsberichts:
        
        - Erstellung von Testprodukten
        - Generierung des Reports
        - Überprüfung, ob Inhalte korrekt enthalten sind
        """

        # Repositories
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

        # Testdaten
        service.create_product("P1", "Produkt A", "Test", 100.0, initial_quantity=10)
        service.create_product("P2", "Produkt B", "Test", 50.0, initial_quantity=5)

        # Report
        report = service.generate_inventory_report()

        # Assertions
        assert len(report) > 0
        assert "P1" in report
        assert "P2" in report
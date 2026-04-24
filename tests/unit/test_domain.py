"""Tests - Unit Tests für die Geschäftslogik

Dieses Modul enthält Unit-Tests für die Domain-Klasse Product
sowie für die Business-Logic im FitnessCenterService.
"""

import pytest
from src.domain.product import Product
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


class TestProduct:
    """Unit-Tests für die Product-Domain-Klasse."""

    def test_product_creation(self):
        """Testet die korrekte Erstellung eines Produkts."""
        product = Product(
            id="P001",
            name="Test Produkt",
            description="Ein Test",
            price=10.0,
            quantity=5,
        )
        assert product.id == "P001"
        assert product.name == "Test Produkt"
        assert product.quantity == 5

    def test_product_validation_negative_price(self):
        """Testet, dass ein negativer Preis eine Exception auslöst."""
        with pytest.raises(ValueError):
            Product(
                id="P001",
                name="Test",
                description="Test",
                price=-10.0,
            )

    def test_update_quantity(self):
        """Testet das Erhöhen und Verringern des Lagerbestands."""
        product = Product(
            id="P001",
            name="Test",
            description="Test",
            price=10.0,
            quantity=10,
        )
        product.update_quantity(5)
        assert product.quantity == 15

        product.update_quantity(-5)
        assert product.quantity == 10

    def test_update_quantity_insufficient(self):
        """Testet, dass der Bestand nicht negativ werden kann."""
        product = Product(
            id="P001",
            name="Test",
            description="Test",
            price=10.0,
            quantity=5,
        )
        with pytest.raises(ValueError):
            product.update_quantity(-10)

    def test_get_total_value(self):
        """Testet die Berechnung des Gesamtwerts eines Produkts."""
        product = Product(
            id="P001",
            name="Test",
            description="Test",
            price=10.0,
            quantity=5,
        )
        assert product.get_total_value() == 50.0


class TestFitnessCenterService:
    """Unit-Tests für die Business-Logik im FitnessCenterService."""

    @pytest.fixture
    def service(self):
        """Erstellt eine Service-Instanz mit In-Memory-Repositories für Tests."""
        product_repo = InMemoryProductRepository()
        movement_repo = InMemoryMovementRepository()
        member_repo = InMemoryMemberRepository()
        employee_repo = InMemoryEmployeeRepository()
        equipment_repo = InMemoryEquipmentRepository()
        machine_repo = InMemoryVendingMachineRepository()

        return FitnessCenterService(
            product_repository=product_repo,
            movement_repository=movement_repo,
            member_repository=member_repo,
            employee_repository=employee_repo,
            equipment_repository=equipment_repo,
            vending_machine_repository=machine_repo,
            report_adapter=ConsoleReportAdapter(),
        )

    def test_create_product(self, service):
        """Testet das Erstellen eines Produkts über den Service."""
        product = service.create_product(
            product_id="P001",
            name="Test Produkt",
            description="Ein Test",
            price=15.0,
            category="Test",
            initial_quantity=10,
        )
        assert product.id == "P001"
        assert product.quantity == 10

    def test_add_stock(self, service):
        """Testet das Hinzufügen von Lagerbestand."""
        service.create_product("P001", "Test", "Test", 10.0, initial_quantity=5)
        service.add_stock("P001", 3, reason="Neuer Einkauf")

        product = service.get_product("P001")
        assert product.quantity == 8

    def test_remove_stock(self, service):
        """Testet das Entfernen von Lagerbestand."""
        service.create_product("P001", "Test", "Test", 10.0, initial_quantity=10)
        service.remove_stock("P001", 3, reason="Verkauf")

        product = service.get_product("P001")
        assert product.quantity == 7

    def test_remove_stock_insufficient(self, service):
        """Testet Fehlerfall: Entfernen von zu viel Bestand."""
        service.create_product("P001", "Test", "Test", 10.0, initial_quantity=5)

        with pytest.raises(ValueError):
            service.remove_stock("P001", 10)

    def test_get_all_products(self, service):
        """Testet das Laden aller Produkte."""
        service.create_product("P001", "Produkt 1", "Test", 10.0)
        service.create_product("P002", "Produkt 2", "Test", 20.0)

        products = service.get_all_products()
        assert len(products) == 2

    def test_get_total_inventory_value(self, service):
        """Testet die Berechnung des gesamten Lagerwerts."""
        service.create_product("P001", "Test 1", "Test", 10.0, initial_quantity=5)
        service.create_product("P002", "Test 2", "Test", 20.0, initial_quantity=3)

        total = service.get_total_inventory_value()
        assert total == 110.0

    def test_get_movements(self, service):
        """Testet das Abrufen aller Lagerbewegungen."""
        service.create_product("P001", "Test", "Test", 10.0, initial_quantity=5)
        service.add_stock("P001", 3)
        service.remove_stock("P001", 2)

        movements = service.get_movements()
        assert len(movements) == 2
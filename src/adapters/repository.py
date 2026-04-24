"""Repository Adapter - In-Memory Implementierungen

Dieses Modul enthält In-Memory Implementierungen der Repository-Interfaces.
Sie dienen hauptsächlich für Tests und schnelle Entwicklung ohne echte Datenbank.
"""


from typing import Dict, List, Optional

from ..domain.employee import Employee
from ..domain.equipment import Equipment
from ..domain.member import Member
from ..domain.product import Product
from ..domain.vending_machine import VendingMachine
from ..domain.warehouse import Movement
from ..ports.employee_repository_port import EmployeeRepositoryPort
from ..ports.equipment_repository_port import EquipmentRepositoryPort
from ..ports.member_repository_port import MemberRepositoryPort
from ..ports.movement_repository_port import MovementRepositoryPort
from ..ports.product_repository_port import ProductRepositoryPort
from ..ports.vending_machine_repository_port import VendingMachineRepositoryPort
from .supabase_repository import (
    SupabaseEmployeeRepository,
    SupabaseEquipmentRepository,
    SupabaseMemberRepository,
    SupabaseMovementRepository,
    SupabaseProductRepository,
    SupabaseVendingMachineRepository,
)


class InMemoryProductRepository(ProductRepositoryPort):
    """In-Memory Repository für Produkte."""

    def __init__(self):
        """Initialisiert einen leeren Produktspeicher."""
        self.products: Dict[str, Product] = {}

    def save_product(self, product: Product) -> None:
        """Speichert oder überschreibt ein Produkt."""
        self.products[product.id] = product

    def load_product(self, product_id: str) -> Optional[Product]:
        """Lädt ein Produkt anhand seiner ID."""
        return self.products.get(product_id)

    def load_all_products(self) -> List[Product]:
        """Gibt alle gespeicherten Produkte zurück."""
        return list(self.products.values())

    def delete_product(self, product_id: str) -> None:
        """Löscht ein Produkt, falls vorhanden."""
        if product_id in self.products:
            del self.products[product_id]


class InMemoryMovementRepository(MovementRepositoryPort):
    """In-Memory Repository für Lagerbewegungen."""

    def __init__(self):
        """Initialisiert eine leere Bewegungsliste."""
        self.movements: List[Movement] = []

    def save_movement(self, movement: Movement) -> None:
        """Speichert eine neue Bewegung."""
        self.movements.append(movement)

    def load_movements(self) -> List[Movement]:
        """Gibt alle Bewegungen zurück."""
        return self.movements.copy()


class InMemoryMemberRepository(MemberRepositoryPort):
    """In-Memory Repository für Mitglieder."""

    def __init__(self):
        """Initialisiert einen leeren Mitgliederspeicher."""
        self.members: Dict[str, Member] = {}

    def save_member(self, member: Member) -> None:
        """Speichert oder aktualisiert ein Mitglied."""
        self.members[member.member_id] = member

    def load_member(self, member_id: str) -> Optional[Member]:
        """Lädt ein Mitglied anhand der ID."""
        return self.members.get(member_id)

    def load_all_members(self) -> List[Member]:
        """Gibt alle Mitglieder zurück."""
        return list(self.members.values())

    def delete_member(self, member_id: str) -> None:
        """Löscht ein Mitglied, falls vorhanden."""
        if member_id in self.members:
            del self.members[member_id]


class InMemoryEmployeeRepository(EmployeeRepositoryPort):
    """In-Memory Repository für Mitarbeiter."""

    def __init__(self):
        """Initialisiert einen leeren Mitarbeiterspeicher."""
        self.employees: Dict[str, Employee] = {}

    def save_employee(self, employee: Employee) -> None:
        """Speichert oder aktualisiert einen Mitarbeiter."""
        self.employees[employee.employee_id] = employee

    def load_employee(self, employee_id: str) -> Optional[Employee]:
        """Lädt einen Mitarbeiter anhand der ID."""
        return self.employees.get(employee_id)

    def load_all_employees(self) -> List[Employee]:
        """Gibt alle Mitarbeiter zurück."""
        return list(self.employees.values())

    def delete_employee(self, employee_id: str) -> None:
        """Löscht einen Mitarbeiter, falls vorhanden."""
        if employee_id in self.employees:
            del self.employees[employee_id]


class InMemoryEquipmentRepository(EquipmentRepositoryPort):
    """In-Memory Repository für Equipment."""

    def __init__(self):
        """Initialisiert einen leeren Equipment-Speicher."""
        self.equipment: Dict[str, Equipment] = {}

    def save_equipment(self, equipment: Equipment) -> None:
        """Speichert oder aktualisiert Equipment."""
        self.equipment[equipment.equipment_id] = equipment

    def load_equipment(self, equipment_id: str) -> Optional[Equipment]:
        """Lädt Equipment anhand der ID."""
        return self.equipment.get(equipment_id)

    def load_all_equipment(self) -> List[Equipment]:
        """Gibt alles Equipment zurück."""
        return list(self.equipment.values())

    def delete_equipment(self, equipment_id: str) -> None:
        """Löscht Equipment, falls vorhanden."""
        if equipment_id in self.equipment:
            del self.equipment[equipment_id]


class InMemoryVendingMachineRepository(VendingMachineRepositoryPort):
    """In-Memory Repository für Verkaufsautomaten."""

    def __init__(self):
        """Initialisiert einen leeren Automaten-Speicher."""
        self.machines: Dict[str, VendingMachine] = {}

    def save_machine(self, machine: VendingMachine) -> None:
        """Speichert oder aktualisiert einen Automaten."""
        self.machines[machine.machine_id] = machine

    def load_machine(self, machine_id: str) -> Optional[VendingMachine]:
        """Lädt einen Automaten anhand der ID."""
        return self.machines.get(machine_id)

    def load_all_machines(self) -> List[VendingMachine]:
        """Gibt alle Automaten zurück."""
        return list(self.machines.values())

    def delete_machine(self, machine_id: str) -> None:
        """Löscht einen Automaten, falls vorhanden."""
        if machine_id in self.machines:
            del self.machines[machine_id]


class RepositoryFactory:
    """Factory zur Erstellung von Repository-Implementierungen."""

    @staticmethod
    def create_product_repository(
        repository_type: str = "memory",
    ) -> ProductRepositoryPort:
        """Erstellt ein Produkt-Repository basierend auf dem Typ."""
        if repository_type == "memory":
            return InMemoryProductRepository()
        if repository_type == "supabase":
            return SupabaseProductRepository()
        raise ValueError(f"Unbekannter Repository-Typ: {repository_type}")

    @staticmethod
    def create_movement_repository(
        repository_type: str = "memory",
    ) -> MovementRepositoryPort:
        """Erstellt ein Movement-Repository basierend auf dem Typ."""
        if repository_type == "memory":
            return InMemoryMovementRepository()
        if repository_type == "supabase":
            return SupabaseMovementRepository()
        raise ValueError(f"Unbekannter Repository-Typ: {repository_type}")

    @staticmethod
    def create_member_repository(
        repository_type: str = "memory",
    ) -> MemberRepositoryPort:
        """Erstellt ein Member-Repository basierend auf dem Typ."""
        if repository_type == "memory":
            return InMemoryMemberRepository()
        if repository_type == "supabase":
            return SupabaseMemberRepository()
        raise ValueError(f"Unbekannter Repository-Typ: {repository_type}")

    @staticmethod
    def create_employee_repository(
        repository_type: str = "memory",
    ) -> EmployeeRepositoryPort:
        """Erstellt ein Employee-Repository basierend auf dem Typ."""
        if repository_type == "memory":
            return InMemoryEmployeeRepository()
        if repository_type == "supabase":
            return SupabaseEmployeeRepository()
        raise ValueError(f"Unbekannter Repository-Typ: {repository_type}")

    @staticmethod
    def create_equipment_repository(
        repository_type: str = "memory",
    ) -> EquipmentRepositoryPort:
        """Erstellt ein Equipment-Repository basierend auf dem Typ."""
        if repository_type == "memory":
            return InMemoryEquipmentRepository()
        if repository_type == "supabase":
            return SupabaseEquipmentRepository()
        raise ValueError(f"Unbekannter Repository-Typ: {repository_type}")

    @staticmethod
    def create_vending_machine_repository(
        repository_type: str = "memory",
    ) -> VendingMachineRepositoryPort:
        """Erstellt ein VendingMachine-Repository basierend auf dem Typ."""
        if repository_type == "memory":
            return InMemoryVendingMachineRepository()
        if repository_type == "supabase":
            return SupabaseVendingMachineRepository()
        raise ValueError(f"Unbekannter Repository-Typ: {repository_type}")
"""Repository Adapter - In-Memory Implementierungen"""

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
    def __init__(self):
        self.products: Dict[str, Product] = {}

    def save_product(self, product: Product) -> None:
        self.products[product.id] = product

    def load_product(self, product_id: str) -> Optional[Product]:
        return self.products.get(product_id)

    def load_all_products(self) -> List[Product]:
        return list(self.products.values())

    def delete_product(self, product_id: str) -> None:
        if product_id in self.products:
            del self.products[product_id]


class InMemoryMovementRepository(MovementRepositoryPort):
    def __init__(self):
        self.movements: List[Movement] = []

    def save_movement(self, movement: Movement) -> None:
        self.movements.append(movement)

    def load_movements(self) -> List[Movement]:
        return self.movements.copy()


class InMemoryMemberRepository(MemberRepositoryPort):
    def __init__(self):
        self.members: Dict[str, Member] = {}

    def save_member(self, member: Member) -> None:
        self.members[member.member_id] = member

    def load_member(self, member_id: str) -> Optional[Member]:
        return self.members.get(member_id)

    def load_all_members(self) -> List[Member]:
        return list(self.members.values())

    def delete_member(self, member_id: str) -> None:
        if member_id in self.members:
            del self.members[member_id]


class InMemoryEmployeeRepository(EmployeeRepositoryPort):
    def __init__(self):
        self.employees: Dict[str, Employee] = {}

    def save_employee(self, employee: Employee) -> None:
        self.employees[employee.employee_id] = employee

    def load_employee(self, employee_id: str) -> Optional[Employee]:
        return self.employees.get(employee_id)

    def load_all_employees(self) -> List[Employee]:
        return list(self.employees.values())

    def delete_employee(self, employee_id: str) -> None:
        if employee_id in self.employees:
            del self.employees[employee_id]


class InMemoryEquipmentRepository(EquipmentRepositoryPort):
    def __init__(self):
        self.equipment: Dict[str, Equipment] = {}

    def save_equipment(self, equipment: Equipment) -> None:
        self.equipment[equipment.equipment_id] = equipment

    def load_equipment(self, equipment_id: str) -> Optional[Equipment]:
        return self.equipment.get(equipment_id)

    def load_all_equipment(self) -> List[Equipment]:
        return list(self.equipment.values())

    def delete_equipment(self, equipment_id: str) -> None:
        if equipment_id in self.equipment:
            del self.equipment[equipment_id]


class InMemoryVendingMachineRepository(VendingMachineRepositoryPort):
    def __init__(self):
        self.machines: Dict[str, VendingMachine] = {}

    def save_machine(self, machine: VendingMachine) -> None:
        self.machines[machine.machine_id] = machine

    def load_machine(self, machine_id: str) -> Optional[VendingMachine]:
        return self.machines.get(machine_id)

    def load_all_machines(self) -> List[VendingMachine]:
        return list(self.machines.values())

    def delete_machine(self, machine_id: str) -> None:
        if machine_id in self.machines:
            del self.machines[machine_id]


class RepositoryFactory:
    @staticmethod
    def create_product_repository(
        repository_type: str = "memory",
    ) -> ProductRepositoryPort:
        if repository_type == "memory":
            return InMemoryProductRepository()
        if repository_type == "supabase":
            return SupabaseProductRepository()
        raise ValueError(f"Unbekannter Repository-Typ: {repository_type}")

    @staticmethod
    def create_movement_repository(
        repository_type: str = "memory",
    ) -> MovementRepositoryPort:
        if repository_type == "memory":
            return InMemoryMovementRepository()
        if repository_type == "supabase":
            return SupabaseMovementRepository()
        raise ValueError(f"Unbekannter Repository-Typ: {repository_type}")

    @staticmethod
    def create_member_repository(
        repository_type: str = "memory",
    ) -> MemberRepositoryPort:
        if repository_type == "memory":
            return InMemoryMemberRepository()
        if repository_type == "supabase":
            return SupabaseMemberRepository()
        raise ValueError(f"Unbekannter Repository-Typ: {repository_type}")

    @staticmethod
    def create_employee_repository(
        repository_type: str = "memory",
    ) -> EmployeeRepositoryPort:
        if repository_type == "memory":
            return InMemoryEmployeeRepository()
        if repository_type == "supabase":
            return SupabaseEmployeeRepository()
        raise ValueError(f"Unbekannter Repository-Typ: {repository_type}")

    @staticmethod
    def create_equipment_repository(
        repository_type: str = "memory",
    ) -> EquipmentRepositoryPort:
        if repository_type == "memory":
            return InMemoryEquipmentRepository()
        if repository_type == "supabase":
            return SupabaseEquipmentRepository()
        raise ValueError(f"Unbekannter Repository-Typ: {repository_type}")

    @staticmethod
    def create_vending_machine_repository(
        repository_type: str = "memory",
    ) -> VendingMachineRepositoryPort:
        if repository_type == "memory":
            return InMemoryVendingMachineRepository()
        if repository_type == "supabase":
            return SupabaseVendingMachineRepository()
        raise ValueError(f"Unbekannter Repository-Typ: {repository_type}")
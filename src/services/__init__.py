"""Services - Business Logic Layer"""

from datetime import datetime
from typing import List, Optional

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
from ..adapters.report import ConsoleReportAdapter


class FitnessCenterService:
    """Zentrale Business-Logic für das Fitnesscenter"""

    def __init__(
        self,
        product_repository: ProductRepositoryPort,
        movement_repository: MovementRepositoryPort,
        member_repository: MemberRepositoryPort,
        employee_repository: EmployeeRepositoryPort,
        equipment_repository: EquipmentRepositoryPort,
        vending_machine_repository: VendingMachineRepositoryPort,
        report_adapter: ConsoleReportAdapter
    ):
        self.product_repository = product_repository
        self.movement_repository = movement_repository
        self.member_repository = member_repository
        self.employee_repository = employee_repository
        self.equipment_repository = equipment_repository
        self.vending_machine_repository = vending_machine_repository
        self.report_adapter = report_adapter


    def create_member(
        self,
        member_id: str,
        first_name: str,
        last_name: str,
        email: str,
        phone: str = "",
        membership_type: str = "Standard",
    ) -> Member:
        existing_member = self.member_repository.load_member(member_id)
        if existing_member:
            raise ValueError(f"Mitglied mit ID {member_id} existiert bereits")

        member = Member(
            member_id=member_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            membership_type=membership_type,
        )

        self.member_repository.save_member(member)
        return member

    def get_member(self, member_id: str) -> Optional[Member]:
        return self.member_repository.load_member(member_id)

    def get_all_members(self) -> List[Member]:
        return self.member_repository.load_all_members()

    def update_member(
        self,
        member_id: str,
        first_name: str,
        last_name: str,
        email: str,
        phone: str = "",
        membership_type: str = "Standard",
    ) -> Member:
        member = self.member_repository.load_member(member_id)

        if not member:
            raise ValueError(f"Mitglied {member_id} nicht gefunden")

        member.first_name = first_name
        member.last_name = last_name
        member.email = email
        member.phone = phone
        member.membership_type = membership_type

        self.member_repository.save_member(member)
        return member

    def deactivate_member(self, member_id: str) -> None:
        member = self.member_repository.load_member(member_id)

        if not member:
            raise ValueError(f"Mitglied {member_id} nicht gefunden")

        member.deactivate()
        self.member_repository.save_member(member)

    def activate_member(self, member_id: str) -> None:
        member = self.member_repository.load_member(member_id)

        if not member:
            raise ValueError(f"Mitglied {member_id} nicht gefunden")

        member.activate()
        self.member_repository.save_member(member)

    def create_employee(
        self,
        employee_id: str,
        first_name: str,
        last_name: str,
        role: str,
        email: str,
        phone: str = "",
    ) -> Employee:
        existing_employee = self.employee_repository.load_employee(employee_id)
        if existing_employee:
            raise ValueError(f"Mitarbeiter mit ID {employee_id} existiert bereits")

        employee = Employee(
            employee_id=employee_id,
            first_name=first_name,
            last_name=last_name,
            role=role,
            email=email,
            phone=phone,
        )

        self.employee_repository.save_employee(employee)
        return employee

    def get_employee(self, employee_id: str) -> Optional[Employee]:
        return self.employee_repository.load_employee(employee_id)

    def get_all_employees(self) -> List[Employee]:
        return self.employee_repository.load_all_employees()
    
    def update_employee(
        self,
        employee_id: str,
        first_name: str,
        last_name: str,
        role: str,
        email: str,
        phone: str = "",
    ) -> Employee:
        employee = self.employee_repository.load_employee(employee_id)

        if not employee:
            raise ValueError(f"Mitarbeiter {employee_id} nicht gefunden")

        employee.first_name = first_name
        employee.last_name = last_name
        employee.role = role
        employee.email = email
        employee.phone = phone

        self.employee_repository.save_employee(employee)
        return employee

    def deactivate_employee(self, employee_id: str) -> None:
        employee = self.employee_repository.load_employee(employee_id)

        if not employee:
            raise ValueError(f"Mitarbeiter {employee_id} nicht gefunden")

        employee.deactivate()
        self.employee_repository.save_employee(employee)

    def activate_employee(self, employee_id: str) -> None:
        employee = self.employee_repository.load_employee(employee_id)

        if not employee:
            raise ValueError(f"Mitarbeiter {employee_id} nicht gefunden")

        employee.activate()
        self.employee_repository.save_employee(employee)

    def create_product(
        self,
        product_id: str,
        name: str,
        description: str,
        price: float,
        category: str = "",
        initial_quantity: int = 0,
        sku: str = "",
        notes: str | None = None,
    ) -> Product:
        existing_product = self.product_repository.load_product(product_id)
        if existing_product:
            raise ValueError(f"Produkt mit ID {product_id} existiert bereits")

        product = Product(
            id=product_id,
            name=name,
            description=description,
            price=price,
            quantity=initial_quantity,
            sku=sku,
            category=category,
            notes=notes,
        )

        self.product_repository.save_product(product)
        return product

    def get_product(self, product_id: str) -> Optional[Product]:
        return self.product_repository.load_product(product_id)

    def get_all_products(self) -> List[Product]:
        return self.product_repository.load_all_products()
    
    def update_product(
        self,
        product_id: str,
        name: str,
        description: str,
        price: float,
        category: str = "",
        sku: str = "",
        notes: str | None = None,
    ) -> Product:
        product = self.product_repository.load_product(product_id)

        if not product:
            raise ValueError(f"Produkt {product_id} nicht gefunden")

        product.name = name
        product.description = description
        product.price = price
        product.category = category
        product.sku = sku
        product.notes = notes

        self.product_repository.save_product(product)
        return product

    def delete_product(self, product_id: str) -> None:
        product = self.product_repository.load_product(product_id)

        if not product:
            raise ValueError(f"Produkt {product_id} nicht gefunden")

        self.product_repository.delete_product(product_id)

    def add_stock(
        self,
        product_id: str,
        quantity: int,
        reason: str = "",
        user: str = "system",
    ) -> None:
        if quantity <= 0:
            raise ValueError("Menge muss größer als 0 sein")

        product = self.product_repository.load_product(product_id)
        if not product:
            raise ValueError(f"Produkt {product_id} nicht gefunden")

        product.update_quantity(quantity)
        self.product_repository.save_product(product)

        movement = Movement(
            id=f"mov_{datetime.now().timestamp()}",
            product_id=product_id,
            product_name=product.name,
            quantity_change=quantity,
            movement_type="IN",
            reason=reason,
            performed_by=user,
        )

        self.movement_repository.save_movement(movement)

    def remove_stock(
        self,
        product_id: str,
        quantity: int,
        reason: str = "",
        user: str = "system",
    ) -> None:
        if quantity <= 0:
            raise ValueError("Menge muss größer als 0 sein")

        product = self.product_repository.load_product(product_id)
        if not product:
            raise ValueError(f"Produkt {product_id} nicht gefunden")

        if product.quantity < quantity:
            raise ValueError(
                f"Unzureichender Bestand. Verfügbar: {product.quantity}, Angefordert: {quantity}"
            )

        product.update_quantity(-quantity)
        self.product_repository.save_product(product)

        movement = Movement(
            id=f"mov_{datetime.now().timestamp()}",
            product_id=product_id,
            product_name=product.name,
            quantity_change=-quantity,
            movement_type="OUT",
            reason=reason,
            performed_by=user,
        )

        self.movement_repository.save_movement(movement)

    def get_movements(self) -> List[Movement]:
        return self.movement_repository.load_movements()

    def get_total_inventory_value(self) -> float:
        products = self.product_repository.load_all_products()
        return sum(product.get_total_value() for product in products)

    def create_equipment(
        self,
        equipment_id: str,
        name: str,
        equipment_type: str,
        location: str,
        status: str = "available",
        assigned_employee_id: str = "",
    ) -> Equipment:
        existing_equipment = self.equipment_repository.load_equipment(equipment_id)
        if existing_equipment:
            raise ValueError(f"Gerät mit ID {equipment_id} existiert bereits")

        if assigned_employee_id:
            employee = self.employee_repository.load_employee(assigned_employee_id)
            if not employee:
                raise ValueError(
                    f"Mitarbeiter {assigned_employee_id} für Gerätezuweisung nicht gefunden"
                )

        equipment = Equipment(
            equipment_id=equipment_id,
            name=name,
            equipment_type=equipment_type,
            location=location,
            status=status,
            assigned_employee_id=assigned_employee_id,
        )

        self.equipment_repository.save_equipment(equipment)
        return equipment

    def update_equipment_status(self, equipment_id: str, status: str) -> None:
        equipment = self.equipment_repository.load_equipment(equipment_id)

        if not equipment:
            raise ValueError(f"Gerät {equipment_id} nicht gefunden")

        equipment.set_status(status)
        self.equipment_repository.save_equipment(equipment)

    def assign_employee_to_equipment(self, equipment_id: str, employee_id: str) -> None:
        equipment = self.equipment_repository.load_equipment(equipment_id)
        if not equipment:
            raise ValueError(f"Gerät {equipment_id} nicht gefunden")

        employee = self.employee_repository.load_employee(employee_id)
        if not employee:
            raise ValueError(f"Mitarbeiter {employee_id} nicht gefunden")

        equipment.assign_employee(employee_id)
        self.equipment_repository.save_equipment(equipment)

    def get_equipment(self, equipment_id: str) -> Optional[Equipment]:
        return self.equipment_repository.load_equipment(equipment_id)

    def get_all_equipment(self) -> List[Equipment]:
        return self.equipment_repository.load_all_equipment()

    def create_machine(
        self,
        machine_id: str,
        location: str,
        machine_type: str,
        assigned_employee_id: str = "",
    ) -> VendingMachine:
        existing_machine = self.vending_machine_repository.load_machine(machine_id)
        if existing_machine:
            raise ValueError(f"Automat mit ID {machine_id} existiert bereits")

        if assigned_employee_id:
            employee = self.employee_repository.load_employee(assigned_employee_id)
            if not employee:
                raise ValueError(
                    f"Mitarbeiter {assigned_employee_id} für Automatenzuweisung nicht gefunden"
                )

        machine = VendingMachine(
            machine_id=machine_id,
            location=location,
            machine_type=machine_type,
            assigned_employee_id=assigned_employee_id,
        )

        self.vending_machine_repository.save_machine(machine)
        return machine

    def assign_employee_to_machine(self, machine_id: str, employee_id: str) -> None:
        machine = self.vending_machine_repository.load_machine(machine_id)
        if not machine:
            raise ValueError(f"Automat {machine_id} nicht gefunden")

        employee = self.employee_repository.load_employee(employee_id)
        if not employee:
            raise ValueError(f"Mitarbeiter {employee_id} nicht gefunden")

        machine.assign_employee(employee_id)
        self.vending_machine_repository.save_machine(machine)

    def deactivate_machine(self, machine_id: str) -> None:
        machine = self.vending_machine_repository.load_machine(machine_id)

        if not machine:
            raise ValueError(f"Automat {machine_id} nicht gefunden")

        machine.deactivate()
        self.vending_machine_repository.save_machine(machine)

    def activate_machine(self, machine_id: str) -> None:
        machine = self.vending_machine_repository.load_machine(machine_id)

        if not machine:
            raise ValueError(f"Automat {machine_id} nicht gefunden")

        machine.activate()
        self.vending_machine_repository.save_machine(machine)

    def get_machine(self, machine_id: str) -> Optional[VendingMachine]:
        return self.vending_machine_repository.load_machine(machine_id)

    def get_all_machines(self) -> List[VendingMachine]:
        return self.vending_machine_repository.load_all_machines()
    
    def generate_inventory_report(self) -> str:
        products = self.product_repository.load_all_products()
        movements = self.movement_repository.load_movements()

        # Daten an ReportAdapter übergeben
        self.report_adapter.products = {p.id: p for p in products}
        self.report_adapter.movements = movements

        return self.report_adapter.generate_inventory_report()
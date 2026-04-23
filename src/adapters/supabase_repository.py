"""Supabase Repository Adapter

Dieses Modul enthält die Implementierungen der Repository-Interfaces
für die Supabase-Datenbank. Es ermöglicht das Speichern und Laden
von Daten über die Supabase API.
"""


import os
from datetime import datetime
from typing import List, Optional

from dotenv import load_dotenv
from supabase import Client, create_client

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

load_dotenv()


def _create_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("SUPABASE_URL oder SUPABASE_KEY fehlen in der .env Datei")

    return create_client(url, key)


class SupabaseProductRepository(ProductRepositoryPort):
    def __init__(self):
        self.client = _create_supabase_client()

    def save_product(self, product: Product) -> None:
        data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "quantity": product.quantity,
            "sku": product.sku,
            "category": product.category,
            "created_at": product.created_at.isoformat(),
            "updated_at": product.updated_at.isoformat(),
            "notes": product.notes,
        }
        self.client.table("products").upsert(data).execute()

    def load_product(self, product_id: str) -> Optional[Product]:
        response = (
            self.client.table("products").select("*").eq("id", product_id).execute()
        )

        if not response.data:
            return None

        p = response.data[0]
        return Product(
            id=p["id"],
            name=p["name"],
            description=p["description"],
            price=p["price"],
            quantity=p["quantity"],
            sku=p.get("sku", ""),
            category=p.get("category", ""),
            created_at=datetime.fromisoformat(p["created_at"]),
            updated_at=datetime.fromisoformat(p["updated_at"]),
            notes=p.get("notes"),
        )

    def load_all_products(self) -> List[Product]:
        response = self.client.table("products").select("*").execute()

        products: List[Product] = []
        for p in response.data:
            products.append(
                Product(
                    id=p["id"],
                    name=p["name"],
                    description=p["description"],
                    price=p["price"],
                    quantity=p["quantity"],
                    sku=p.get("sku", ""),
                    category=p.get("category", ""),
                    created_at=datetime.fromisoformat(p["created_at"]),
                    updated_at=datetime.fromisoformat(p["updated_at"]),
                    notes=p.get("notes"),
                )
            )

        return products

    def delete_product(self, product_id: str) -> None:
        self.client.table("products").delete().eq("id", product_id).execute()


class SupabaseMovementRepository(MovementRepositoryPort):
    def __init__(self):
        self.client = _create_supabase_client()

    def save_movement(self, movement: Movement) -> None:
        data = {
            "id": movement.id,
            "product_id": movement.product_id,
            "product_name": movement.product_name,
            "quantity_change": movement.quantity_change,
            "movement_type": movement.movement_type,
            "reason": movement.reason,
            "timestamp": movement.timestamp.isoformat(),
            "performed_by": movement.performed_by,
        }
        self.client.table("movements").insert(data).execute()

    def load_movements(self) -> List[Movement]:
        response = self.client.table("movements").select("*").execute()

        movements: List[Movement] = []
        for m in response.data:
            movements.append(
                Movement(
                    id=m["id"],
                    product_id=m["product_id"],
                    product_name=m["product_name"],
                    quantity_change=m["quantity_change"],
                    movement_type=m["movement_type"],
                    reason=m.get("reason"),
                    timestamp=datetime.fromisoformat(m["timestamp"]),
                    performed_by=m["performed_by"],
                )
            )

        return movements


class SupabaseMemberRepository(MemberRepositoryPort):
    def __init__(self):
        self.client = _create_supabase_client()

    def save_member(self, member: Member) -> None:
        data = {
            "member_id": member.member_id,
            "first_name": member.first_name,
            "last_name": member.last_name,
            "email": member.email,
            "phone": member.phone,
            "membership_type": member.membership_type,
            "active": member.active,
            "created_at": member.created_at.isoformat(),
        }
        self.client.table("members").upsert(data).execute()

    def load_member(self, member_id: str) -> Optional[Member]:
        response = (
            self.client.table("members")
            .select("*")
            .eq("member_id", member_id)
            .execute()
        )

        if not response.data:
            return None

        m = response.data[0]
        return Member(
            member_id=m["member_id"],
            first_name=m["first_name"],
            last_name=m["last_name"],
            email=m["email"],
            phone=m.get("phone", ""),
            membership_type=m.get("membership_type", "Standard"),
            active=m.get("active", True),
            created_at=datetime.fromisoformat(m["created_at"]),
        )

    def load_all_members(self) -> List[Member]:
        response = self.client.table("members").select("*").execute()

        members: List[Member] = []
        for m in response.data:
            members.append(
                Member(
                    member_id=m["member_id"],
                    first_name=m["first_name"],
                    last_name=m["last_name"],
                    email=m["email"],
                    phone=m.get("phone", ""),
                    membership_type=m.get("membership_type", "Standard"),
                    active=m.get("active", True),
                    created_at=datetime.fromisoformat(m["created_at"]),
                )
            )

        return members

    def delete_member(self, member_id: str) -> None:
        self.client.table("members").delete().eq("member_id", member_id).execute()


class SupabaseEmployeeRepository(EmployeeRepositoryPort):
    def __init__(self):
        self.client = _create_supabase_client()

    def save_employee(self, employee: Employee) -> None:
        data = {
            "employee_id": employee.employee_id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "role": employee.role,
            "email": employee.email,
            "phone": employee.phone,
            "active": employee.active,
            "created_at": employee.created_at.isoformat(),
        }
        self.client.table("employees").upsert(data).execute()

    def load_employee(self, employee_id: str) -> Optional[Employee]:
        response = (
            self.client.table("employees")
            .select("*")
            .eq("employee_id", employee_id)
            .execute()
        )

        if not response.data:
            return None

        e = response.data[0]
        return Employee(
            employee_id=e["employee_id"],
            first_name=e["first_name"],
            last_name=e["last_name"],
            role=e["role"],
            email=e["email"],
            phone=e.get("phone", ""),
            active=e.get("active", True),
            created_at=datetime.fromisoformat(e["created_at"]),
        )

    def load_all_employees(self) -> List[Employee]:
        response = self.client.table("employees").select("*").execute()

        employees: List[Employee] = []
        for e in response.data:
            employees.append(
                Employee(
                    employee_id=e["employee_id"],
                    first_name=e["first_name"],
                    last_name=e["last_name"],
                    role=e["role"],
                    email=e["email"],
                    phone=e.get("phone", ""),
                    active=e.get("active", True),
                    created_at=datetime.fromisoformat(e["created_at"]),
                )
            )

        return employees

    def delete_employee(self, employee_id: str) -> None:
        self.client.table("employees").delete().eq("employee_id", employee_id).execute()


class SupabaseEquipmentRepository(EquipmentRepositoryPort):
    def __init__(self):
        self.client = _create_supabase_client()

    def save_equipment(self, equipment: Equipment) -> None:
        data = {
            "equipment_id": equipment.equipment_id,
            "name": equipment.name,
            "equipment_type": equipment.equipment_type,
            "location": equipment.location,
            "status": equipment.status,
            "assigned_employee_id": equipment.assigned_employee_id,
            "created_at": equipment.created_at.isoformat(),
        }
        self.client.table("equipment").upsert(data).execute()

    def load_equipment(self, equipment_id: str) -> Optional[Equipment]:
        response = (
            self.client.table("equipment")
            .select("*")
            .eq("equipment_id", equipment_id)
            .execute()
        )

        if not response.data:
            return None

        eq = response.data[0]
        return Equipment(
            equipment_id=eq["equipment_id"],
            name=eq["name"],
            equipment_type=eq["equipment_type"],
            location=eq["location"],
            status=eq.get("status", "available"),
            assigned_employee_id=eq.get("assigned_employee_id", ""),
            created_at=datetime.fromisoformat(eq["created_at"]),
        )

    def load_all_equipment(self) -> List[Equipment]:
        response = self.client.table("equipment").select("*").execute()

        equipment_list: List[Equipment] = []
        for eq in response.data:
            equipment_list.append(
                Equipment(
                    equipment_id=eq["equipment_id"],
                    name=eq["name"],
                    equipment_type=eq["equipment_type"],
                    location=eq["location"],
                    status=eq.get("status", "available"),
                    assigned_employee_id=eq.get("assigned_employee_id", ""),
                    created_at=datetime.fromisoformat(eq["created_at"]),
                )
            )

        return equipment_list

    def delete_equipment(self, equipment_id: str) -> None:
        self.client.table("equipment").delete().eq("equipment_id", equipment_id).execute()


class SupabaseVendingMachineRepository(VendingMachineRepositoryPort):
    def __init__(self):
        self.client = _create_supabase_client()

    def save_machine(self, machine: VendingMachine) -> None:
        data = {
            "machine_id": machine.machine_id,
            "location": machine.location,
            "machine_type": machine.machine_type,
            "assigned_employee_id": machine.assigned_employee_id,
            "active": machine.active,
            "created_at": machine.created_at.isoformat(),
        }
        self.client.table("vending_machines").upsert(data).execute()

    def load_machine(self, machine_id: str) -> Optional[VendingMachine]:
        response = (
            self.client.table("vending_machines")
            .select("*")
            .eq("machine_id", machine_id)
            .execute()
        )

        if not response.data:
            return None

        m = response.data[0]
        return VendingMachine(
            machine_id=m["machine_id"],
            location=m["location"],
            machine_type=m["machine_type"],
            assigned_employee_id=m.get("assigned_employee_id", ""),
            active=m.get("active", True),
            created_at=datetime.fromisoformat(m["created_at"]),
        )

    def load_all_machines(self) -> List[VendingMachine]:
        response = self.client.table("vending_machines").select("*").execute()

        machines: List[VendingMachine] = []
        for m in response.data:
            machines.append(
                VendingMachine(
                    machine_id=m["machine_id"],
                    location=m["location"],
                    machine_type=m["machine_type"],
                    assigned_employee_id=m.get("assigned_employee_id", ""),
                    active=m.get("active", True),
                    created_at=datetime.fromisoformat(m["created_at"]),
                )
            )

        return machines

    def delete_machine(self, machine_id: str) -> None:
        self.client.table("vending_machines").delete().eq("machine_id", machine_id).execute()
import os
from datetime import datetime
from typing import Dict, List, Optional

from dotenv import load_dotenv
from supabase import Client, create_client

from ..domain.member import Member
from ..domain.product import Product
from ..domain.warehouse import Movement
from ..ports import RepositoryPort

load_dotenv()


class SupabaseRepository(RepositoryPort):
    """Supabase Repository - speichert Daten in Supabase PostgreSQL"""

    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

        if not url or not key:
            raise ValueError("SUPABASE_URL oder SUPABASE_KEY fehlen in der .env Datei")

        self.client: Client = create_client(url, key)

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
        response = self.client.table("products").select("*").eq("id", product_id).execute()

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

    def load_all_products(self) -> Dict[str, Product]:
        response = self.client.table("products").select("*").execute()

        products: Dict[str, Product] = {}

        for p in response.data:
            product = Product(
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
            products[product.id] = product

        return products

    def delete_product(self, product_id: str) -> None:
        self.client.table("products").delete().eq("id", product_id).execute()

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
            movement = Movement(
                id=m["id"],
                product_id=m["product_id"],
                product_name=m["product_name"],
                quantity_change=m["quantity_change"],
                movement_type=m["movement_type"],
                reason=m.get("reason"),
                timestamp=datetime.fromisoformat(m["timestamp"]),
                performed_by=m["performed_by"],
            )
            movements.append(movement)

        return movements

    def save_member(self, member: Member) -> None:
        data = {
            "id": member.id,
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
        response = self.client.table("members").select("*").eq("id", member_id).execute()

        if not response.data:
            return None

        m = response.data[0]

        return Member(
            id=m["id"],
            first_name=m["first_name"],
            last_name=m["last_name"],
            email=m["email"],
            phone=m.get("phone", ""),
            membership_type=m.get("membership_type", "Standard"),
            active=m.get("active", True),
            created_at=datetime.fromisoformat(m["created_at"]),
        )

    def load_all_members(self) -> Dict[str, Member]:
        response = self.client.table("members").select("*").execute()

        members: Dict[str, Member] = {}

        for m in response.data:
            member = Member(
                id=m["id"],
                first_name=m["first_name"],
                last_name=m["last_name"],
                email=m["email"],
                phone=m.get("phone", ""),
                membership_type=m.get("membership_type", "Standard"),
                active=m.get("active", True),
                created_at=datetime.fromisoformat(m["created_at"]),
            )
            members[member.id] = member

        return members

    def delete_member(self, member_id: str) -> None:
        self.client.table("members").delete().eq("id", member_id).execute()
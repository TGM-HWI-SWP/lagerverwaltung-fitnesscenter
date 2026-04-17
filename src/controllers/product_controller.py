from typing import Any


def create_product(service: Any, data: dict[str, Any]):
    return service.create_product(
        data["product_id"],
        data["name"],
        data["description"],
        data["price"],
        data.get("category", ""),
        data.get("initial_quantity", 0),
        data.get("sku", ""),
        data.get("notes"),
    )


def get_product(service: Any, product_id: str):
    return service.get_product(product_id)


def get_all_products(service: Any):
    return service.get_all_products()


def add_stock(
    service: Any,
    product_id: str,
    quantity: int,
    reason: str = "",
    user: str = "system",
):
    return service.add_stock(product_id, quantity, reason, user)


def remove_stock(
    service: Any,
    product_id: str,
    quantity: int,
    reason: str = "",
    user: str = "system",
):
    return service.remove_stock(product_id, quantity, reason, user)


def update_product(service: Any, product_id: str, data: dict[str, Any]):
    return service.update_product(
        product_id,
        name=data["name"],
        description=data["description"],
        price=data["price"],
        category=data.get("category", ""),
        sku=data.get("sku", ""),
        notes=data.get("notes"),
    )


def delete_product(service: Any, product_id: str):
    return service.delete_product(product_id)
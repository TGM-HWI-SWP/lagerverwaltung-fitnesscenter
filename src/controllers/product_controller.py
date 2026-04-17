def create_product(service, data):
    return service.create_product(
        data["product_id"],
        data["name"],
        data["description"],
        data["price"],
        data.get("category", ""),
        data.get("initial_quantity", 0),
        data.get("sku", ""),
        data.get("notes")
    )


def get_product(service, product_id):
    return service.get_product(product_id)


def get_all_products(service):
    return service.get_all_products()


def add_stock(service, product_id, quantity, reason="", user="system"):
    return service.add_stock(product_id, quantity, reason, user)


def remove_stock(service, product_id, quantity, reason="", user="system"):
    return service.remove_stock(product_id, quantity, reason, user)
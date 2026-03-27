def create_product(service, data):
    return service.create_product(
        data["product_id"],
        data["name"],
        data["description"],
        data["price"],
        data["quantity"],
        data["category"]
    )


def get_product(service, product_id):
    return service.get_product(product_id)


def get_all_products(service):
    return service.get_all_products()


def add_stock(service, product_id, quantity, performed_by):
    return service.add_stock(product_id, quantity, performed_by)


def remove_stock(service, product_id, quantity, performed_by):
    return service.remove_stock(product_id, quantity, performed_by)


def delete_product(service, product_id):
    return service.delete_product(product_id)
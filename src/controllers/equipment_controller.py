def create_equipment(service, data):
    return service.create_equipment(
        data["equipment_id"],
        data["name"],
        data["equipment_type"],
        data["location"],
        data.get("status", "available")
    )


def get_equipment(service, equipment_id):
    return service.get_equipment(equipment_id)


def get_all_equipment(service):
    return service.get_all_equipment()


def update_equipment_status(service, equipment_id, status):
    return service.update_equipment_status(equipment_id, status)


def assign_employee_to_equipment(service, equipment_id, employee_id):
    return service.assign_employee_to_equipment(equipment_id, employee_id)


def delete_equipment(service, equipment_id):
    return service.delete_equipment(equipment_id)
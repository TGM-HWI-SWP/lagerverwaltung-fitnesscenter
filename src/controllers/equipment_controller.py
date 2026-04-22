from typing import Any


def create_equipment(service: Any, data: dict[str, Any]):
    return service.create_equipment(
        data["equipment_id"],
        data["name"],
        data["equipment_type"],
        data["location"],
        data.get("status", "available"),
        data.get("assigned_employee_id", ""),
    )


def get_equipment(service: Any, equipment_id: str):
    return service.get_equipment(equipment_id)


def get_all_equipment(service: Any):
    return service.get_all_equipment()


def update_equipment_status(service: Any, equipment_id: str, status: str):
    return service.update_equipment_status(equipment_id, status)


def assign_employee_to_equipment(service: Any, equipment_id: str, employee_id: str):
    return service.assign_employee_to_equipment(equipment_id, employee_id)


def delete_equipment(service: Any, equipment_id: str):
    return service.delete_equipment(equipment_id)
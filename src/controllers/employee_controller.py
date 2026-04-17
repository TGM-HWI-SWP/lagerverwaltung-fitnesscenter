from typing import Any


def create_employee(service: Any, data: dict[str, Any]):
    return service.create_employee(
        data["employee_id"],
        data["first_name"],
        data["last_name"],
        data["role"],
        data["email"],
        data.get("phone", ""),
    )


def get_employee(service: Any, employee_id: str):
    return service.get_employee(employee_id)


def get_all_employees(service: Any):
    return service.get_all_employees()


def activate_employee(service: Any, employee_id: str):
    return service.activate_employee(employee_id)


def deactivate_employee(service: Any, employee_id: str):
    return service.deactivate_employee(employee_id)


def update_employee(service: Any, employee_id: str, data: dict[str, Any]):
    return service.update_employee(
        employee_id,
        first_name=data["first_name"],
        last_name=data["last_name"],
        role=data["role"],
        email=data["email"],
        phone=data.get("phone", ""),
    )
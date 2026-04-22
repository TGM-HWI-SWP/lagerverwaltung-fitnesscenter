from typing import Any


def create_machine(service: Any, data: dict[str, Any]):
    return service.create_machine(
        data["machine_id"],
        data["location"],
        data["machine_type"],
        data.get("assigned_employee_id", ""),
    )


def get_machine(service: Any, machine_id: str):
    return service.get_machine(machine_id)


def get_all_machines(service: Any):
    return service.get_all_machines()


def assign_employee_to_machine(service: Any, machine_id: str, employee_id: str):
    return service.assign_employee_to_machine(machine_id, employee_id)


def activate_machine(service: Any, machine_id: str):
    return service.activate_machine(machine_id)


def deactivate_machine(service: Any, machine_id: str):
    return service.deactivate_machine(machine_id)


def delete_machine(service: Any, machine_id: str):
    return service.delete_machine(machine_id)
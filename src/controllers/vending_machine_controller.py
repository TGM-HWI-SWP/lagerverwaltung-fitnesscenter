def create_machine(service, data):
    return service.create_machine(
        data["machine_id"],
        data["location"],
        data["machine_type"]
    )


def get_machine(service, machine_id):
    return service.get_machine(machine_id)


def get_all_machines(service):
    return service.get_all_machines()


def assign_employee_to_machine(service, machine_id, employee_id):
    return service.assign_employee_to_machine(machine_id, employee_id)


def activate_machine(service, machine_id):
    return service.activate_machine(machine_id)


def deactivate_machine(service, machine_id):
    return service.deactivate_machine(machine_id)


def delete_machine(service, machine_id):
    return service.delete_machine(machine_id)
def create_employee(service, data):
    return service.create_employee(
        data["employee_id"],
        data["first_name"],
        data["last_name"],
        data["role"],
        data["email"],
        data.get("phone", "")
    )


def get_employee(service, employee_id):
    return service.get_employee(employee_id)


def get_all_employees(service):
    return service.get_all_employees()


def activate_employee(service, employee_id):
    return service.activate_employee(employee_id)


def deactivate_employee(service, employee_id):
    return service.deactivate_employee(employee_id)
def create_member(service, data):
    return service.create_member(
        data["member_id"],
        data["first_name"],
        data["last_name"],
        data["email"],
        data.get("phone", ""),
        data.get("membership_type", "Standard")
    )


def get_member(service, member_id):
    return service.get_member(member_id)


def get_all_members(service):
    return service.get_all_members()


def activate_member(service, member_id):
    return service.activate_member(member_id)


def deactivate_member(service, member_id):
    return service.deactivate_member(member_id)
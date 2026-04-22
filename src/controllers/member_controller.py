from typing import Any


def create_member(service: Any, data: dict[str, Any]):
    return service.create_member(
        data["member_id"],
        data["first_name"],
        data["last_name"],
        data["email"],
        data.get("phone", ""),
        data.get("membership_type", "Standard"),
    )


def get_member(service: Any, member_id: str):
    return service.get_member(member_id)


def get_all_members(service: Any):
    return service.get_all_members()


def activate_member(service: Any, member_id: str):
    return service.activate_member(member_id)


def deactivate_member(service: Any, member_id: str):
    return service.deactivate_member(member_id)


def update_member(service: Any, member_id: str, data: dict[str, Any]):
    return service.update_member(
        member_id,
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        phone=data.get("phone", ""),
        membership_type=data.get("membership_type", "Standard"),
    )
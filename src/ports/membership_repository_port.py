from typing import Protocol, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.membership import Membership


class MembershipRepositoryPort(Protocol):
    def save_membership(self, membership: "Membership") -> None:
        ...

    def load_membership(self, membership_id: str) -> Optional["Membership"]:
        ...

    def load_all_memberships(self) -> list["Membership"]:
        ...

    def delete_membership(self, membership_id: str) -> None:
        ...
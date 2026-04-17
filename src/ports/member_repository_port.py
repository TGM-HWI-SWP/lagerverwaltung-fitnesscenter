from typing import Protocol, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.member import Member


class MemberRepositoryPort(Protocol):
    def save_member(self, member: "Member") -> None:
        ...

    def load_member(self, member_id: str) -> Optional["Member"]:
        ...

    def load_all_members(self) -> list["Member"]:
        ...

    def delete_member(self, member_id: str) -> None:
        ...
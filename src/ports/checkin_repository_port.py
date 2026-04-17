from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.checkin import CheckIn


class CheckInRepositoryPort(Protocol):
    def save_checkin(self, checkin: "CheckIn") -> None:
        ...

    def load_all_checkins(self) -> list["CheckIn"]:
        ...

    def load_checkins_by_member(self, member_id: str) -> list["CheckIn"]:
        ...
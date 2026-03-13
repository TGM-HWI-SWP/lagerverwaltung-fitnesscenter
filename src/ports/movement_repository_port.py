from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.warehouse import Movement


class MovementRepositoryPort(Protocol):

    def save_movement(self, movement: "Movement") -> None:
        ...

    def load_movements(self) -> list["Movement"]:
        ...
from typing import Protocol, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.equipment import Equipment


class EquipmentRepositoryPort(Protocol):

    def save_equipment(self, equipment: "Equipment") -> None:
        ...

    def load_equipment(self, equipment_id: str) -> Optional["Equipment"]:
        ...

    def load_all_equipment(self) -> list["Equipment"]:
        ...

    def delete_equipment(self, equipment_id: str) -> None:
        ...
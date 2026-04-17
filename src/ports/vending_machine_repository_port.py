from typing import Protocol, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.vending_machine import VendingMachine


class VendingMachineRepositoryPort(Protocol):

    def save_machine(self, machine: "VendingMachine") -> None:
        ...

    def load_machine(self, machine_id: str) -> Optional["VendingMachine"]:
        ...

    def load_all_machines(self) -> list["VendingMachine"]:
        ...

    def delete_machine(self, machine_id: str) -> None:
        ...
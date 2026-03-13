from typing import Protocol, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.employee import Employee


class EmployeeRepositoryPort(Protocol):

    def save_employee(self, employee: "Employee") -> None:
        ...

    def load_employee(self, employee_id: str) -> Optional["Employee"]:
        ...

    def load_all_employees(self) -> list["Employee"]:
        ...

    def delete_employee(self, employee_id: str) -> None:
        ...
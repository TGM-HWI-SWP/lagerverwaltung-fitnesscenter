from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class VendingMachine:
    """Domain-Modell für einen Snack- oder Getränkeautomaten"""

    machine_id: str
    location: str
    machine_type: str
    assigned_employee_id: str = ""
    active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if not self.machine_id:
            raise ValueError("Machine ID kann nicht leer sein")
        if not self.location.strip():
            raise ValueError("Standort kann nicht leer sein")
        if not self.machine_type.strip():
            raise ValueError("Automatentyp kann nicht leer sein")

    def deactivate(self) -> None:
        """Automaten deaktivieren"""
        self.active = False

    def activate(self) -> None:
        """Automaten aktivieren"""
        self.active = True

    def assign_employee(self, employee_id: str) -> None:
        """Mitarbeiter einem Automaten zuweisen"""
        if not employee_id.strip():
            raise ValueError("Employee ID kann nicht leer sein")
        self.assigned_employee_id = employee_id
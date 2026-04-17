from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Equipment:
    """Domain-Modell für ein Fitnessgerät"""

    equipment_id: str
    name: str
    equipment_type: str
    location: str
    status: str = "available"
    assigned_employee_id: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if not self.equipment_id:
            raise ValueError("Equipment ID kann nicht leer sein")
        if not self.name.strip():
            raise ValueError("Name kann nicht leer sein")
        if not self.equipment_type.strip():
            raise ValueError("Gerätetyp kann nicht leer sein")
        if not self.location.strip():
            raise ValueError("Standort kann nicht leer sein")
        if not self.status.strip():
            raise ValueError("Status kann nicht leer sein")

    def set_status(self, status: str) -> None:
        """Status des Geräts setzen"""
        if not status.strip():
            raise ValueError("Status kann nicht leer sein")
        self.status = status

    def assign_employee(self, employee_id: str) -> None:
        """Mitarbeiter dem Gerät zuweisen"""
        if not employee_id.strip():
            raise ValueError("Employee ID kann nicht leer sein")
        self.assigned_employee_id = employee_id
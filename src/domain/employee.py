from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Employee:
    """Domain-Modell für einen Mitarbeiter des Fitnesscenters"""

    employee_id: str
    first_name: str
    last_name: str
    role: str
    email: str
    phone: str = ""
    active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        if not self.employee_id:
            raise ValueError("Employee ID kann nicht leer sein")
        if not self.first_name.strip():
            raise ValueError("Vorname kann nicht leer sein")
        if not self.last_name.strip():
            raise ValueError("Nachname kann nicht leer sein")
        if not self.role.strip():
            raise ValueError("Rolle kann nicht leer sein")
        if not self.email.strip():
            raise ValueError("E-Mail kann nicht leer sein")

    def deactivate(self) -> None:
        """Mitarbeiter deaktivieren"""
        self.active = False

    def activate(self) -> None:
        """Mitarbeiter aktivieren"""
        self.active = True

    def full_name(self) -> str:
        """Vollständigen Namen zurückgeben"""
        return f"{self.first_name} {self.last_name}"
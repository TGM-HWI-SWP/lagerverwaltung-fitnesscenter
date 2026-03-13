from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Member:
    """Domain-Modell für ein Fitnesscenter-Mitglied"""

    id: str
    first_name: str
    last_name: str
    email: str
    phone: str = ""
    membership_type: str = "Standard"
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.id:
            raise ValueError("Member ID kann nicht leer sein")
        if not self.first_name.strip():
            raise ValueError("Vorname kann nicht leer sein")
        if not self.last_name.strip():
            raise ValueError("Nachname kann nicht leer sein")
        if not self.email.strip():
            raise ValueError("E-Mail kann nicht leer sein")

    def deactivate(self) -> None:
        """Mitglied deaktivieren"""
        self.active = False

    def activate(self) -> None:
        """Mitglied aktivieren"""
        self.active = True

    def full_name(self) -> str:
        """Vollständigen Namen zurückgeben"""
        return f"{self.first_name} {self.last_name}"
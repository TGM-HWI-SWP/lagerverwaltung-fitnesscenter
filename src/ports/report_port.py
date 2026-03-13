from typing import Protocol


class ReportPort(Protocol):
    def generate_member_overview(self) -> list[dict]:
        ...
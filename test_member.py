"""Member Test - Verwaltung von Mitgliedern mit Supabase

Dieses Script dient als Demo und Test für die Member-Funktionalität
im FitnessCenterSystem unter Verwendung der Supabase-Datenbank.

Ablauf:
- Verbindung zur Supabase-Datenbank herstellen
- Ein neues Mitglied erstellen
- Alle Mitglieder abrufen und anzeigen
- Ein Mitglied deaktivieren
- Den aktualisierten Status erneut abrufen
"""

from src.adapters.repository import RepositoryFactory
from src.adapters.report import ConsoleReportAdapter
from src.services import FitnessCenterService


def main():
    """Führt den Member-Test mit Supabase durch.

    Initialisiert alle benötigten Repositories, erstellt ein Testmitglied,
    zeigt alle Mitglieder an und überprüft die Aktivierungslogik.
    """

    # Supabase Repositories
    product_repo = RepositoryFactory.create_product_repository("supabase")
    movement_repo = RepositoryFactory.create_movement_repository("supabase")
    member_repo = RepositoryFactory.create_member_repository("supabase")
    employee_repo = RepositoryFactory.create_employee_repository("supabase")
    equipment_repo = RepositoryFactory.create_equipment_repository("supabase")
    machine_repo = RepositoryFactory.create_vending_machine_repository("supabase")

    # Report Adapter
    report_adapter = ConsoleReportAdapter()

    # Service
    service = FitnessCenterService(
        product_repository=product_repo,
        movement_repository=movement_repo,
        member_repository=member_repo,
        employee_repository=employee_repo,
        equipment_repository=equipment_repo,
        vending_machine_repository=machine_repo,
        report_adapter=report_adapter,
    )

    # 1. Member erstellen
    service.create_member("M0027", "Dwayne", "Johnson", "dwayne@test.com")

    # 2. Alle Members laden
    members = service.get_all_members()

    print("Members:")
    for m in members:
        print(f"{m.first_name} {m.last_name} - {'Aktiv' if m.active else 'Inaktiv'}")

    # 3. Member deaktivieren
    service.deactivate_member("M0027")

    # 4. Wieder laden
    member = service.get_member("M0027")
    print("Status nach Deaktivierung:", "Aktiv" if member.active else "Inaktiv")


if __name__ == "__main__":
    main()
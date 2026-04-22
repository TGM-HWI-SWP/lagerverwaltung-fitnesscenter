from src.adapters.repository import RepositoryFactory
from src.adapters.report import ConsoleReportAdapter
from src.services import FitnessCenterService


def main():
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

    # REPORT A aus Supabase
    report = service.generate_inventory_report()
    print(report)


if __name__ == "__main__":
    main()
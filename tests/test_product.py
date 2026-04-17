from src.services import FitnessCenterService
from src.adapters.repository import InMemoryRepository
from src.adapters.report import ConsoleReportAdapter


def create_service():
    repo = InMemoryRepository()
    return FitnessCenterService(repo, repo, repo, repo, repo, repo, ConsoleReportAdapter())


def test_create_product():
    service = create_service()

    service.create_product("p1", "Protein", "Drink", 5.0)

    product = service.get_product("p1")

    assert product is not None
    assert product.name == "Protein"
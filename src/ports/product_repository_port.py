from typing import Protocol, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.product import Product


class ProductRepositoryPort(Protocol):

    def save_product(self, product: "Product") -> None:
        ...

    def load_product(self, product_id: str) -> Optional["Product"]:
        ...

    def load_all_products(self) -> list["Product"]:
        ...

    def delete_product(self, product_id: str) -> None:
        ...
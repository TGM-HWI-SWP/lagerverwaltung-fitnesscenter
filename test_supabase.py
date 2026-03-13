from src.adapters.supabase_repository import SupabaseRepository
from src.domain.product import Product


repo = SupabaseRepository()

product = Product(
    id="FIT001",
    name="Proteinriegel",
    description="Eiweißriegel für den Verkauf im Fitnesscenter",
    price=2.5,
    quantity=20,
    category="Snacks"
)

repo.save_product(product)

print("Produkt gespeichert!")

loaded_product = repo.load_product("FIT001")

print("Geladenes Produkt:")
print(loaded_product)
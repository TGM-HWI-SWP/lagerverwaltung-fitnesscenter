"""Supabase Test - Produkt speichern und laden

Dieses Script dient als einfacher Test für die Supabase-Anbindung.
Es überprüft, ob ein Produkt erfolgreich in der Datenbank gespeichert
und anschließend wieder geladen werden kann.

Ablauf:
- Verbindung zum Supabase Product Repository herstellen
- Produkt erstellen und speichern
- Produkt aus der Datenbank laden
- Ausgabe des geladenen Produkts
"""

from src.adapters.repository import RepositoryFactory
from src.domain.product import Product


def main():
    """Führt den Supabase-Test für Produkte aus.

    Erstellt ein neues Produkt, speichert es in der Supabase-Datenbank
    und lädt es anschließend wieder, um die Funktionalität zu überprüfen.
    """

    # Supabase Product Repository holen
    repo = RepositoryFactory.create_product_repository("supabase")

    # Neues Produkt erstellen
    product = Product(
        id="FIT999",
        name="Cold Brew Protein Coffee",
        description="Proteinreicher Eiskaffee für vor dem Training",
        price=4.49,
        quantity=25,
        category="Drink"
    )

    # Speichern
    repo.save_product(product)
    print("Produkt gespeichert!")

    # Laden
    loaded_product = repo.load_product("FIT999")

    print("Geladenes Produkt:")
    print(loaded_product)


if __name__ == "__main__":
    main()
from src.adapters.repository import RepositoryFactory
from src.services import WarehouseService

# Supabase Repository verwenden
repository = RepositoryFactory.create_repository("supabase")

service = WarehouseService(repository)

# 1. Member erstellen
service.create_member("M001", "Max", "Mustermann", "max@test.com")

# 2. Alle Members laden
members = service.get_all_members()

print("Members:")
for m in members.values():
    print(m.full_name(), "-", "Aktiv" if m.active else "Inaktiv")

# 3. Member deaktivieren
service.deactivate_member("M001")

# 4. Wieder laden
member = service.get_member("M001")
print("Status nach Deaktivierung:", "Aktiv" if member.active else "Inaktiv")
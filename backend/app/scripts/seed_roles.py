from sqlalchemy import text

from app.database.database import SessionLocal
from app.roles.models import Role
from app.users.models import User  # noqa: F401

db = SessionLocal()

db.execute(
    text(
        "SELECT setval('roles_id_seq', COALESCE((SELECT MAX(id) FROM roles), 1), true)"
    )
)

roles = [
    "Administrator",
    "Manager",
    "Agent",
    "Billing",
    "Support",
    "Sales",
]

for role_name in roles:
    exists = (
        db.query(Role)
        .filter(Role.name == role_name)
        .first()
    )
    if not exists:
        db.add(Role(name=role_name))

db.commit()
db.close()
print("Roles creados exitosamente")
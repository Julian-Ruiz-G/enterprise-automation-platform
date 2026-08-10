from app.database.database import SessionLocal
from app.roles.models import Role

db = SessionLocal()

roles = [
    "Administrator",
    "Manager",
    "Agent"
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
from sqlalchemy.orm import Session

from app.users.models import User
from app.roles.models import Role

CATEGORY_TO_ROLE = {
    "BILLING": "Facturación",
    "SUPPORT": "Soporte",
    "SALES": "Ventas",
    "Facturación": "Facturación",
    "Soporte": "Soporte",
    "Ventas": "Ventas",
}

def assign_user(
    db: Session,
    category: str,
):
    role_name = CATEGORY_TO_ROLE.get(category)
    if not role_name:
        return None
    return (
        db.query(User)
        .join(Role)
        .filter(
            Role.name == role_name,
            User.is_active.is_(True),
            )
        .first()
    )
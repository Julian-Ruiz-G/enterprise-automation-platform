from sqlalchemy.orm import Session

from app.users.models import User


def assign_user(
    db: Session,
    category: str,
):
    if category == "Facturación":
        return (
            db.query(User)
            .filter(User.role_id == 4)
            .first()
        )

    if category == "Soporte":
        return (
            db.query(User)
            .filter(User.role_id == 5)
            .first()
        )

    if category == "Ventas":
        return (
            db.query(User)
            .filter(User.role_id == 6)
            .first()
        )

    return None
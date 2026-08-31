from app.users import crud
from sqlalchemy.orm import Session
from app.security.auth import (
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_token,
)
def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = crud.get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    token = create_access_token(
        {
            "sub": user.email,
            "role_id": user.role_id
        }
    )

    claims = {
        "sub": user.email,
        "role_id": user.role_id,
    }
    return {
        "access_token": create_access_token(claims),
        "refresh_token": create_refresh_token(claims),
        "token_type": "bearer",
    }

def refresh_access_token(db: Session, refresh_token: str) -> dict | None:
    payload = verify_token(refresh_token)
    if payload is None or payload.get("type") != "refresh":
        return None
    email = payload.get("sub")
    if not email:
        return None
    user = crud.get_user_by_email(db, email)
    if not user or not user.is_active:
        return None
    claims = {
        "sub": user.email,
        "role_id": user.role_id,
    }
    return {
        "access_token": create_access_token(claims),
        "refresh_token": create_refresh_token(claims),
        "token_type": "bearer",
    }
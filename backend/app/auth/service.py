from app.users import crud
from app.security.auth import create_access_token
from sqlalchemy.orm import Session
from app.security.auth import (
    verify_password
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

    return token


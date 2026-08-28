from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.users.models import User
from app.users import crud
from app.security.auth import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    email = payload.get("sub")

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    user = crud.get_user_by_email(db, email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    return user


def current_active_user(
    current_user: User = Depends(get_current_user)
):

    if not current_user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Usuario inactivo"
        )

    return current_user


def require_role(role_id: int):

    print("REQUIRE ROLE CREADO:", role_id)

    def role_checker(
        current_user: User = Depends(current_active_user)
    ):

        print("Usuario:", current_user.username)
        print("Role usuario:", current_user.role_id)
        print("Role requerido:", role_id)

        if current_user.role_id != role_id:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos"
            )

        return current_user

    return role_checker


def require_role_name(*allowed: str):
    def rol_checker(
        current_user: User = Depends(current_active_user),
    ):
        role_name = current_user.role.name if current_user.role else None 
        if role_name not in allowed: 
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos"
            )
        return current_user
    return rol_checker
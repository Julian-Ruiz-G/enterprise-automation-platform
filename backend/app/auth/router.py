from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.schemas import Token
from app.auth.service import authenticate_user
from app.database.database import get_db
from sqlalchemy.orm import Session
from app.security.dependencies import get_current_user
from fastapi import HTTPException

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.get("/me")
def get_me(
    current_user = Depends(get_current_user)
):
    return current_user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    token = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
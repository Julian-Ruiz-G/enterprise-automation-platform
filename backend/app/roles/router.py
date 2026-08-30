from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.roles.schemas import RoleResponse
from app.roles.service import list_roles
from app.security.dependencies import get_current_user

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("", response_model=list[RoleResponse])
def get_roles(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return list_roles(db)   
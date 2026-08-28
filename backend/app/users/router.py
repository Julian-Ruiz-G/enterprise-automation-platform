from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.users.schemas import (
    UserCreate,
    UserUpdate,
    UserResponse
)

from app.users.service import (
    register_user,
    get_user,
    list_users,
    update_user,
    delete_user
)

from app.security.dependencies import (
    get_current_user, 
    require_role_name,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post(
    "",
    response_model=UserResponse
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role_name('Administrador')),
):

    created = register_user(
        db,
        user,
        current_user
    )

    if created is None:
        raise HTTPException(
            status_code=400,
            detail="El cliente ya existe"
        )

    return created

@router.get(
    "",
    response_model=list[UserResponse]
)
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return list_users(
        db,
        skip,
        limit
    )

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_one_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    user = get_user(
        db,
        user_id
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user

@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def edit_user(
    user_id: int,
    updates: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    user = update_user(
        db,
        user_id,
        updates,
        current_user
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user

@router.delete(
    "/{user_id}"
)
def remove_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role_name('Administrador')),
):

    user = delete_user(
        db,
        user_id,
        current_user
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return {
        "message": "Usuario eliminado correctamente"
    }
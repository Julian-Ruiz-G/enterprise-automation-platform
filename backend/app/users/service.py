from sqlalchemy.orm import Session
from app.audit.service import register_log
from app.users import crud
from app.users.models import User
from app.security.auth import hash_password
from app.users.schemas import (
    UserCreate,
    UserUpdate
)


def register_user(
    db: Session,
    user: UserCreate,
    current_user
):

    existing = crud.get_user_by_email(
        db,
        user.email
    )

    if existing:
        return None
    old_values = {
        "username": None,
        "email": None,
        "hashed_password": None,
        "is_active": None,
        "role_id": None
    }
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        role_id=user.role_id,
        is_active=True        
    )

    created = crud.create_user(
        db,
        db_user
    )

    register_log(
    db=db,
    table_name="users",
    record_id=created.id,
    action="CREATE",
    user_id=current_user.id,
    old_values=old_values,
    new_values={
        "username": created.username,
        "email": created.email,
        "hashed_password": created.hashed_password,
        "is_active": created.is_active,
        "role_id": created.role_id
    }
    )

    return created




def list_users(
    db: Session,
    skip: int = 0,
    limit: int = 100
):

    return crud.get_users(
        db,
        skip,
        limit
    )


def get_user(
    db: Session,
    user_id: int
):

    return crud.get_user(
        db,
        user_id
    )


def update_user(
    db: Session,
    user_id: int,
    updates: UserUpdate,
    current_user
):

    user = crud.get_user(
        db,
        user_id
    )

    if not user:
        return None
    old_values = {
        "username": user.username,
        "email": user.email,
        "hashed_password": user.hashed_password,
        "is_active": user.is_active,
        "role_id": user.role_id
    }
    data = updates.model_dump(
        exclude_unset=True
    )

    for key, value in data.items():
        setattr(user, key, value)

    updated = crud.update_user(
        db,
        user
    )

    register_log(
        db=db,
        table_name="users",
        record_id=updated.id,
        action="UPDATE",
        user_id=current_user.id,
        old_values=old_values,
        new_values={
            "username": updated.username,
            "email": updated.email,
            "hashed_password": updated.hashed_password,
            "is_active": updated.is_active,
            "role_id": updated.role_id
        }
    )

    return updated


def delete_user(
    db: Session,
    user_id: int,
    current_user
):

    user = crud.get_user(
        db,
        user_id
    )

    if not user:
        return None
    
    old_values = {
        "username": user.username,
        "email": user.email,
        "hashed_password": user.hashed_password,
        "is_active": user.is_active,
        "role_id": user.role_id
    }

    crud.delete_user(
        db,
        user
    )

    register_log(
        db=db,
        table_name="users",
        record_id=user.id,
        action="DELETE",
        user_id=current_user.id,
        old_values=old_values,
        new_values={}
    )

    return user
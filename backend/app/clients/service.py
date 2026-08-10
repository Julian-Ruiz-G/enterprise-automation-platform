from sqlalchemy.orm import Session
from app.audit.service import register_log
from app.clients import crud
from app.clients.models import Client
from app.clients.schemas import (
    ClientCreate,
    ClientUpdate
)


def register_client(
    db,
    client,
    current_user
):
    existing = crud.get_client_by_email(
        db,
        client.email
    )
    if existing:
        return None
    db_client = Client(

        company_name=client.company_name,
        contact_name=client.contact_name,
        email=client.email,
        phone=client.phone,
        address=client.address,
        city=client.city,
        country=client.country

    )

    created = crud.create_client(
        db,
        db_client
    )

    register_log(

        db=db,

        table_name="clients",

        record_id=created.id,

        action="CREATE",

        user_id=current_user.id,

        new_values={
            "company_name": created.company_name,
            "contact_name": created.contact_name,
            "email": created.email
        }

    )

    return created

def list_clients(
    db: Session,
    skip: int = 0,
    limit: int = 100
):

    return crud.get_clients(
        db,
        skip,
        limit
    )


def get_client(
    db: Session,
    client_id: int
):

    return crud.get_client(
        db,
        client_id
    )


def update_client(
    db: Session,
    client_id: int,
    updates: ClientUpdate,
    current_user
):

    client = crud.get_client(
        db,
        client_id
    )

    if not client:
        return None
    old_values = {
        "company_name": client.company_name,
        "contact_name": client.contact_name,
        "email": client.email
    }
    data = updates.model_dump(
        exclude_unset=True
    )

    for key, value in data.items():
        setattr(client, key, value)

    register_log(

        db=db,

        table_name="clients",

        record_id=client.id,

        action="UPDATE",

        user_id=current_user.id,

        old_values=old_values,

        new_values=data

    )

    return crud.update_client(
        db,
        client
    )


def delete_client(
    db: Session,
    client_id: int,
    current_user
):

    client = crud.get_client(
        db,
        client_id
    )

    if not client:
        return None
    
    old_values = {
        "company_name": client.company_name,
        "contact_name": client.contact_name,
        "email": client.email
    }

    crud.delete_client(
        db,
        client
    )

    register_log(

        db=db,

        table_name="clients",

        record_id=client.id,

        action="DELETE",

        user_id=current_user.id,

        old_values=old_values

    )

    return client
from sqlalchemy.orm import Session

from app.clients.models import Client


def create_client(db: Session, client: Client):

    db.add(client)
    db.commit()
    db.refresh(client)

    return client


def get_client(db: Session, client_id: int):

    return (
        db.query(Client)
        .filter(Client.id == client_id)
        .first()
    )


def get_client_by_email(
    db: Session,
    email: str
):

    return (
        db.query(Client)
        .filter(Client.email == email)
        .first()
    )


def get_clients(
    db: Session,
    skip: int = 0,
    limit: int = 100
):

    return (
        db.query(Client)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_client(
    db: Session,
    client: Client
):

    db.commit()
    db.refresh(client)

    return client


def delete_client(
    db: Session,
    client: Client
):

    db.delete(client)
    db.commit()
from sqlalchemy.orm import Session
from datetime import datetime
from app.ticket_comments import crud
from app.audit.service import register_log, register_update_log
from app.ticket_comments.models import TicketComment
from app.workflows.engine import run_workflow
from app.users.service import get_user
from app.clients.service import get_client

from app.tickets.schemas import (
    TicketUpdate
)


def register_ticket_comment(
    db,
    ticket_comment,
    current_user
):

    existing = crud.get_ticket_comment(
        db,
        ticket_comment.ticket_comment_id
    )

    if existing:
        return None

    user_exists = get_user(
        db,
        ticket_comment.user_id
    )

    if not user_exists:
        return "Usuario no encontrado"

    client_exists = get_client(
        db,
        ticket_comment.client_id
    )

    if not client_exists:
        return "Cliente no encontrado"


    db_ticket_comment = TicketComment(
        ticket_id=ticket_comment.ticket_id,
        comment=ticket_comment.comment,
        user_id=ticket_comment.user_id,
        client_id=ticket_comment.client_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    created = crud.create_ticket_comment(
        db,
        db_ticket_comment
    )

    # Register log
    register_log(
        db=db,
        table_name="ticket_comments",
        record_id=created.id,
        action="CREATE",
        user_id=current_user.id,
        client_id=current_user.client_id,
        new_values={
            "ticket_id": created.ticket_id,
            "comment": created.comment,
            "user_id": created.user_id,
            "client_id": created.client_id
        }
    )

    return created


def list_tickets_comments(
    db: Session,
    skip: int = 0,
    limit: int = 100
):

    return crud.get_ticket_comments(
        db, 
        skip,
        limit
    )


def get_ticket_comment(
    db: Session,    
    ticket_comment_id: int
):

    return crud.get_ticket_comment(
        db,
        ticket_comment_id
    )


def update_ticket_comment(
    db: Session,
    ticket_comment_id: int,
    updates: TicketUpdate,
    current_user
):

    ticket_comment = crud.get_ticket_comment(
        db,
        ticket_comment_id
    )

    if not ticket_comment:
        return None
    old_values ={
        "ticket_id": ticket_comment.ticket_id,
        "comment": ticket_comment.comment,
        "user_id": ticket_comment.user_id,
        "client_id": ticket_comment.client_id
    }
    data = updates.model_dump(
        exclude_unset=True
    )

    register_update_log(
        db=db,
        table_name="ticket_comments",
        old_record=ticket_comment,
        new_record=ticket_comment,
        user_id=current_user.id,
        client_id=current_user.client_id
    )

    for key, value in data.items():
        setattr(ticket_comment, key, value)

    register_log(
        db=db,
        table_name="ticket_comments",
        record_id=ticket_comment.id,
        action="UPDATE",
        user_id=current_user.id,
        client_id=current_user.client_id,
        old_values=old_values,
        new_values=data
    )
    
    return crud.update_ticket_comment(
        db,
        ticket_comment
    )


def delete_ticket_comment(
    db: Session,
    ticket_comment_id: int,
    current_user
):

    ticket_comment = crud.get_ticket_comment(
        db,
        ticket_comment_id
    )

    if not ticket_comment:
        return None
    old_values = {
        "ticket_id": ticket_comment.ticket_id,
        "comment": ticket_comment.comment,
        "user_id": ticket_comment.user_id,
        "client_id": ticket_comment.client_id
    }
    crud.delete_ticket_comment(
        db,
        ticket_comment
    )

    register_log(
        db=db,
        table_name="ticket_comments",
        record_id=ticket_comment.id,
        action="DELETE",
        user_id=current_user.id,
        client_id=current_user.client_id,
        old_values=old_values
    )

    return ticket_comment
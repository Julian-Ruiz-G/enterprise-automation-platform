from datetime import datetime

from sqlalchemy.orm import Session

from app.audit.service import register_log
from app.ticket_comments import crud
from app.ticket_comments.models import TicketComment
from app.ticket_comments.schemas import TicketCommentCreate
from app.tickets import crud as tickets_crud


def register_ticket_comment(
    db: Session,
    ticket_id: int,
    payload: TicketCommentCreate,
    current_user,
):
    ticket = tickets_crud.get_ticket(db, ticket_id)
    if ticket is None:
        return "Ticket no encontrado"

    comment = TicketComment(
        ticket_id=ticket_id,
        user_id=current_user.id,
        client_id=ticket.client_id,
        message=payload.message,
        is_internal=payload.is_internal,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    created = crud.create_ticket_comment(db, comment)

    if not payload.is_internal and ticket.first_response_at is None:
        ticket.first_response_at = datetime.now()
        tickets_crud.update_ticket(db, ticket)

    register_log(
        db=db,
        table_name="ticket_comments",
        record_id=created.id,
        action="CREATE",
        user_id=current_user.id,
        new_values={
            "ticket_id": created.ticket_id,
            "message": created.message,
            "user_id": created.user_id,
            "is_internal": created.is_internal,
        },
    )

    return created


def list_ticket_comments(
    db: Session,
    ticket_id: int,
    current_user,
    skip: int = 0,
    limit: int = 100,
):
    ticket = tickets_crud.get_ticket(db, ticket_id)
    if ticket is None:
        return "Ticket no encontrado"

    role_name = current_user.role.name if current_user.role else None
    include_internal = role_name != "Client"

    return crud.get_comments_by_ticket(
        db,
        ticket_id,
        skip=skip,
        limit=limit,
        include_internal=include_internal,
    )

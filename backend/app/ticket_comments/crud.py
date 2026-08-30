from sqlalchemy.orm import Session

from app.ticket_comments.models import TicketComment


def create_ticket_comment(db: Session, ticket_comment: TicketComment):
    db.add(ticket_comment)
    db.commit()
    db.refresh(ticket_comment)
    return ticket_comment


def get_ticket_comment(db: Session, ticket_comment_id: int):
    return (
        db.query(TicketComment)
        .filter(TicketComment.id == ticket_comment_id)
        .first()
    )


def get_comments_by_ticket(
    db: Session,
    ticket_id: int,
    skip: int = 0,
    limit: int = 100,
    include_internal: bool = True,
):
    query = db.query(TicketComment).filter(TicketComment.ticket_id == ticket_id)
    if not include_internal:
        query = query.filter(TicketComment.is_internal.is_(False))
    return (
        query.order_by(TicketComment.created_at)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_ticket_comment(db: Session, ticket_comment: TicketComment):
    db.commit()
    db.refresh(ticket_comment)
    return ticket_comment


def delete_ticket_comment(db: Session, ticket_comment: TicketComment):
    db.delete(ticket_comment)
    db.commit()

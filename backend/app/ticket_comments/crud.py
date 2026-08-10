from sqlalchemy.orm import Session

from app.ticket_comments.models import TicketComment
from app.assignment.service import assign_user


def create_ticket_comment(db: Session, ticket_comment: TicketComment):

    assigned = assign_user(
        db,
        ticket_comment.category
    )

    if assigned:
        ticket_comment.assigned_user_id = assigned.id
    
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



def get_ticket_comments(
    db: Session,
    skip: int = 0,
    limit: int = 100
):

    return (
        db.query(TicketComment)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_ticket_comment(
    db: Session,
    ticket_comment: TicketComment
):

    db.commit()
    db.refresh(ticket_comment)
    
    return ticket_comment


def delete_ticket_comment(
    db: Session,
    ticket_comment: TicketComment
):

    db.delete(ticket_comment)
    db.commit()
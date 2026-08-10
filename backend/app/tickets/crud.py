from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.tickets.models import Ticket
from app.ai.analyzer import analyze_ticket
from app.assignment.service import assign_user


def create_ticket(db: Session, ticket: Ticket):

    data = analyze_ticket(ticket)

    ticket.priority = data["prioridad"]
    ticket.category = data["categoria"]

    if ticket.priority == "Baja":
        ticket.sla_due_at = datetime.now() + timedelta(hours=48)

    elif ticket.priority == "Media":
        ticket.sla_due_at = datetime.now() + timedelta(hours=24)

    elif ticket.priority == "Alta":
        ticket.sla_due_at = datetime.now() + timedelta(hours=8)

    elif ticket.priority == "Urgente":
        ticket.sla_due_at = datetime.now() + timedelta(hours=1)

    assigned = assign_user(
        db,
        ticket.category
    )

    if assigned:
        ticket.assigned_user_id = assigned.id
    
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


def get_ticket(db: Session, ticket_id: int):

    return (
        db.query(Ticket)
        .filter(Ticket.id == ticket_id)
        .first()
    )


def get_ticket_by_title(
    db: Session,
    title: str
):

    return (
        db.query(Ticket)
        .filter(Ticket.title == title)
        .first()
    )


def get_tickets(
    db: Session,
    skip: int = 0,
    limit: int = 100
):

    return (
        db.query(Ticket)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_ticket(
    db: Session,
    ticket: Ticket
):

    db.commit()
    db.refresh(ticket)
    
    return ticket


def delete_ticket(
    db: Session,
    ticket: Ticket
):

    db.delete(ticket)
    db.commit()
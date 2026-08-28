import logging
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.tickets.models import Ticket
from app.ai.analyzer import analyze_ticket
from app.assignment.service import assign_user


logger = logging.getLogger(__name__)

SLA_HOURS = {

    "Baja": 48,
    "Media": 24,
    "Alta": 8,
    "Urgente": 1,

}

def create_ticket(db: Session, ticket: Ticket):

    ticket.category = "Soporte"
    ticket.priority = "Media"

    try:
        data = analyze_ticket(ticket)
        ticket.priority = data["prioridad"]
        ticket.category = data["categoria"]
        ticket.ai_category = data["categoria"]
        ticket.ai_priority = data["prioridad"]
        ticket.ai_summary = data["resumen"]
        ticket.ai_response = data["respuesta"]

    except Exception:
        logger.exception("Ia no disponible; Ticket guardado con valores por defecto")

    hours = SLA_HOURS.get(ticket.priority, 24)
    ticket.sla_due_at = datetime.now() + timedelta(hours=hours)

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
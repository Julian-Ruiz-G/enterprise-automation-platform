import logging
from sqlalchemy.orm import Session
from app.common.enums import TicketCategory, TicketPriority, TicketStatus
from datetime import datetime, timedelta, timezone

from app.tickets.models import Ticket
from app.ai.analyzer import analyze_ticket
from app.assignment.service import assign_user


logger = logging.getLogger(__name__)

SLA_HOURS = {
    TicketPriority.LOW.value: 24,
    TicketPriority.MEDIUM.value: 8,
    TicketPriority.HIGH.value: 2,
    TicketPriority.CRITICAL.value: 1,  # horas; luego afinamos a minutos
    # tickets viejos:
    "Baja": 48,
    "Media": 24,
    "Alta": 8,
    "Urgente": 1,
}

def create_ticket(db: Session, ticket: Ticket):

    ticket.category = TicketCategory.SUPPORT.value
    ticket.priority = TicketPriority.MEDIUM.value

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

def get_sla_breached_tickets(db: Session) -> list[Ticket]:
    now = datetime.now(timezone.utc)
    closed = (
        TicketStatus.RESOLVED.value,
        TicketStatus.CLOSED.value,
    )
    return (
        db.query(Ticket)
        .filter(
            Ticket.sla_due_at.isnot(None),
            Ticket.sla_due_at < now,
            Ticket.first_response_at.is_(None),
            Ticket.sla_alerted_at.is_(None),
            Ticket.status.notin_(closed),
        )
        .all()
    )
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.tickets import crud
from app.audit.service import register_log
from app.tickets.models import Ticket
from app.workflows.engine import run_workflow
from app.clients.service import get_client

from app.tickets.schemas import (
    TicketUpdate
)


def register_ticket(
    db,
    ticket,
    current_user
):

    client_exists = get_client(
        db,
        ticket.client_id
    )

    if not client_exists:
        return "Cliente no encontrado"


    assigned_id = ticket.assigned_user_id
    if assigned_id == 0:
        assigned_id = None

    db_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        status=ticket.status,
        channel=ticket.channel,
        client_id=ticket.client_id,
        assigned_user_id=assigned_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    created = crud.create_ticket(
        db,
        db_ticket
    )
    
    # Run workflow  
    run_workflow(
        db,
        "NEW_TICKET",
        {
            "ticket_id": created.id,
            "title": created.title,
            "client_id": created.client_id,
            "priority": created.priority,
            "category": created.category,
            "status": created.status,
        },
    )
    
    register_log(
        db=db,
        table_name="tickets",
        record_id=created.id,
        action="CREATE",
        user_id=current_user.id,
        new_values={
            "title": created.title,
            "description": created.description,
            "status": created.status,
            "priority": created.priority,
            "channel": created.channel,
            "client_id": created.client_id
        }
    )

    return created


def list_tickets(
    db: Session,
    skip: int = 0,
    limit: int = 100
):

    return crud.get_tickets(
        db, 
        skip,
        limit
    )


def get_ticket(
    db: Session,    
    ticket_id: int
):

    return crud.get_ticket(
        db,
        ticket_id
    )


def update_ticket(
    db: Session,
    ticket_id: int,
    updates: TicketUpdate,
    current_user,
):
    ticket = crud.get_ticket(db, ticket_id)

    if not ticket:
        return None

        

    old_values = {
        "title": ticket.title,
        "description": ticket.description,
        "status": ticket.status,
        "priority": ticket.priority,
        "channel": ticket.channel,
        "client_id": ticket.client_id,
        "assigned_user_id": ticket.assigned_user_id,
        "category": ticket.category,
    }

    data = updates.model_dump(exclude_unset=True)

    # Swagger envía 0 en enteros opcionales; 0 no es un id válido
    if data.get("assigned_user_id") == 0:
        data["assigned_user_id"] = None
    if data.get("client_id") == 0:
        data.pop("client_id", None)

    for key, value in data.items():
        setattr(ticket, key, value)

    ticket.updated_at = datetime.now()

    if ticket.status == "CLOSED" and getattr(ticket, "closed_at", None) is None:
        ticket.closed_at = datetime.now()

    register_log(
        db=db,
        table_name="tickets",
        record_id=ticket.id,
        action="UPDATE",
        user_id=current_user.id,
        old_values=old_values,
        new_values=data,
    )

    return crud.update_ticket(db, ticket)


def delete_ticket(
    db: Session,
    ticket_id: int,
    current_user
):

    ticket = crud.get_ticket(
        db,
        ticket_id
    )

    if not ticket:
        return None
    old_values = {
        "title": ticket.title,
        "description": ticket.description,
        "status": ticket.status,
        "priority": ticket.priority,
        "channel": ticket.channel,
        "client_id": ticket.client_id
    }
    crud.delete_ticket(
        db,
        ticket
    )

    register_log(
        db=db,
        table_name="tickets",
        record_id=ticket.id,
        action="DELETE",
        user_id=current_user.id,
        old_values=old_values
    )

    return ticket

def check_sla_breaches(db: Session) -> list[int]:
    tickets = crud.get_sla_breached_tickets(db)
    ids = []
    now = datetime.now(timezone.utc)
    for ticket in tickets:
        run_workflow(
            db,
            "SLA_BREACH",
            {
                "ticket_id": ticket.id,
                "title": ticket.title,
                "client_id": ticket.client_id,
                "priority": ticket.priority,
                "category": ticket.category,
                "status": ticket.status,
            },
        )
        ticket.sla_alerted_at = now
        ids.append(ticket.id)
    if ids:
        db.commit()
    return ids
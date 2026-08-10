from sqlalchemy.orm import Session
from datetime import datetime
from app.tickets import crud
from app.audit.service import register_log, register_update_log
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

    existing = crud.get_ticket_by_title(
        db,
        ticket.title
    )

    if existing:
        return None

    client_exists = get_client(
        db,
        ticket.client_id
    )

    if not client_exists:
        return "Cliente no encontrado"


    db_ticket = Ticket(
        title=ticket.title,
        description=ticket.description,
        status=ticket.status,
        channel=ticket.channel,
        client_id=ticket.client_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    created = crud.create_ticket(
        db,
        db_ticket
    )
    

    print("====== IA ======")
    print(created.ai_category)
    print(created.ai_priority)
    print(created.ai_summary)
    print(created.ai_response)
    print(created.ai_category)
    print(db_ticket.ai_response)
    print("====== FIN IA ======")
    
    # Run workflow  
    run_workflow(
        db,
        "NEW_TICKET",
        {
            "ticket_id": created.id,
            "title": created.title,
            "client_id": created.client_id
        }
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
    current_user
):

    ticket = crud.get_ticket(
        db,
        ticket_id
    )

    if not ticket:
        return None
    old_values ={
        "title": ticket.title,
        "description": ticket.description,
        "status": ticket.status,
        "priority": ticket.priority,
        "channel": ticket.channel,
        "client_id": ticket.client_id
    }
    data = updates.model_dump(
        exclude_unset=True
    )

    register_update_log(
        db=db,
        table_name="tickets",
        old_record=ticket,
        new_record=ticket,
        user_id=current_user.id
    )

    for key, value in data.items():
        setattr(ticket, key, value)

    register_log(
        db=db,
        table_name="tickets",
        record_id=ticket.id,
        action="UPDATE",
        user_id=current_user.id,
        old_values=old_values,
        new_values=data
    )
    
    return crud.update_ticket(
        db,
        ticket
    )


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
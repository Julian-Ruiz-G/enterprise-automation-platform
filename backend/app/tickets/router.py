from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.tickets.schemas import (
    TicketCreate,
    TicketUpdate,
    TicketResponse,
    SlaCheckResponse,
    TicketStatsResponse,
)

from app.tickets.service import (
    register_ticket,
    list_tickets,
    get_ticket,
    update_ticket,
    delete_ticket,
    check_sla_breaches,
    ticket_stats,
)
from app.security.dependencies import (
    get_current_user,
    require_role_name,
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

@router.post(
    "",
    response_model=TicketResponse
)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    created = register_ticket(
        db,
        ticket,
        current_user
    )

    if created is None:
        raise HTTPException(
            status_code=400,
            detail="El ticket ya existe"
        )

    if created == "Cliente no encontrado":
        raise HTTPException(
            status_code=400,
            detail="Cliente no encontrado"
        )

    return created


@router.get(
    "",
    response_model=list[TicketResponse]
)
def get_tickets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return list_tickets(
        db,
        skip,
        limit
    )


@router.post(
    "/sla-check",
    response_model=SlaCheckResponse,
)
def run_sla_check(
    db: Session = Depends(get_db),
    current_user=Depends(require_role_name("Administrador")),
):
    ids = check_sla_breaches(db)
    return SlaCheckResponse(
        breached_count=len(ids),
        ticket_ids=ids,
    )

@router.get(
    "/stats",
    response_model=TicketStatsResponse,
)
def get_ticket_stats(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    return ticket_stats(db)

@router.get(
    "/{ticket_id}",
    response_model=TicketResponse   
)
def get_one_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    ticket = get_ticket(
        db,
        ticket_id
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket no encontrado"
        )

    return ticket

@router.put(
    "/{ticket_id}",
    response_model=TicketResponse
)
def edit_ticket(
    ticket_id: int,
    updates: TicketUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)

):

    ticket = update_ticket(
        db,
        ticket_id,
        updates,
        current_user
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket no encontrado"
        )
    if ticket == "Usuario no encontrado":
        raise HTTPException(
            status_code=400,
            detail="Usuario no encontrado"
        )
    if ticket == "Cliente no encontrado":
        raise HTTPException(
            status_code=400,
            detail="Cliente no encontrado"
        )
    return ticket

@router.delete(
    "/{ticket_id}"
)
def remove_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    ticket = delete_ticket(
        db,
        ticket_id,
        current_user
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket no encontrado"
        )

    return {
        "message": "Ticket eliminado correctamente"
    }
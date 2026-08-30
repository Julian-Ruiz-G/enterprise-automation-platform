from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 

from app.database.database import get_db
from app.security.dependencies import get_current_user
from app.ticket_comments.schemas import TicketCommentCreate, TicketCommentResponse
from app.ticket_comments.service import list_ticket_comments, register_ticket_comment

router = APIRouter(
    prefix="/tickets/{ticket_id}/comments",
    tags=["Ticket comments"],
)

@router.post(
    "", response_model=TicketCommentResponse
)

def create_comment(
    ticket_id: int,
    payload: TicketCommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    created = register_ticket_comment(db, ticket_id, payload, current_user)

    if created == "Ticket no encontrado":
        raise HTTPException(
            status_code=404,
            detail="Ticket no encontrado"
        )
    return created

@router.get("", response_model=list[TicketCommentResponse])
def get_comments(
    ticket_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    comments = list_ticket_comments(
        db,
        ticket_id,
        current_user,
        skip=skip,
        limit=limit,
    )
    if comments == "Ticket no encontrado":
        raise HTTPException(status_code=404, detail="Ticket no encontrado")
    return comments
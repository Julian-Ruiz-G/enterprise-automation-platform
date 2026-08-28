from fastapi import APIRouter, Depends

from app.ai.analyzer import analyze_ticket
from app.tickets.schemas import TicketCreate, TicketAnalysis

from app.security.dependencies import get_current_user
from app.users.models import User

router = APIRouter(
    prefix="/ai",
    tags=["Artificial Intelligence"]
)


@router.post(
    "/analyze",
    response_model=TicketAnalysis
)
def analyze(ticket: TicketCreate, current_user: User = Depends(get_current_user)):

    return analyze_ticket(ticket=ticket)
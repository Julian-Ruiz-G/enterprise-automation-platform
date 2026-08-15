from fastapi import APIRouter

from app.ai.analyzer import analyze_ticket
from app.tickets.schemas import TicketCreate, TicketResponse, TicketAnalysis

router = APIRouter(
    prefix="/ai",
    tags=["Artificial Intelligence"]
)


@router.post(
    "/analyze",
    response_model=TicketAnalysis
)
def analyze(ticket: TicketCreate):

    return analyze_ticket(ticket=ticket)
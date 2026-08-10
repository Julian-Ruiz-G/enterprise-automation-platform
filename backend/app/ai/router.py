from fastapi import APIRouter

from app.ai.schemas import TicketAnalysis
from app.ai.analyzer import analyze_ticket

router = APIRouter(
    prefix="/ai",
    tags=["Artificial Intelligence"]
)


@router.post(
    "/analyze",
    response_model=TicketAnalysis
)
def analyze():

    return analyze_ticket(

        title="No puedo descargar mi factura",

        description="Cuando doy clic aparece error 500."
    )
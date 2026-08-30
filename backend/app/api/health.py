from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.database import get_db

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "enterprise-automation-platform",
    }


@router.get("/health/ready")
def health_ready(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Base de datos no disponible",
        )
    return {"status": "ready"}
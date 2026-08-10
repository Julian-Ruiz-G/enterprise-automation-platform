from sqlalchemy.orm import Session

from app.roles import crud

def list_roles(db: Session):
    return crud.get_roles(db)

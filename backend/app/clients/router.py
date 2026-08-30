from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.clients.schemas import (
    ClientCreate,
    ClientUpdate,
    ClientResponse
)

from app.clients.service import (
    register_client,
    list_clients,
    get_client,
    update_client,
    delete_client
)

from app.security.dependencies import (
    get_current_user,
    require_role_name,
)

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

@router.post(
    "",
    response_model=ClientResponse
)
def create_client(
    client: ClientCreate,

    db: Session = Depends(get_db),

    current_user=Depends(require_role_name("Administrador"))
    
):

    created = register_client(
        db,
        client,
        current_user
    )

    if created is None:
        raise HTTPException(
            status_code=400,
            detail="El cliente ya existe"
        )

    return created

@router.get(
    "",
    response_model=list[ClientResponse]
)
def get_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return list_clients(
        db,
        skip,
        limit
    )

@router.get(
    "/{client_id}",
    response_model=ClientResponse
)
def get_one_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    client = get_client(
        db,
        client_id
    )

    if client is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    return client

@router.put(
    "/{client_id}",
    response_model=ClientResponse
)
def edit_client(
    client_id: int,
    updates: ClientUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role_name("Administrador"))
):

    client = update_client(
        db,
        client_id,
        updates,
        current_user
    )

    if client is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    return client

@router.delete(
    "/{client_id}"
)
def remove_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role_name("Administrador"))

):

    client = delete_client(
        db,
        client_id,
        current_user
    )

    if client is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )


    return {
        "message": "Cliente eliminado correctamente"
    }
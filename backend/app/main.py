from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.core.config import settings
from app.api.health import router as health_router
from app.users.router import router as users_router
from app.workflows.router import router as workflows_router
from app.roles.router import router as roles_router
from app.audit.router import router as audit_router
from app.clients.router import router as clients_router
from app.tickets.router import router as tickets_router
from app.ai.router import router as ai_router
import app.roles.models
import app.users.models
import app.clients.models
import app.audit.models
import app.tickets.models
import app.workflows.models


from app.database.database import Base, engine


app = FastAPI(
    title=settings.APP_NAME
    
)

app.include_router(health_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(workflows_router)
app.include_router(roles_router)
app.include_router(audit_router)
app.include_router(clients_router)
app.include_router(tickets_router)
app.include_router(ai_router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {
        "message": "Enterprise Automation Platform"
    }
    
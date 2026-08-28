from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app = FastAPI(
    title=settings.APP_NAME

)

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.get("/")
def root():
    return {
        "message": "Enterprise Automation Platform"
    }
    
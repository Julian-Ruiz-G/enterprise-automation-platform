# Enterprise Automation Platform

Una plataforma integral de automatización empresarial construida con FastAPI, diseñada para gestionar workflows, tickets, usuarios, roles y auditoría de sistemas.

## Arquitectura

### Stack Tecnológico

- **Backend**: FastAPI 0.138.0
- **Base de Datos**: PostgreSQL 16
- **Cache**: Redis 7
- **ORM**: SQLAlchemy 2.0.51
- **Validación**: Pydantic 2.13.4
- **Migraciones**: Alembic 1.18.4
- **Autenticación**: JWT (python-jose)
- **Servidor ASGI**: Uvicorn 0.49.0

### Estructura del Proyecto

```
enterprise-automation-platform/
├── backend/
│   ├── app/
│   │   ├── ai/              # Módulo de IA y automatización inteligente
│   │   ├── api/             # Endpoints de API
│   │   ├── auth/            # Autenticación y autorización
│   │   ├── audit/           # Sistema de auditoría
│   │   ├── clients/         # Gestión de clientes
│   │   ├── common/          # Utilidades comunes
│   │   ├── core/            # Configuración central
│   │   ├── database/        # Configuración de base de datos
│   │   ├── notifications/   # Sistema de notificaciones
│   │   ├── roles/           # Gestión de roles y permisos
│   │   ├── security/        # Seguridad y encriptación
│   │   ├── tickets/         # Sistema de tickets
│   │   ├── users/           # Gestión de usuarios
│   │   ├── workflow_engine/ # Motor de workflows
│   │   └── workflows/       # Gestión de workflows
│   ├── alembic/             # Migraciones de base de datos
│   ├── tests/               # Tests unitarios
│   ├── requirements.txt     # Dependencias de Python
│   └── .env                 # Variables de entorno (no versionado)
├── frontend/                # Frontend (pendiente)
├── infrastructure/          # Infraestructura como código (pendiente)
├── docs/                    # Documentación (pendiente)
├── docker-compose.yml       # Orquestación de contenedores
└── .gitignore              # Archivos ignorados por git
```

## Configuración e Instalación

### Prerrequisitos

- Docker y Docker Compose
- Python 3.13+
- Git

### Variables de Entorno

Crear un archivo `.env` en el directorio `backend/` con las siguientes variables:

```env
APP_NAME=Enterprise Automation Platform
ENVIRONMENT=development

# PostgreSQL
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
JWT_SECRET_KEY
JWT_ALGORITHM

# Tokens
ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS
```

### Iniciar con Docker

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd enterprise-automation-platform
```

2. Iniciar los servicios:
```bash
docker-compose up -d
```

3. Verificar que los servicios estén corriendo:
```bash
docker-compose ps
```

### Instalación Local

1. Crear entorno virtual:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar base de datos:
```bash
alembic upgrade head
```

4. Iniciar el servidor:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📡 API Endpoints

### Endpoints Principales

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /auth/login` - Inicio de sesión
- `POST /auth/register` - Registro de usuarios
- `GET /users/` - Listar usuarios
- `GET /workflows/` - Listar workflows
- `GET /tickets/` - Listar tickets
- `GET /roles/` - Listar roles
- `GET /audit/` - Logs de auditoría
- `GET /clients/` - Listar clientes
- `GET /ai/` - Endpoints de IA

### Documentación Interactiva

Una vez iniciado el servidor, accede a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🗄️ Base de Datos

### Migraciones

Crear nueva migración:
```bash
alembic revision --autogenerate -m "description"
```

Aplicar migraciones:
```bash
alembic upgrade head
```

Revertir migración:
```bash
alembic downgrade -1
```

## Seguridad

- Autenticación basada en JWT
- Encriptación de contraseñas con bcrypt
- Sistema de roles y permisos
- Auditoría de acciones
- Variables de entorno para datos sensibles

## Testing

Ejecutar tests:
```bash
pytest
```

Ejecutar tests con cobertura:
```bash
pytest --cov=app --cov-report=html
```

## Módulos Principales

### Auth
- Registro y autenticación de usuarios
- Gestión de tokens JWT (access y refresh)
- Validación de credenciales

### Users
- CRUD de usuarios
- Gestión de perfiles
- Asignación de roles

### Roles
- Definición de roles y permisos
- Asignación de roles a usuarios
- Control de acceso basado en roles (RBAC)

### Tickets
- Sistema de tickets de soporte
- Gestión de estados y prioridades
- Comentarios en tickets

### Workflows
- Definición de workflows
- Ejecución de procesos automatizados
- Motor de workflow engine

### Audit
- Registro de acciones del sistema
- Trazabilidad de cambios
- Logs de seguridad

### Clients
- Gestión de clientes empresariales
- Información de contacto
- Historial de interacciones

### AI
- Integración con servicios de IA
- Automatización inteligente
- Análisis predictivo

## Desarrollo

### Código de Estilo

El proyecto sigue las convenciones de PEP 8 y utiliza:
- Type hints
- Pydantic para validación
- SQLAlchemy ORM
- FastAPI para la API

### Branching Strategy

- `master` - Rama principal de producción
- `develop` - Rama de desarrollo
- `feature/*` - Nuevas funcionalidades
- `bugfix/*` - Correcciones de bugs



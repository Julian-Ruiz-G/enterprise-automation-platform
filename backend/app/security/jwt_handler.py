from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

def create_access_token(payload):   
    expire = datetime.utcnow() + timedelta(minutes=15)
    payload.update({"exp": expire})
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

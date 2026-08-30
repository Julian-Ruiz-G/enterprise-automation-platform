from pydantic import BaseModel, EmailStr, ConfigDict


class ClientCreate(BaseModel):

    company_name: str
    contact_name: str
    email: EmailStr
    phone: str
    address: str
    city: str
    country: str


class ClientUpdate(BaseModel):

    company_name: str | None = None
    contact_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    city: str | None = None
    country: str | None = None
    is_active: bool | None = None


class ClientResponse(BaseModel):

    id: int
    company_name: str
    contact_name: str
    email: EmailStr
    phone: str
    address: str
    city: str
    country: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
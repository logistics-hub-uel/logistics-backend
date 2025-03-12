from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, List
from .base import BaseSchema
from app.models.enums import RoleEnum

class AccountBase(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    role: RoleEnum
    tax_number: Optional[str] = None
    address: Optional[Dict] = None

class AccountCreateRequest(AccountBase):
    password: str

class AccountCreateResponse(BaseModel):
    user_id: str

    # ORM 
    class config:
        orm_mode = True

class AccountResetPasswordRequest(BaseModel):
    email: EmailStr

class AccountNewPasswordRequest(BaseModel):
    password: str
    token: str

class AccountUpdateRequest(AccountBase):
    id: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.helpers.enums import UserRole
from app.models.enums import RoleEnum
from app.models.enums import VisibilityEnum

# Document Schemas
class SchemaDocumentCreate(BaseModel):
    title: str
    visibility: VisibilityEnum = VisibilityEnum.private

class SchemaDocumentUpdate(BaseModel):
    title: Optional[str] = None
    visibility: Optional[VisibilityEnum] = None

class SchemaDocumentResponse(BaseModel):
    id: str
    title: str
    visibility: VisibilityEnum
    created_at: datetime
    updated_at: datetime
    account_id: str

    class Config:
        orm_mode = True

# Page Schemas
class SchemaPageCreate(BaseModel):
    content: str
    image_url: Optional[str] = None
    document_id: str

class SchemaPageUpdate(BaseModel):
    content: Optional[str] = None
    image_url: Optional[str] = None

class SchemaPageResponse(BaseModel):
    id: str
    content: str
    image_url: Optional[str]
    document_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# List Response Schemas
class SchemaDocumentList(BaseModel):
    total: int
    items: list[SchemaDocumentResponse]

class SchemaPageList(BaseModel):
    total: int
    items: list[SchemaPageResponse]


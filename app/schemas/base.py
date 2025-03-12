from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from typing import Optional, TypeVar, Generic
from pydantic.generics import GenericModel

from app.constants.cnt_message import *
from pydantic import BaseModel


class BaseSchema(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True



T = TypeVar("T")


class ResponseSchemaBase(BaseModel):
    __abstract__ = True

    code: str = ''
    message: str = ''

    def custom_response(self, code: str, message: str):
        self.code = code
        self.message = message
        return self

    def success_response(self):
        self.code = '000'
        self.message = SUCCESS_RESPONSE_MESSAGE
        return self


class DataResponse(ResponseSchemaBase, GenericModel, Generic[T]):
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True

    def custom_response(self, code: str, message: str, data: T):
        self.code = code
        self.message = message
        self.data = data
        return self

    def success_response(self, data: T):
        self.code = '000'
        self.message = SUCCESS_RESPONSE_MESSAGE
        self.data = data
        return self


class MetadataSchema(BaseModel):
    current_page: int
    page_size: int
    total_items: int

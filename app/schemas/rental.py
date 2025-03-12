from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .base import BaseSchema
from app.models.enums import StatusEnum

class ServiceRentalBase(BaseModel):
    buyer_id: str
    service_id: str
    status: StatusEnum
    demand_description: Optional[str] = None
    expectation: Optional[str] = None
    from_date: datetime
    to_date: datetime

class ServiceRentalCreate(ServiceRentalBase):
    pass

class ServiceRentalUpdate(ServiceRentalBase):
    pass

class ServiceRental(ServiceRentalBase, BaseSchema):
    pass

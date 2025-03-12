from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List
from .base import BaseSchema
from app.models.enums import StatusEnum

class DemandBase(BaseModel):
    from_date: datetime
    to_date: datetime
    demand_description: Optional[str] = None
    previous_experience: Optional[str] = None
    expectation: Optional[str] = None
    preference_social_media: Optional[List[str]] = None
    is_support_preference: bool = False
    type_demand_service: str
    demand_status: StatusEnum
    account_id: str

class DemandCreate(DemandBase):
    pass

class DemandUpdate(DemandBase):
    pass

class Demand(DemandBase, BaseSchema):
    pass

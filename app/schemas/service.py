from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from decimal import Decimal
from .base import BaseSchema

# BASE
class ServiceBase(BaseModel):
    name: str
    description: str
    price: Decimal
    available_time_slots: Dict 
    images_urls: Optional[List[str]] = None
    is_support_preference: bool
    preference_social_media: List[str] = None
    category: str

    class config:
        orm_mode = True


# CREATE A SERVICE
class ServiceCreateRequest(ServiceBase, BaseSchema):
    supplier_id: Optional[str] = None

class ServiceCreateResponse(BaseModel):
    service_id: str

# UPDATE A SERVICE
class ServiceUpdateRequest(ServiceBase):
    supplier_id: str


class ServiceUpdateResponse(BaseModel):
    service_id: str

# DELETE A SERVICE
class ServiceDeleteRequest(BaseModel):
    service_id: str

class ServiceDeleteResponse(BaseModel):
    service_id: str

# GET A SERVICE BY ID
class ServiceGetByIdRequest(BaseModel):
    service_id: str

class ServiceItemResponse(ServiceBase, BaseSchema):
    supplier_id: str
    rentals: Optional[List[Dict]] = []

class ServiceUpdateRequest(ServiceBase):
    pass
    

class ServiceUpdateResponse(BaseModel):
    service_id: str

# CREATE A SERVICE RENTAL REQUEST
class ServiceRentalBase(BaseModel):
    service_id: str
    buyer_id: str   
    status: str
    from_date: datetime
    to_date: datetime
    demand_description: str
    expectation: str

    class config:
        orm_mode = True

class ServiceRentalResponseItem(ServiceRentalBase, BaseSchema):
    name: str
    pass

class ServiceRentalCreateRequest(ServiceRentalBase):
    pass

class ServiceRentalCreateResponse(BaseModel):
    rental_id: str

# GET A SERVICE RENTAL BY ID
class ServiceRentalGetByIdRequest(BaseModel):
    rental_id: str

class ServiceRentalGetByIdResponse(ServiceRentalBase, BaseSchema):
    pass 

# UPDATE A SERVICE RENTAL
class ServiceRentalUpdateRequest(BaseModel):
    status: str

class ServiceRentalUpdateResponse(BaseModel):
    rental_id: str




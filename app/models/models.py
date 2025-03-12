from sqlalchemy.dialects.postgresql import JSONB, NUMERIC, ARRAY
from sqlalchemy import Column, String, Boolean, Enum, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.enums import RoleEnum, StatusEnum
from app.core.config import settings
from app.models.model_base import BareBaseModel
# Enums

class Account(BareBaseModel):
    __tablename__ = 'account'
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone_number = Column(String(20), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role =  Column(Enum(RoleEnum, name="role_enum"), default=RoleEnum.buyer)
    tax_number = Column(String, nullable=True)
    address = Column(JSONB, nullable=True)
    services = relationship('Service', back_populates='supplier', cascade="all, delete-orphan")
    rentals = relationship('ServiceRental', back_populates='buyer', cascade="all, delete-orphan")
    demands = relationship('Demand', back_populates='account', cascade="all, delete-orphan")
    demand_applications = relationship('DemandApplication', back_populates='supplier', cascade="all, delete-orphan")

class Service(BareBaseModel):
    __tablename__ = 'service'
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(NUMERIC, nullable=False)
    available_time_slots = Column(JSONB, nullable=False)
    images_urls = Column(ARRAY(String), nullable=True)
    is_support_preference = Column(Boolean, default=False, nullable=False)
    preference_social_media = Column(ARRAY(String), nullable=True)
    category = Column(String, nullable=False)
    supplier_id = Column(String, ForeignKey('account.id', ondelete="CASCADE"), nullable=False)
    rentals = relationship('ServiceRental', back_populates='service', cascade="all, delete-orphan")
    supplier = relationship('Account', back_populates='services')

class ServiceRental(BareBaseModel):
    __tablename__ = 'service_rental'
    buyer_id = Column(String, ForeignKey('account.id', ondelete="CASCADE"), nullable=False)
    service_id = Column(String, ForeignKey('service.id', ondelete="CASCADE"), nullable=False)
    status = Column(Enum(StatusEnum, name="status_enum"), default=StatusEnum.pending, nullable=False)
    demand_description = Column(String, nullable=True)
    expectation = Column(String, nullable=True)
    from_date = Column(DateTime, nullable=False)
    to_date = Column(DateTime, nullable=False)
    buyer = relationship('Account', back_populates='rentals')
    service = relationship('Service', back_populates='rentals')

class Demand(BareBaseModel):
    __tablename__ = 'demand'
    from_date = Column(DateTime, nullable=False)
    to_date = Column(DateTime, nullable=False)
    demand_description = Column(String, nullable=True)
    previous_experience = Column(String, nullable=True)
    expectation = Column(String, nullable=True)
    preference_social_media = Column(ARRAY(String), nullable=True)
    is_support_preference = Column(Boolean, default=False, nullable=False)
    type_demand_service = Column(String, nullable=False)
    demand_status = Column(Enum(StatusEnum, name="status_enum"), default=StatusEnum.pending, nullable=False)
    account_id = Column(String, ForeignKey('account.id', ondelete="CASCADE"), nullable=False)
    account = relationship('Account', back_populates='demands')
    demand_applications = relationship('DemandApplication', back_populates='demand', cascade="all, delete-orphan")

class DemandApplication(BareBaseModel):
    __tablename__ = 'demand_application'
    demand_id = Column(String, ForeignKey('demand.id', ondelete="CASCADE"), nullable=False)
    supplier_id = Column(String, ForeignKey('account.id', ondelete="CASCADE"), nullable=False)  
    payment_method = Column(String, nullable=False)
    application_status = Column(Enum(StatusEnum, name="status_enum"), default=StatusEnum.pending, nullable=False)
    promotion_event = Column(String, nullable=True)
    note = Column(String, nullable=True)

    demand = relationship('Demand', back_populates='demand_applications')
    supplier = relationship('Account', back_populates='demand_applications')
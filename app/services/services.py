import jwt


from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi_sqlalchemy import db
from pydantic import ValidationError
from starlette import status

from app.models import *

from app.core.config import settings
from app.core.security import verify_password, get_password_hash
from app.schemas.sche_token import TokenPayload
from app.helpers.paging import Page, PaginationParams, paginate
from app.schemas.service import *
from app.helpers.filters import ServiceFilter, RentalFilter

class ServiceService(object): 
    __instance = None

    def __init__(self):
        pass


    @staticmethod   
    def get_service_by_id(service_id: int) -> ServiceItemResponse:
        service = db.session.query(Service).filter(Service.id == service_id).first()
        # GET THE RENTALS IN THE SERVICE
        service_detail = ServiceItemResponse(**service.__dict__) if service else None
        service_detail.rentals = db.session.query(ServiceRental).filter(ServiceRental.service_id == service_id).all()
        return service_detail
    @staticmethod   
    def update_service(service_id: int, data: ServiceUpdateRequest):
        service = db.session.query(Service).filter(Service.id == service_id).first()
        if service:
            service.name = data.name
            service.description = data.description
            service.price = data.price
            service.available_time_slots = data.available_time_slots
            service.images_urls = data.images_urls
            service.is_support_preference = data.is_support_preference
            service.preference_social_media = data.preference_social_media
            service.category = data.category
            db.session.commit()
            db.session.refresh(service)
            return service
        return None

    @staticmethod 
    def create_service(data: ServiceCreateRequest) -> ServiceItemResponse:
        new_service = Service(
            name=data.name,
            description=data.description,
            price=data.price,
            available_time_slots=data.available_time_slots,
            images_urls=data.images_urls,
            is_support_preference=data.is_support_preference,
            preference_social_media=data.preference_social_media,
            category=data.category,
            supplier_id=data.supplier_id
        )

        db.session.add(new_service)
        db.session.commit()
        db.session.refresh(new_service)
        service = ServiceItemResponse(
            id=new_service.id,
            name=new_service.name,
            description=new_service.description,
            price=new_service.price,
            available_time_slots=new_service.available_time_slots,
            images_urls=new_service.images_urls,
            is_support_preference=new_service.is_support_preference,
            preference_social_media=new_service.preference_social_media,
            category=new_service.category,
            supplier_id=new_service.supplier_id,
            created_at=new_service.created_at,
            updated_at=new_service.updated_at
        )
        return service 

    @staticmethod
    def get_all(params, name: str = None, category: str = None, min_price: float = None, max_price: float = None, supplier_id: str = None):
        _query = db.session.query(Service)
        
        # Apply filters using the helper
        _query = ServiceFilter.apply_filters(
            query=_query,
            name=name,
            category=category,
            min_price=min_price,
            max_price=max_price,
            supplier_id=supplier_id
        )
        
        services = paginate(model=Service, query=_query, params=params)
        return services
    
    @staticmethod
    def update_service(service_id: str, data: ServiceUpdateRequest, payload: TokenPayload) -> ServiceUpdateResponse:
        service = db.session.query(Service).filter(Service.id == service_id).first()
        if service:
            if service.supplier_id != payload.user_id:
                raise HTTPException(status_code=403, detail="You do not have permission to update this service")
            service.name = data.name
            service.description = data.description
            service.price = data.price
            service.available_time_slots = data.available_time_slots
            service.images_urls = data.images_urls
            service.is_support_preference = data.is_support_preference
            service.preference_social_media = data.preference_social_media
            service.category = data.category
            db.session.commit()
            db.session.refresh(service)
            return ServiceUpdateResponse(service_id=service.id)
        return None
    
    @staticmethod
    def delete_service(service_id: str, payload: TokenPayload) -> ServiceDeleteResponse:
        service = db.session.query(Service).filter(Service.id == service_id).first()
        if service:
            if service.supplier_id != payload.user_id:
                raise HTTPException(status_code=403, detail="You do not have permission to delete this service")
            db.session.delete(service)
            db.session.commit()
            return ServiceDeleteResponse(service_id=service.id)
        return None
    
    @staticmethod
    def rent_service(data: ServiceRentalCreateRequest, payload: TokenPayload) -> ServiceRentalCreateResponse:
        service = db.session.query(Service).filter(Service.id == data.service_id).first()
        if not service:
            raise HTTPException(status_code=404, detail="Service not found")
        
        # Get the list of current rentals and check if the service is available in the time range is just pending or canceled
        rentals = db.session.query(ServiceRental).filter(ServiceRental.service_id == data.service_id, ServiceRental.status.in_([StatusEnum.accepted]), 
            ServiceRental.from_date <= data.to_date, ServiceRental.to_date >= data.from_date).all()
        
        if rentals:
            raise HTTPException(status_code=400, detail="Service is not available in this time")

        if service.supplier_id == payload.user_id:
            raise HTTPException(status_code=400, detail="You can not rent your own service")
        
        new_rental = ServiceRental(
            buyer_id=payload.user_id,
            service_id=data.service_id,
            status=StatusEnum.pending,
            demand_description=data.demand_description,
            expectation=data.expectation,
            from_date=data.from_date,
            to_date=data.to_date
        )
        
        db.session.add(new_rental)
        db.session.commit()
        db.session.refresh(new_rental)
        
        rental = ServiceRentalCreateResponse(
            rental_id=new_rental.id
        )
        
        return rental
    
    @staticmethod
    def get_all_rentals(params: PaginationParams):
        query = db.session.query(ServiceRental).join(Service, Service.id == ServiceRental.service_id)
        # query = RentalFilter.apply_filters(query, **filter_params)
        rentals = paginate(model=ServiceRental, query=query, params=params)

        items = []
        for rental in rentals.data:
            rental_item = ServiceRentalResponseItem(
                id=rental.id,
                name=rental.service.name,
                buyer_id=rental.buyer_id,
                service_id=rental.service_id,
                status=rental.status.value,
                demand_description=rental.demand_description,
                expectation=rental.expectation,
                from_date=rental.from_date,
                to_date=rental.to_date,
                created_at=rental.created_at,
                updated_at=rental.updated_at
            )
            items.append(rental_item)

        rentals.data = items
        return rentals
    
    @staticmethod
    def update_rental(rental_id: str, data: ServiceRentalUpdateRequest, payload: TokenPayload) -> ServiceRentalUpdateResponse:
        rental = db.session.query(ServiceRental).filter(ServiceRental.id == rental_id).first()
        if not rental:
            raise HTTPException(status_code=404, detail="Rental not found")
        
        if payload.role != RoleEnum.admin.value and rental.buyer_id != payload.user_id:
            raise HTTPException(status_code=403, detail="You do not have permission to update this rental")
        
        rental.status = data.status
        db.session.commit()
        db.session.refresh(rental)
        
        return ServiceRentalUpdateResponse(rental_id=rental.id)
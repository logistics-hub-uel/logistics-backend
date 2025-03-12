from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from app.helpers.exception_handler import CustomException
from app.helpers.login_manager import valid_token_required
from app.helpers.paging import Page, PaginationParams
from app.schemas.base import DataResponse
from app.services.services import ServiceService
from app.schemas.service import (
    ServiceRentalCreateResponse, 
    ServiceRentalCreateRequest, 
    ServiceRentalResponseItem,
    ServiceRentalUpdateRequest,
    ServiceRentalUpdateResponse
)
from app.schemas.sche_token import TokenPayload

router = APIRouter()

@router.post("", dependencies=[Depends(valid_token_required)], response_model=DataResponse[ServiceRentalCreateResponse])
def rent(req:ServiceRentalCreateRequest, service_service: ServiceService = Depends(), payload: TokenPayload = Depends(valid_token_required)):
    """
    API Rent Service
    """
    try:
        return DataResponse().success_response(data=service_service.rent_service(data=req, payload=payload))
    except HTTPException as e:
        raise CustomException(http_code=400, code='400', message=e.detail)
    
@router.get("", dependencies=[Depends(valid_token_required)], response_model=Page[ServiceRentalResponseItem])
def get_rentals(
    params: PaginationParams = Depends(),
    service_service: ServiceService = Depends()
) -> Any:
    """
    API Get list Rentals
    """
    try:
        rentals = service_service.get_all_rentals(params=params)
        return rentals
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

@router.put("/{rental_id}", dependencies=[Depends(valid_token_required)], response_model=DataResponse[ServiceRentalUpdateResponse])
def update_rental(
    rental_id: str,
    req: ServiceRentalUpdateRequest,
    service_service: ServiceService = Depends(),
    payload: TokenPayload = Depends(valid_token_required)
):
    """
    API Update Service Rental
    """
    try:
        return DataResponse().success_response(
            data=service_service.update_rental(rental_id=rental_id, data=req, payload=payload)
        )
    except HTTPException as e:
        raise CustomException(http_code=400, code='400', message=e.detail)

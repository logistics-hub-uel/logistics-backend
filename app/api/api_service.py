from typing import Any, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db

from app.helpers.exception_handler import CustomException
from fastapi import HTTPException
from app.helpers.login_manager import login_required, PermissionRequired, valid_token_required
from app.helpers.paging import Page, PaginationParams, paginate
from app.schemas.base import DataResponse
from app.services.services import ServiceService
from app.schemas.service import *
from app.schemas.sche_token import TokenPayload
from app.models.enums import RoleEnum
# from app.schemas.sche_account import *
from app.models import Account

router = APIRouter()

# ADMIN ONLYS!
# GET LIST OF SERVICES      
@router.get("", dependencies=[Depends(valid_token_required)], response_model=Page[ServiceItemResponse])
def get(
    params: PaginationParams = Depends(),
    name: str = None,
    category: str = None,
    min_price: float = None,
    max_price: float = None,
    supplier_id: str = None,
    service_service: ServiceService = Depends()
) -> Any:
    """
    API Get list Services with filters
    - **name**: Filter by service name (partial match)
    - **category**: Filter by exact category
    - **min_price**: Filter servi(ces with price >= min_price
    - **max_price**: Filter services with price <= max_price
    - **supplier_id**: Filter by supplier ID
    """
    try:
        services = service_service.get_all(
            params=params,
            name=name,
            category=category,
            min_price=min_price,
            max_price=max_price,
            supplier_id=supplier_id
        )
        return services
    except Exception as e:
        return HTTPException(status_code=400, detail=logger.error(e))

# USER CAN DELETE ONLY THEIR OWN SERVICES

# ANY USER CAN CREATE A SERVICE
@router.post("", dependencies=[Depends(valid_token_required)], response_model=DataResponse[ServiceItemResponse])
def create(service_data: ServiceCreateRequest, service_service: ServiceService = Depends(), payload: TokenPayload = Depends(valid_token_required)):
    """
    API Create Service
    """
    try:
        if payload.role != RoleEnum.admin.value:
            service_data.supplier_id = payload.user_id
        new_service = service_service.create_service(service_data)
        return DataResponse().success_response(data=new_service)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))
# USER CAN JUST UPDATE THEIR OWN SERVICES
@router.put("/{service_id}", dependencies=[Depends(valid_token_required)], response_model=DataResponse[ServiceUpdateResponse])
def update(service_id: str, service_data: ServiceUpdateRequest, service_service: ServiceService = Depends(), payload: TokenPayload = Depends(valid_token_required)):
    """
    API Update Service
    """
    try:
        updated_service = service_service.update_service(service_id=service_id, data=service_data, payload=payload)
        return DataResponse().success_response(data=updated_service)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))

# USER READ A SERVICE BY SERVICE_ID
@router.get("/{service_id}", dependencies=[Depends(valid_token_required)], response_model=DataResponse[ServiceItemResponse])
def detail(service_id: str, service_service: ServiceService = Depends()) -> Any:
    """
    API get Detail Service
    """
    try:
        return DataResponse().success_response(data=service_service.get_service_by_id(service_id))
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))

# USER CAN DELETE ONLY THEIR OWN SERVICES
@router.delete("/{service_id}", dependencies=[Depends(valid_token_required)], response_model=DataResponse[ServiceDeleteResponse])
def delete(service_id: str, service_service: ServiceService = Depends(), payload: TokenPayload = Depends(valid_token_required)):
    """
    API Delete Service
    """
    try:
        return DataResponse().success_response(data=service_service.delete_service(service_id=service_id, payload=payload))
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))
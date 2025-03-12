from typing import Any

from fastapi import APIRouter, Depends

from app.helpers.exception_handler import CustomException
from app.schemas.base import DataResponse
from app.services.account import AccountService
from app.schemas.account import AccountCreateRequest, AccountCreateResponse
# from app.schemas.sche_account import AccountCreateRequest, AccountItemResponse
from app.models.enums import RoleEnum
router = APIRouter()

# BUYER REGISTER
@router.post('/buyer', response_model=DataResponse[AccountCreateResponse])    
def register(register_data: AccountCreateRequest, user_service: AccountService = Depends()) -> Any:
    try:
        register_data.role = RoleEnum.buyer
        register_user = user_service.register_user(register_data)
        return DataResponse().success_response(data=AccountCreateResponse(user_id=register_user.id))
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))
# SUPPLIER REGISTER

@router.post('/supplier', response_model=DataResponse[AccountCreateResponse])
def register(register_data: AccountCreateRequest, user_service: AccountService = Depends()) -> Any:
    try:
        register_data.role = RoleEnum.provider
        register_user = user_service.register_user(register_data)
        return DataResponse().success_response(data=AccountCreateResponse(user_id=register_user.id))
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))
    
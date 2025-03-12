from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from fastapi_sqlalchemy import db

from app.core.security import create_access_token
from app.schemas.account import LoginRequest, LoginResponse
from app.schemas.base import DataResponse
# from app.schemas.sche_token import Token
from app.services.account import AccountService
# from app.schemas.sche_account import AccountLoginRequest

router = APIRouter()

# LOGIN
@router.post('', response_model=DataResponse[LoginResponse])
def login_access_token(form_data: LoginRequest, account_service: AccountService = Depends()):
    user = account_service.authenticate(email=form_data.email, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    return DataResponse().success_response(LoginResponse(
        access_token=create_access_token({"user_id":user.id, "role": user.role.value})
    ))    
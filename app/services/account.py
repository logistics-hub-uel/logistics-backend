import jwt

from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi_sqlalchemy import db
from pydantic import ValidationError
from starlette import status

from app.models import Account

from app.core.config import settings
from app.core.security import verify_password, get_password_hash
from app.schemas.sche_token import TokenPayload
# from app.schemas.sche_account import * 
from app.schemas.account import AccountCreateRequest
class AccountService(object): 
    __instance = None

    def __init__(self):
        pass

    reusable_oauth2 = HTTPBearer(
        scheme_name='Authorization'
    )


    @staticmethod
    def authenticate(*, email: str, password: str) -> Optional[Account]:
        """
        Check email and password is correct.
        Return object Account if correct, else return None
        """
        account = db.session.query(Account).filter_by(email=email).first()
        if not account:
            return None
        if not verify_password(password, account.hashed_password):
            return None
        return account
    
    @staticmethod
    def validate_current_token(http_authorization_credentials=Depends(reusable_oauth2)) -> TokenPayload:
        """
        Check token is valid or not
        """
        try:
                # Split token from "Bearer token"
            token = http_authorization_credentials.credentials.split(" ")[1]
            payload = jwt.decode(
                token, settings.SECRET_KEY,
                algorithms=[settings.SECURITY_ALGORITHM]
            )
            token_data = TokenPayload(**payload)
            return token_data
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not validate credentials",
            )
    
    def get_current_account(http_authorization_credentials=Depends(reusable_oauth2)):
        """
        Decode JWT token to get user_id => return User info from DB query
        """
        try:
            # Split token from "Bearer token"
            token = http_authorization_credentials.credentials.split(" ")[1]
            payload = jwt.decode(
                token, settings.SECRET_KEY,
                algorithms=[settings.SECURITY_ALGORITHM]
            )
            token_data = TokenPayload(**payload)
            return token_data
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not validate credentials",
            )

    
    @staticmethod
    def register_user(data: AccountCreateRequest):
        exist_account = db.session.query(Account).filter(Account.email == data.email).first()
        if exist_account:
            raise Exception('Email already exists')
        register_account = Account(
            full_name=data.full_name,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            phone_number=data.phone_number,
            role=data.role,
            tax_number=data.tax_number,
            address=data.address
        )
        db.session.add(register_account)
        db.session.commit()
        db.session.refresh(register_account)
        return register_account

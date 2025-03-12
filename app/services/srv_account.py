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
    def get_current_account(http_authorization_credentials=Depends(reusable_oauth2)) -> AccountItemResponse:
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
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Could not validate credentials",
            )
        account = db.session.query(Account).get(token_data.user_id)
        account = AccountItemResponse(
            id=account.id,
            full_name=account.full_name,
            email=account.email,
            is_active=account.is_active,
            is_email_verified=account.is_email_verified,
            role=account.role,
            year_of_birth=account.year_of_birth,
            phone_number=account.phone_number,
            gender=account.gender,
            residence_city=account.residence_city,
            residence_country=account.residence_country,
            home_town=account.home_town)
        if not account:
            raise HTTPException(status_code=404, detail="User not found")
        return account
    
    # @staticmethod
    # def register_user(data: AccountCreateRequest):
    #     exist_account = db.session.query(Account).filter(Account.email == data.email).first()
    #     if exist_account:
    #         raise Exception('Email already exists')
    #     register_account = Account(
    #         full_name=data.full_name,
    #         email=data.email,
    #         hashed_password=get_password_hash(data.password),
    #         is_active=True,
    #         role="user",
    #         phone_number="9999",
    #         gender="male",
    #         year_of_birth=1990,
    #         home_town="Hanoi",
    #         residence_country="Vietnam",
    #         residence_city="Hanoi"

    #     )
    #     db.session.add(register_account)
    #     db.session.commit()

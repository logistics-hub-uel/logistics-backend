from fastapi import HTTPException, Depends

from app.models import Account
from app.services.account import AccountService


def login_required(http_authorization_credentials=Depends(AccountService().reusable_oauth2)):
    return AccountService().get_current_account(http_authorization_credentials)

def valid_token_required(http_authorization_credentials=Depends(AccountService().reusable_oauth2)):
    t =  AccountService().validate_current_token(http_authorization_credentials)
    print("T: ", t)
    return t
class PermissionRequired:
    def __init__(self, *args):
        self.user = None
        self.permissions = args

    def __call__(self, user: Account = Depends(login_required)):
        self.user = user
        if self.user.role not in self.permissions and self.permissions:
            raise HTTPException(status_code=400,
                                detail=f'Account {self.user.email} can not access this api')

from app.core.security import get_password_hash
from app.core.config import settings
from app.models.enums import RoleEnum
from app.models.models import Account, RoleEnum
from passlib.context import CryptContext
from app.db.base import get_db

def create_admin():
    with next(get_db()) as db:
        admin_email=settings.DEFAULT_ADMIN_EMAIL

        # Check if admin exists
        existing_admin = db.query(Account).filter(Account.email == admin_email).first()
        if not existing_admin:

            admin = Account(
                full_name=settings.DEFAULT_ADMIN_FULL_NAME,
                email=admin_email,
                hashed_password=get_password_hash(settings.DEFAULT_ADMIN_PASSWORD),
                role=RoleEnum.admin,
                phone_number=settings.DEFAULT_ADMIN_PHONE,
            )
            
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("✅ Admin account created!")
        else:
            print("⚠️ Admin account already exists.")

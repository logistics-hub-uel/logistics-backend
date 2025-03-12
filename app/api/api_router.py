from fastapi import APIRouter

from app.api import api_login, api_register, api_healthcheck, api_account, api_image, api_service, api_service_rental

router = APIRouter()

router.include_router(api_healthcheck.router, tags=["health-check"], prefix="/healthcheck")
router.include_router(api_login.router, tags=["login"], prefix="/login")
router.include_router(api_register.router, tags=["register"], prefix="/register")
router.include_router(api_account.router, tags=["account"], prefix="/accounts")
router.include_router(api_image.router, tags=["image"], prefix="/images")
router.include_router(api_service.router, tags=["service"], prefix="/services")
router.include_router(api_service_rental.router, tags=["service-rental"], prefix="/rental")

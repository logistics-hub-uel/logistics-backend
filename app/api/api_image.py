import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.image_schema import ImageResponse, ImageUrl
from app.schemas.base import ResponseSchemaBase, DataResponse
from app.core.config import settings

router = APIRouter()

STATIC_DIR = "static"
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}

if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

@router.post("/upload", response_model=DataResponse[ImageResponse])
async def upload_image(file: UploadFile = File(...)):
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    file_name = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(STATIC_DIR, file_name)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    image_response = ImageResponse(url=f"{settings.BACKEND_HOST}/static/{file_name}")
    print(image_response)
    return DataResponse().success_response(data=image_response)
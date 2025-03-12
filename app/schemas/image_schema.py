from pydantic import BaseModel
from app.schemas.base_schema import BaseSchema

class ImageUrl(BaseModel):
    url: str

class ImageResponse(ImageUrl):
    pass

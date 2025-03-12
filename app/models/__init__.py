# Import all the models, so that Base has them before being
# imported by Alembic
from app.models.model_base import Base  
from app.models.models import *
from app.models.enums import *
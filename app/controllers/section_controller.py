from app.controllers import paths
from app.models import schemas, models
from app.controllers.base_controller import crud

paths['section'] = crud(schemas.Section, schemas.Section, models.Section, 'id')

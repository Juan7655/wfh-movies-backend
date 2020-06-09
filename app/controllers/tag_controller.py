from app.controllers import paths
from app.models import schemas, models
from app.controllers.base_controller import crud

paths['tag'] = crud(schemas.Tag, schemas.Tag, models.Tag, 'name')

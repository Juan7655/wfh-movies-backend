from app.controllers import paths
from app.controllers.base_controller import crud
from app.models import schemas, models

paths['user'] = crud(schemas.User, schemas.User, models.User, 'id')

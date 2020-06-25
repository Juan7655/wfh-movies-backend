from app.controllers import paths
from app.controllers.base_controller import crud
from app.models import schemas, models

paths['user'] = crud(schemas.UserRead, schemas.UserWrite, models.User, 'id')

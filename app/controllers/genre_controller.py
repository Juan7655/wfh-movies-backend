from app.controllers import paths
from app.models import schemas, models
from app.controllers.base_controller import crud

paths['genre'] = crud(schemas.Genre, schemas.Genre, models.Genre, 'id')

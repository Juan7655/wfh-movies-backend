from app.controllers import paths
from app.controllers.base_controller import crud
from app.models import schemas, models

paths['review'] = crud(schemas.ReviewRead, schemas.Review, models.Review, 'movie_user')

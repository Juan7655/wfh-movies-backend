from app.controllers import paths
from app.models import schemas, models
from app.controllers.base_controller import crud

paths['watchlist'] = crud(schemas.Watchlist, schemas.Watchlist, models.Watchlist, 'movie_user')

from fastapi import APIRouter

from app.controllers.base_controller import crud
from app.models import schemas, models
from app.service.commons import Filter

router = APIRouter()


class MovieFilter(Filter):
    operators = {
        **Filter.operators,
        'superset': {
            'description':
                "Currently only working to match Movies Genres. The operation should be read as 'select movies whose "
                "related genres include the given values'. Formally, the semantics are interpreted as 'select movies "
                "whose genre set is a superset of the set of input values'. That is, **Movie.genres >= values**"
                "<br>Value format should be a list of values separated by pipe symbol "
                "(e.g. superset(genre, [drama|romantic|action]))",
            'expression':
                lambda col: lambda vals: tuple(col.any(models.MovieGenre.genre == v) for v in vals[1:-1].split('|'))
        }
    }

    docs = "Filter data. Input format: operation(field, value). Available operations: <br>" \
           + '\n'.join([f'<br>**-{k}**: ' + v.get('description') for k, v in operators.items()])


crud(router, schemas.MovieRead, schemas.Movie, models.Movie, 'id', filter_model=MovieFilter)

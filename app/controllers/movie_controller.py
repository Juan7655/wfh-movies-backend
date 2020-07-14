from typing import List

from app.controllers import paths
from app.controllers.base_controller import crud
from app.models import schemas, models
from app.service.commons import Filter, create_instance, save_instance, query_objects, paginator
from config import log


class MovieFilter(Filter):
    operators = {
        **Filter.operators,
        'superset': {
            'description':
                "superset(field: column[str], values: List[str]) -> `all(substring IN field for substring in values)`",
            'expression':
                lambda col: lambda vals: tuple(col.like(f'%{v}%') for v in vals[1:-1].split('|'))
        }
    }

    docs = "Filter data. Input format: operation(field, value). Available operations: <br>" \
           + '\n'.join([f'<br>**-{k}**: ' + v.get('description') for k, v in operators.items()])


def create(db, instance: models.Movie, model):
    genres = instance.genres.split('|')
    new_genres = [models.Genre(id=g) for g in genres if db.query(models.Genre).filter_by(id=g).first() is None]
    [save_instance(genre, db=db) for genre in new_genres]

    return create_instance(db=db, instance=instance, model=model)


def get_all(db, limit: int = 10, page: int = 1, sort: List[str] = (), filters: List[str] = (), user_id=None):
    if user_id is not None:
        log.info("Searching watchlist for user: {%s} with data type: {%s}", user_id, type(user_id))
        watchlist = [i for i, in db.query(models.Watchlist.movie).filter_by(user=user_id).all()]
        log.info("Retrieved %s elements in user's watchlist", len(watchlist))
    else:
        watchlist = []
    query = query_objects(db=db, query_model=models.Movie, filters=filters, sort=sort, filter_model=MovieFilter)
    result = paginator(query, page_number=page, per_page_limit=limit)
    [setattr(i, 'in_watchlist', i.id in watchlist) for i in result.items]
    return result


paths['movie'] = crud(schemas.MovieRead, schemas.Movie, models.Movie, 'id', get_all=get_all, post=create)

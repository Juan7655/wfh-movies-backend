from app.controllers import paths
from app.controllers.base_controller import crud
from app.models import schemas, models
from app.service.commons import Filter, create_instance, save_instance


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


paths['movie'] = crud(schemas.MovieRead, schemas.Movie, models.Movie, 'id', filter_model=MovieFilter, post=create)

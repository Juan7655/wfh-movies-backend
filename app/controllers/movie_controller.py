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


paths['movie'] = crud(schemas.MovieRead, schemas.Movie, models.Movie, filter_model=MovieFilter, id_field='id')

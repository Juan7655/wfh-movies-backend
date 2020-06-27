from typing import List

from pydantic import HttpUrl

from app.controllers import paths
from app.models import schemas, models
from app.controllers.base_controller import crud
from app.service.commons import query_objects, Filter, paginator


def query_movie(skip: int = 0, **kwargs):
    def apply(db):
        movie: models.Movie = query_objects(db=db, query_model=models.Movie, **kwargs).offset(skip).first()
        return movie.poster_path, movie.title
    return apply


def exact(url: HttpUrl):
    return lambda _: (url, '')


def update_section(db, section: models.Section) -> models.Section:
    section.poster_path, section.description = eval(section.poster_function)(db)
    return section


def read_all(db, limit: int = 10, page: int = 1, sort: List[str] = (), filters: List[str] = ()):
    query = query_objects(db=db, query_model=models.Section, filters=filters, sort=sort)
    page = paginator(query, page_number=page, per_page_limit=limit)
    page.items = [update_section(db, item) for item in page.items]
    return page


def read_one(db, instance: models.Section):
    return update_section(db=db, section=instance)


paths['section'] = crud(schemas.SectionRead, schemas.Section, models.Section, 'id', get_all=read_all, get_one=read_one)

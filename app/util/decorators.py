from typing import List

from fastapi import Depends, HTTPException, Path, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import Base, get_db
from app.util.commons import create_instance, delete_instance, instance_existence, save_instance, \
    PlainOkResponse, paginator
from app.models.schemas import MovieRead, Page


def crud(router, read_model: BaseModel, write_model: BaseModel, query_model: Base, id_field: str):
    @router.get('', response_model=Page[read_model])
    def read_all(limit: int = 10, page: int = 1, db: Session = Depends(get_db)):
        return paginator(db.query(query_model), page_number=page, per_page_limit=limit)

    @router.post('', response_model=read_model)
    def create(movie: write_model, db: Session = Depends(get_db)):
        count = db.query(query_model).filter_by(title=movie.title).count()
        if count != 0:
            raise HTTPException(status_code=400,
                                detail=query_model.__name__ + " already registered")
        return create_instance(db=db, instance=movie, model=query_model)

    @router.get("/{%s}" % id_field, response_model=read_model)
    def read_one(user_data: Base = Depends(instance_existence(query_model, id_field=id_field))):
        return user_data

    @router.put("/{%s}" % id_field, response_model=read_model)
    def update_data(
            movie: write_model,
            db: Session = Depends(get_db),
            user_data: Base = Depends(instance_existence(query_model, id_field=id_field))
    ):
        # TODO make schema fields optional
        for k, v in movie.dict().items():
            getattr(user_data, k)
            setattr(user_data, k, v)
        return save_instance(db, user_data)

    @router.delete("/{%s}" % id_field, responses={200: PlainOkResponse().definition})
    def delete(db: Session = Depends(get_db),
               user_data: Base = Depends(instance_existence(query_model, id_field=id_field))):
        delete_instance(db, instance=user_data)
        return PlainOkResponse().content


def paginated(dump, items_per_page=10):
    def wrapper(fun):
        @wraps(fun)
        def wrapped(*args, page=1, **kwargs):
            try:
                max_per_page = kwargs.pop('items_per_page', items_per_page)
                query = fun(*args, **kwargs) \
                    .paginate(page=int(page), max_per_page=int(max_per_page))
            except NotFound:
                raise PageUnavailable(page)

            return {
                'page': query.page,
                'total_pages': query.pages,
                'total_items': query.total,
                'items_per_page': query.per_page,
                'has_next': query.has_next,
                'has_prev': query.has_prev,
                'items': dump(query.items)
            }

        return wrapped

    return wrapper

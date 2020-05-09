from typing import List

from fastapi import Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import Base, get_db
from app.models.schemas import Page, BaseModel
from app.util.commons import create_instance, delete_instance, instance_existence, save_instance, \
    PlainOkResponse, paginator, Filter


def crud(router, read_model: BaseModel, write_model: BaseModel, query_model: Base, id_field: str):
    @router.get('', response_model=Page[read_model])
    def read_all(limit: int = Query(10, description='Max number of items per page'),
                 page: int = 1,
                 db: Session = Depends(get_db),
                 sort: List[str] = Query([], description="Sorting parameter given in the "
                                                         "format field.[asc|desc]"),
                 filter: List[str] = Query([], description=Filter.docs)):
        query = db.query(query_model)
        for i in filter:
            query = query.filter(Filter(i, query_model).evaluate())
        for i in sort:
            query = query.order_by(text(i.replace('.', ' ')))
        return paginator(query, page_number=page, per_page_limit=limit)

    @router.post('', response_model=read_model)
    def create(data: write_model, db: Session = Depends(get_db)):
        return create_instance(db=db, instance=data, model=query_model)

    @router.get("/{%s}" % id_field, response_model=read_model)
    def read_one(instance: Base = Depends(instance_existence(query_model, id_field=id_field))):
        return instance

    @router.put("/{%s}" % id_field, response_model=read_model)
    def update_data(
            data: write_model,
            db: Session = Depends(get_db),
            instance: Base = Depends(instance_existence(query_model, id_field=id_field))
    ):
        # TODO make schema fields optional
        for k, v in data.dict().items():
            getattr(instance, k)
            setattr(instance, k, v)
        return save_instance(db, instance)

    @router.delete("/{%s}" % id_field, responses={200: PlainOkResponse().definition})
    def delete(db: Session = Depends(get_db),
               instance: Base = Depends(instance_existence(query_model, id_field=id_field))):
        delete_instance(db, instance=instance)
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

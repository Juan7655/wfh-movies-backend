from typing import List, Type

from fastapi import Depends, Query
from sqlalchemy.orm import Session

from app.database import Base, get_db
from app.models.schemas import Page, BaseModel
from app.service.commons import create_instance, delete_instance, instance_existence, \
    PlainOkResponse, paginator, Filter, query_objects, update_instance_data


def crud(router, read_model: Type[BaseModel], write_model: Type[BaseModel], query_model: Base, id_field: str):
    @router.get('', response_model=Page[read_model])
    def read_all(
            db: Session = Depends(get_db),
            limit: int = Query(10, description='Max number of items per page'),
            page: int = 1,
            sort: List[str] = Query([], description="Sorting parameter given in the format field."
                                                    "{asc|desc} (e.g. title.asc)"),
            filters: List[str] = Query([], description=Filter.docs, alias='filter')
    ):
        query = query_objects(db=db, query_model=query_model, filters=filters, sort=sort)
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
        return update_instance_data(db=db, data=data, instance=instance)

    @router.delete("/{%s}" % id_field, responses={200: PlainOkResponse().definition})
    def delete(
            db: Session = Depends(get_db),
            instance: Base = Depends(instance_existence(query_model, id_field=id_field))
    ):
        delete_instance(db=db, instance=instance)
        return PlainOkResponse().content

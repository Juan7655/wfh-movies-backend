from app.database import Base, get_db
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models import models
from fastapi import Depends, HTTPException, Path


class PlainOkResponse(BaseModel):
    content: dict = {'result': 'OK'}
    definition: dict = {"content": {'application/json': {'example': content}}}


def instance_existence(model: Base, id_field: str, should_exist=True):
    def wrapped(ida: int = Path(..., alias=id_field), db: Session = Depends(get_db)) -> Base:
        print(ida)
        db_instance = db.query(model).filter_by(**{id_field: ida}).first()
        if should_exist == (db_instance is None):
            raise HTTPException(
                status_code=404 if should_exist else 400,
                detail=model.__name__ + (" not found" if should_exist else " already exists")
            )
        return db_instance

    return wrapped


def create_instance(db: Session, instance: BaseModel, model: Base):
    db_instance = model(**instance.dict())
    return save_instance(db, db_instance)


def save_instance(db: Session, db_instance):
    db.add(db_instance)
    db.commit()
    db.refresh(db_instance)
    return db_instance


def delete_instance(db: Session, instance: BaseModel):
    db.delete(instance)
    db.commit()


def paginator(query, page_number, per_page_limit):
    count = query.count()
    total_pages = max(1, (count % per_page_limit != 0) + count // per_page_limit)
    has_next = page_number < total_pages
    has_prev = page_number > 1
    if not (0 < page_number <= total_pages):
        raise Exception('page number exceeds limits')
    offset = (page_number - 1) * per_page_limit
    items = query.offset(offset).limit(per_page_limit).all()

    return {
        'page': page_number,
        'total_pages': total_pages,
        'total_items': count,
        'items_per_page': per_page_limit,
        'has_next': has_next,
        'has_prev': has_prev,
        'items': items
    }

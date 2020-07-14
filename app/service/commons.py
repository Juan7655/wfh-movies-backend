import logging
from typing import List, Type, Union

from fastapi import Depends, Path, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import Base, get_db
from app.models import models
from app.models.schemas import Page
from app.util.errors import InvalidParameter, ResourceDoesNotExist, ResourceAlreadyExists
from config import log


class PlainOkResponse(BaseModel):
    content: dict = {'result': 'OK'}
    definition: dict = {"content": {'application/json': {'example': content}}}


class RatingsHistory(BaseModel):
    example: dict = {2001: 4.5}
    definition: dict = {"content": {'application/json': {'example': example}}}


def instance_existence(model: Base, id_field: str):
    def wrapped(id_value: str = Path(..., alias=id_field), db: Session = Depends(get_db)) -> Base:
        if type(id_value) == str:
            filters = {k: v for k, v in zip(id_field.split('_'), id_value.split('_'))}
        else:
            filters = {id_field: id_value}
        db_instance = db.query(model).filter_by(**filters).first()
        if db_instance is None:
            error = ResourceDoesNotExist(model.__name__)
            raise HTTPException(error.status_code, error.content)
        return db_instance

    return wrapped


def create_instance(db: Session, instance: BaseModel, model: Base):
    db_instance = model(**instance.dict())
    return save_instance(db=db, db_instance=db_instance)


def save_instance(db_instance, db: Session):
    try:
        db.add(db_instance)
        db.commit()
        db.refresh(db_instance)
    except IntegrityError as err:
        log.error(err)
        raise ResourceAlreadyExists(type(db_instance).__name__)
    return db_instance


def delete_instance(instance: BaseModel, db: Session):
    db.delete(instance)
    db.commit()


def paginator(query, page_number: int, per_page_limit: int) -> Page:
    count = query.count()
    total_pages = max(1, (count % per_page_limit != 0) + count // per_page_limit)
    has_next = page_number < total_pages
    has_prev = page_number > 1
    if not (0 < page_number <= total_pages):
        raise InvalidParameter('page number exceeds limits')
    offset = (page_number - 1) * per_page_limit
    items = query.offset(offset).limit(per_page_limit).all()

    return Page(
        page=page_number,
        total_pages=total_pages,
        total_items=count,
        items_per_page=per_page_limit,
        has_next=has_next,
        has_prev=has_prev,
        items=items
    )


class Filter:
    operators = {
        'exact': {
            'description': "exact(field: column[str], value: str) -> `field = 'value'`",
            'expression': lambda column: column.__eq__},
        'partial': {
            'description': "partial(field: column[str], value: str) -> `field LIKE '%value%'`",
            'expression': lambda column: lambda value: column.ilike(f'%{value}%')},
        'start': {
            'description': "start(field: column[str], value: str) -> `field LIKE 'value%'`",
            'expression': lambda column: lambda value: column.like(f'{value}%')},
        'end': {
            'description': "end(field: column[str], value: str) -> `field LIKE '%value'`",
            'expression': lambda column: lambda value: column.like(f'%{value}')},
        'word_start': {
            'description': "word_start(field: column[str], value: str) -> `field LIKE '% value%'`",
            'expression': lambda column: lambda value: column.like(f'% {value}%')},
        'anyOf': {
            'description': "anyOf(field: column[Any], values: List[Any]) -> `field IN values`",
            'expression': lambda column: lambda values: column.in_(values[1:-1].split('|'))},
        'lt': {
            'description': "lt(field: column[Comparable], value: Comparable) -> `field < value`",
            'expression': lambda column: lambda value: column < value},
        'le': {
            'description': "le(field: column[Comparable], value: Comparable) -> `field <= value`",
            'expression': lambda column: lambda value: column <= value},
        'gt': {
            'description': "gt(field: column[Comparable], value: Comparable) -> `field > value`",
            'expression': lambda column: lambda value: column > value},
        'ge': {
            'description': "ge(field: column[Comparable], value: Comparable) -> `field >= value`",
            'expression': lambda column: lambda value: column >= value},
        'distinct': {
            'description': "distinct(field: column[Comparable], value: Comparable) -> `field != value`",
            'expression': lambda column: lambda value: column != value},
    }

    docs = "Filter data. Input format: operation(field, value). Available operations: <br>" \
           + '\n'.join([f'<br>**-{k}**: ' + v.get('description') for k, v in operators.items()])

    def __init__(self, expression: str, model: Base):
        operator, expression = tuple(expression.split('(', 1))
        self.model = model
        self.operator = self.operators.get(operator).get('expression')
        self.column, expression = tuple(expression.split(', ', 1))
        self.value = expression[:-1]

    def evaluate(self):
        criteria = self.operator(getattr(self.model, self.column))(self.value)
        return criteria if type(criteria) == tuple else (criteria,)


def query_objects(
        query_model,
        db: Session,
        filters: List[str] = (),
        sort: List[str] = (),
        filter_model: Type[Filter] = Filter
):
    query = db.query(query_model)
    query = apply_filters(query, query_model, filters, filter_model)
    query = apply_sorts(query, sort)
    return query


def apply_filters(query, query_model, filters: List[str] = (), filter_model: Type[Filter] = Filter):
    for i in filters:
        criteria = filter_model(i, query_model).evaluate()
        query = query.filter(*criteria)
    return query


def apply_sorts(query, sort: List[str] = ()):
    for i in sort:
        expression = i.replace('.', ' ')
        split = i.split('.')
        if len(split) != 2 or split[1] not in ['asc', 'desc']:
            raise InvalidParameter('Sorting format must be in the form of <field>.<asc|desc>')

        query = query.order_by(text(expression))
    return query


def update_instance_data(data, instance, db: Session):
    for k, v in data.dict().items():
        getattr(instance, k)
        setattr(instance, k, v)
    return save_instance(db_instance=instance, db=db)


def error_docs(resource_name, *args: Union[Type[Exception], Exception]):
    default = {404: "Unknown error"}
    return {
        k: {"description": v.replace('resource', resource_name)} for error in args
        for k, v in getattr(error, 'docs', default).items()
    }


def get_user_watchlist_ids(db: Session, user_id: int) -> List[int]:
    log.info("Searching watchlist for user: {%s}", user_id)
    watchlist = [] if not user_id else [i for i, in db.query(models.Watchlist.movie).filter_by(user=user_id).all()]
    log.debug("Retrieved %s elements in user's watchlist", len(watchlist))
    return watchlist

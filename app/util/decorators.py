from functools import wraps

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from config import log


def error_handling(fun):
    @wraps(fun)
    def wrapped(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except Exception as err:
            if issubclass(type(err), SQLAlchemyError):
                raise err
            log.error(f"Error caught. Info: {repr(err)}")
            status_code = getattr(err, 'status_code', 404)
            content = getattr(err, 'content', repr(err))
            raise HTTPException(status_code, content)

    return wrapped

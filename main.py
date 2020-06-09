from datetime import datetime as dt

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse
from app.controllers import *
from app.database import get_db
from app.models.models import Request as RequestModel
from app.service.commons import save_instance
from config import log, settings

app = FastAPI(debug=True)
register_paths(app)


@app.exception_handler(SQLAlchemyError)
async def validation_exception_handler(_, exc):
    content = str(getattr(exc, 'orig', repr(exc)))
    log.debug(f"SQLAlchemy found an error: {content}")
    return JSONResponse(
        status_code=400,
        content={"detail": "Database Error", "body": content.split('\n')[0]},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": "Validation Error", "body": str(exc).split('\nbody -> data -> ')[1:]},
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = dt.now().timestamp()
    response = await call_next(request)
    if not settings.audit:
        return response
    end_time = dt.now().timestamp()
    db = next(get_db())
    api_key = request.headers.get('API_KEY')

    instance = RequestModel(
        path=str(request.url).replace('%20', ' ').replace('%28', '(').replace('%7C', '|').replace('%29', ')'),
        verb=request.method,
        start_time=start_time,
        end_time=end_time,
        response_status_code=response.status_code,
        with_token=api_key == settings.api_key
    )
    save_instance(db=db, db_instance=instance)

    response.headers["X-Process-Time"] = str(end_time - start_time)
    return response


# [app.include_router(
#     router,
#     prefix=path,
#     tags=[spacename],
# ) for router, path, spacename in registered_paths]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

from datetime import datetime as dt

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse
from app.controllers import *
from app.database import SessionLocal
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
    db = SessionLocal()
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
    db.close()

    response.headers["X-Process-Time"] = str(end_time - start_time)
    return response


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Unexpected error", status_code=404)
    try:
        request.state.db = SessionLocal()
        log.info("Opened a db session instance")
        response = await call_next(request)
    finally:
        log.info("Closing the db session instance")
        request.state.db.close()
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

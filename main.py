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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

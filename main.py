from datetime import datetime as dt

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

from app.controllers import movie_controller, rating_controller, tag_controller, genre_controller, user_controller, \
    review_controller, watchlist_controller
from app.database import get_db
from app.models.models import Request as RequestModel
from app.service.commons import save_instance
from config import log, settings

app = FastAPI(debug=True)


@app.exception_handler(SQLAlchemyError)
async def validation_exception_handler(request, exc):
    content = str(getattr(exc, 'orig', repr(exc)))
    log.debug(f"SQLAlchemy found an error: {content}")
    return JSONResponse(
        status_code=400,
        content={"detail": "Database Error", "body": content.split('\n')[0]},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
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


app.include_router(
    movie_controller.router,
    prefix="/movie",
    tags=["Movies"],
)

app.include_router(
    rating_controller.router,
    prefix="/rating",
    tags=["Ratings"],
)

app.include_router(
    tag_controller.router,
    prefix="/tag",
    tags=["Tags"],
)

app.include_router(
    genre_controller.router,
    prefix="/genre",
    tags=["Genres"],
)

app.include_router(
    user_controller.router,
    prefix="/user",
    tags=["Users"],
)

app.include_router(
    review_controller.router,
    prefix="/review",
    tags=["Reviews"],
)

app.include_router(
    watchlist_controller.router,
    prefix="/watchlist",
    tags=["Watchlist"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

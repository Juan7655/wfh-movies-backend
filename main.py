import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

from app.controllers import movie_controller, rating_controller, tag_controller, genre_controller
from config import log

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

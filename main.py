import uvicorn
from fastapi import FastAPI

from app.controllers import movie_controller, rating_controller, tag_controller

app = FastAPI()


app.include_router(
    movie_controller.router,
    prefix="/movie",
    tags=["Movies"],
    responses={404: {"description": "Not found"}},
)


app.include_router(
    rating_controller.router,
    prefix="/rating",
    tags=["Rating"],
    responses={404: {"description": "Not found"}},
)


app.include_router(
    tag_controller.router,
    prefix="/tag",
    tags=["Tags"],
    responses={404: {"description": "Not found"}},
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

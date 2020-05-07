from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.models import schemas, models
from app.service import movie_service
from app.database import SessionLocal, engine
from app.controllers import movie_controller
from sqlalchemy.schema import MetaData


app = FastAPI()


app.include_router(
    movie_controller.router,
    prefix="/movie",
    tags=["Movies"],
    responses={404: {"description": "Not found"}},
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

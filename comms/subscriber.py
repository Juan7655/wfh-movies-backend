from google.cloud import pubsub_v1
from database import get_db
from models.dto import Movie, Rating, Base
from models.schemas import Rating as RatingSchema, BaseModel
from json import loads
from sqlalchemy.exc import IntegrityError
from config import settings, log


def run():
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(settings.project_id, settings.subscription_name)

    def callback(message):
        try:
            log.debug("Received message: {}".format(message))
            log.debug(f"data: {message.data}")
            register_rating(loads(message.data))
            message.ack()

        except Exception as err:
            log.error(repr(err))

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=callback
    )
    log.info("Listening for messages on {}..\n".format(subscription_path))

    with subscriber:
        try:
            streaming_pull_future.result()
        except:  # noqa
            streaming_pull_future.cancel()


def register_rating(data):
    db = next(get_db())
    instance: RatingSchema = RatingSchema(**data)
    create_rating(db, instance)
    db.close()


def create_rating(db, instance: RatingSchema):
    movie_instance: Movie = get_movie(movie_id=instance.movie, db=db)
    old_rating_sum = movie_instance.rating * movie_instance.vote_count
    new_rating_sum = old_rating_sum + instance.rating
    movie_instance.rating = new_rating_sum / (movie_instance.vote_count + 1)
    movie_instance.vote_count += 1
    save_instance(movie_instance, db=db)

    return create_rating_instance(db=db, instance=instance)


def get_movie(movie_id, db):
    movie: Movie = db.query(Movie).filter_by(id=movie_id).first()

    if movie is None:
        raise Exception('Movie was not found')

    return movie


def save_instance(db_instance: Base, db):
    try:
        db.add(db_instance)
        db.commit()
        db.refresh(db_instance)
    except IntegrityError as err:
        log.error(repr(err))
        raise Exception(type(db_instance).__name__ + ' already exists')
    return db_instance


def create_rating_instance(db, instance: BaseModel):
    db_instance = Rating(**instance.dict())
    return save_instance(db=db, db_instance=db_instance)


if __name__ == '__main__':
    run()

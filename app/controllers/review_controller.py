from app.controllers import paths
from app.controllers.base_controller import crud
from app.models import schemas, models
from app.service.commons import create_instance, update_instance_data


def create_review(db, instance, model):
    rating_model = db.query(models.Rating).filter_by(user=instance.user).filter_by(movie=instance.movie).first()
    if rating_model is None:
        rating_keys = list(schemas.Rating.schema().get('properties').keys())
        rating = schemas.Rating(**{k: v for k, v in instance.dict().items() if k in rating_keys})
        rating_model = create_instance(db=db, instance=rating, model=models.Rating)
    instance.rating = rating_model
    return create_instance(db=db, instance=instance, model=model)


def update_review(db, data, instance):
    data.fields.pop('rating', None)
    if getattr(data, 'rating', None) is not None:
        delattr(data, 'rating')
    return update_instance_data(db=db, data=data, instance=instance)


paths['review'] = crud(schemas.ReviewRead, schemas.ReviewWrite, models.Review, 'movie_user', post=create_review, put=update_review)

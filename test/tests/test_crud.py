from test.tests.base_crud import CrudBaseTest
from app.models.models import Movie, Rating, Tag
from app.models.schemas import Movie as MovieSchema, MovieRead as MovieReadSchema, Rating as RatingSchema, \
    Tag as TagSchema


class TestMovies(CrudBaseTest):
    def setup(self):
        self.entity = Movie
        self.write_schema = MovieSchema
        self.read_schema = MovieReadSchema
        self.entity_json = {
            'title': 'a Test Title',
            'imdb_id': 1,
        }
        super().setup()


class TestRatings(CrudBaseTest):
    def setup(self):
        self.entity = Rating
        self.write_schema = RatingSchema
        self.read_schema = RatingSchema
        self.entity_json = {
            'user': 1,
            'movie': 1,
            'rating': 3.5,
        }
        super().setup()


class TestTags(CrudBaseTest):
    def setup(self):
        self.entity = Tag
        self.write_schema = TagSchema
        self.read_schema = TagSchema
        self.entity_json = {
            'user': 1,
            'movie': 1,
            'name': 'Tag1',
            'timestamp': 1,
        }
        super().setup()

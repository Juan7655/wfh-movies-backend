from pytest import fixture

from test.tests.base_crud import CrudBaseTest
from app.models.models import Movie, Rating, Tag, Genre
from app.models.schemas import Movie as MovieSchema, MovieRead as MovieReadSchema, Rating as RatingSchema, \
    Tag as TagSchema, Genre as GenreSchema


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

    def test_update_item_successfully(self, web_client, **kwargs):
        super().test_update_item_successfully(web_client, imdb_id=2, **kwargs)

    def test_create_item_already_created_should_return_error(self, web_client):
        pass


class TestRatings(CrudBaseTest):
    @fixture(scope='function', autouse=True)
    def create_movie(self, web_client):
        response = web_client.post('/movie', json={'title': 'a Test Title', 'imdb_id': 1})
        assert response.status_code == 200

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

    def test_update_item_successfully(self, web_client, **kwargs):
        super().test_update_item_successfully(web_client, rating=4.5, **kwargs)

    def test_get_all_with_filters(self, web_client, field_name='timestamp'):
        super().test_get_all_with_filters(web_client, field_name=field_name)

    def test_get_all_with_sorts(self, web_client, field_name='timestamp'):
        super().test_get_all_with_sorts(web_client, field_name=field_name)


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

    def test_get_one_item_successfully(self, web_client, entity_id='Tag1'):
        super().test_get_one_item_successfully(web_client, entity_id)

    def test_delete_item_successfully(self, web_client, entity_id='Tag1'):
        super().test_delete_item_successfully(web_client, entity_id)

    def test_update_item_successfully(self, web_client, entity_id='Tag1', **kwargs):
        super().test_update_item_successfully(web_client, entity_id, timestamp=2, **kwargs)

    def test_get_all_with_filters(self, web_client, field_name='name'):
        super().test_get_all_with_filters(web_client, field_name=field_name)

    def test_get_all_with_sorts(self, web_client, field_name='name'):
        super().test_get_all_with_sorts(web_client, field_name=field_name)


class TestGenres(CrudBaseTest):
    genre = 'new-test-genre'

    def setup(self):
        self.entity = Genre
        self.write_schema = GenreSchema
        self.read_schema = GenreSchema
        self.entity_json = {
            'id': self.genre,
        }
        super().setup()

    def test_get_one_item_successfully(self, web_client, entity_id=genre):
        super().test_get_one_item_successfully(web_client, entity_id)

    def test_delete_item_successfully(self, web_client, entity_id=genre):
        super().test_delete_item_successfully(web_client, entity_id)

    def test_update_item_successfully(self, web_client, entity_id=genre, **kwargs):
        super().test_update_item_successfully(web_client, entity_id, **kwargs)

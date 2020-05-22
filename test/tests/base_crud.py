from pytest import mark
from app.database import Base
from app.service.commons import PlainOkResponse
from test.conftest import engine


class GetAllItemsTest:
    def test_get_all(self, web_client):
        response = web_client.get(self.path)
        assert response.status_code == 200
        assert response.json() == {
            'page': 1,
            'total_pages': 1,
            'total_items': 0,
            'items_per_page': 10,
            'has_next': False,
            'has_prev': False,
            'items': []
        }

    def test_create_item_successfully(self, web_client):
        expected = self.write_schema(**self.entity_json).dict()
        expected['genres'] = []
        expected['id'] = 1

        response = web_client.post(self.path, json=self.entity_json)

        assert response.status_code == 200
        assert response.json() == expected

    def test_get_all_with_pagination_limit_exceeded_should_return_error(self, web_client):
        response = web_client.get(self.path + '?page=1000')
        assert response.status_code == 400
        assert response.json() == {'detail': 'The given parameter is invalid'}

    def test_get_all_with_filters(self, web_client, field_name='id'):
        response = web_client.get(self.path, params=dict(filter=f'exact({field_name}, test)'))
        assert response.status_code == 200
        assert response.json() == {
            'page': 1,
            'total_pages': 1,
            'total_items': 0,
            'items_per_page': 10,
            'has_next': False,
            'has_prev': False,
            'items': []
        }

    def test_get_all_with_sorts(self, web_client, field_name='id'):
        response = web_client.get(self.path, params=dict(sort=f'{field_name}.asc'))
        assert response.status_code == 200
        assert response.json() == {
            'page': 1,
            'total_pages': 1,
            'total_items': 0,
            'items_per_page': 10,
            'has_next': False,
            'has_prev': False,
            'items': []
        }

    def test_get_all_with_invalid_sorts_should_return_error(self, web_client, field_name='id'):
        response = web_client.get(self.path, params=dict(sort=f'{field_name}.abc'))
        assert response.status_code == 400
        assert response.json() == {'detail': 'The given parameter is invalid'}

    def test_get_all_with_invalid_sort_field_should_return_error(self, web_client):
        response = web_client.get(self.path, params=dict(sort=f'abc.asc'))
        assert response.status_code == 400
        assert response.json() == {'detail': 'Database Error', 'body': 'no such column: abc'}


class CreateItemTest:
    def test_create_item_successfully(self, web_client):
        """Pre-Condition: No Items should be registered in system"""
        response = web_client.get(self.path)
        assert response.status_code == 200
        assert response.json().get('total_items') == 0

        """Condition: When requesting to create item, should return successful response"""
        expected = self.write_schema(**self.entity_json).dict()

        response = web_client.post(self.path, json=self.entity_json)
        response_data = response.json()

        assert response.status_code == 200
        assert all(response_data.get(k) == v for k, v in expected.items())

        """Post-Condition: The created Item should be registered in the system"""
        response = web_client.get(self.path)
        assert response.status_code == 200
        assert response.json().get('total_items') == 1

    def test_create_item_already_created_should_return_error(self, web_client):
        """Pre-Condition: One Item should be registered in system"""
        response = web_client.post(self.path, json=self.entity_json)
        assert response.status_code == 200

        """Condition: When requesting to create item, should return error"""
        response = web_client.post(self.path, json=self.entity_json)

        assert response.status_code == 409
        assert response.json() == {"detail": f"The given {self.entity_name} already exists"}


class GetOneItemTest:
    def test_get_one_item_successfully(self, web_client, entity_id=1):
        """Pre-Condition: One item should be registered in the system"""
        response = web_client.post(self.path, json=self.entity_json)
        assert response.status_code == 200

        """Condition: When requesting the item, should return successful response"""
        response = web_client.get(f'{self.path}/{entity_id}')
        json = response.json()
        assert response.status_code == 200
        assert all(json.get(k) == v for k, v in self.write_schema(**self.entity_json).dict().items())

    @mark.parametrize("entity_id", list(range(5)))
    def test_get_nonexistent_item_return_not_found(self, web_client, entity_id):
        response = web_client.get(f'{self.path}/{entity_id}')
        assert response.status_code == 404
        assert response.json() == {'detail': f'The given {self.entity_name} was not found'}


class UpdateItemTest:
    def test_update_item_successfully(self, web_client, entity_id=1, **kwargs):
        response = web_client.post(self.path, json=self.entity_json)
        data_post = response.json()
        assert response.status_code == 200

        response = web_client.put(f'{self.path}/{entity_id}', json={**self.entity_json, **kwargs})
        assert response.status_code == 200
        assert response.json() == {**data_post, **kwargs}


class DeleteItemTest:
    def test_delete_item_successfully(self, web_client, entity_id=1):
        """Pre-condition: One item should be created"""
        response = web_client.post(self.path, json=self.entity_json)
        assert response.status_code == 200

        response = web_client.get(self.path)
        assert response.status_code == 200
        assert response.json().get('total_items') == 1

        """Condition: When requesting to delete item, should return successful response"""
        response = web_client.delete(f'{self.path}/{entity_id}')
        response_data = response.json()

        assert response.status_code == 200
        assert response_data == PlainOkResponse().content

        """Post-Condition: The created Item should be registered in the system"""
        response = web_client.get(self.path)
        assert response.status_code == 200
        assert response.json().get('total_items') == 0


class CrudBaseTest(UpdateItemTest, GetOneItemTest, DeleteItemTest, CreateItemTest, GetAllItemsTest):
    def setup(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.entity_name = self.entity.__name__
        self.path = '/' + self.entity_name.lower()

    def teardown(self):
        Base.metadata.drop_all(bind=engine)

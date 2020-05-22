from pytest import mark


class CrudBaseTest:
    def setup(self):
        self.entity_name = self.entity.__name__
        self.path = '/' + self.entity_name.lower()

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

    @mark.parametrize("entity_id", list(range(5)))
    def test_get_nonexistent_item_return_not_found(self, web_client, entity_id):
        response = web_client.get(f'{self.path}/{entity_id}')
        assert response.status_code == 404
        assert response.json() == {'detail': f'The given {self.entity_name} was not found'}

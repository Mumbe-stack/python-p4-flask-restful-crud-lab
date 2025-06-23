import json
from app import app
from models import db, Plant

class TestPlant:
    '''Flask application in app.py'''

    def setup_method(self):
        '''Reset the database and create a test plant'''
        with app.app_context():
            db.session.query(Plant).delete()
            db.session.commit()

        # Add plant via client POST to ensure shared context
        client = app.test_client()
        response = client.post('/plants', json={
            "name": "Test Plant",
            "image": "test.jpg",
            "price": 9.99
        })
        self.plant_id = json.loads(response.data.decode())['id']
        self.client = client  # Store test client for reuse

    def test_plant_by_id_get_route(self):
        response = self.client.get(f'/plants/{self.plant_id}')
        assert response.status_code == 200

    def test_plant_by_id_get_route_returns_one_plant(self):
        response = self.client.get(f'/plants/{self.plant_id}')
        data = json.loads(response.data.decode())

        assert type(data) == dict
        assert data["id"]
        assert data["name"]

    def test_plant_by_id_patch_route_updates_is_in_stock(self):
        response = self.client.patch(
            f'/plants/{self.plant_id}',
            json={"is_in_stock": False}
        )
        data = json.loads(response.data.decode())

        assert type(data) == dict
        assert data["id"]
        assert data["is_in_stock"] == False

    def test_plant_by_id_delete_route_deletes_plant(self):
        response = self.client.delete(f'/plants/{self.plant_id}')
        assert response.status_code == 204
        assert not response.data

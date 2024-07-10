from types import MappingProxyType
from unittest import TestCase

from app import create_app
from models import Cupcake, connect_db, db

# ==================================================

app = create_app("cupcakes_test", testing=True)
connect_db(app)

app.app_context().push()

db.drop_all()
db.create_all()

# --------------------------------------------------

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_list_cupcakes_filter_flavor(self):
        """Tests retrieving a list of cupcakes that contains a specified flavor name."""

        # Arrange
        query_term = "testflavor99"

        CUPCAKE_DATA_99 = MappingProxyType({
            "flavor": "TestFlavor99",
            "size": "TestSize99",
            "rating": 9,
            "image": "http://test.com/cupcake99.jpg"
        })

        cupcake99 = Cupcake(**CUPCAKE_DATA_99)
        db.session.add(cupcake99)
        db.session.commit()

        # Act
        with app.test_client() as client:
            resp = client.get(f"/api/cupcakes?flavor={query_term}")

        # Assert
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, {
                "cupcakes": [{"id": cupcake99.id} | CUPCAKE_DATA_99]
            })

    def test_list_no_cupcakes(self):
        """Tests returning an empty list when there are no cupcakes."""

        # Arrange
        db.session.query(Cupcake).delete()

        # Act
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

        # Assert
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, {"cupcakes": []})

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_get_nonexistent_cupcake(self):
        """Tests returning a 404 HTTP status code when a cupcake does not exist."""

        # Arrange
        cupcake_id = 99

        # Act
        with app.test_client() as client:
            url = f"/api/cupcakes/{cupcake_id}"
            resp = client.get(url)

        # Assert
            self.assertEqual(resp.status_code, 404)

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        """Tests updating a cupcake."""

        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.patch(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

    def test_update_nonexistent_cupcake(self):
        """Tests updating a cupcake that does not exist."""

        with app.test_client() as client:
            url = "/api/cupcakes/99"
            resp = client.patch(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 404)

    def test_delete_cupcake(self):
        """Tests deleting a cupcake."""

        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, {"message": "Deleted"})

    def test_delete_nonexistent_cupcake(self):
        """Tests deleting a cupcake that does not exist."""

        with app.test_client() as client:
            url = "/api/cupcakes/99"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 404)

from fastapi.testclient import TestClient
import unittest
from fastapi import FastAPI
from main import MyMath


class TestHandles(unittest.TestCase):

    def setUp(self):
        app = FastAPI()
        app.include_router(MyMath().myRouter)
        self.client = TestClient(app)

    def test_params_and_add(self):
        client = self.client
        response = client.get('/params')
        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json())

        response = client.post('/add_val_1')
        self.assertEqual(200, response.status_code)
        self.assertIsNone(response.json())

        response = client.get('/params')
        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.json())

        response = client.post('/add_par_a')
        self.assertEqual(200, response.status_code)
        self.assertIsNone(response.json())

        response = client.post('/add_par_b')
        self.assertEqual(200, response.status_code)
        self.assertIsNone(response.json())

        response = client.get('/params')
        self.assertEqual(200, response.status_code)
        self.assertEqual(['a', 'b'], response.json())

    def test_evaluate(self):
        client = self.client
        client.post('/add_val_1')
        client.post('/add_val_2')
        client.post('/add_val_3')

        client.post('/add_par_a')
        client.post('/add_par_b')
        client.post('/add_par_c')

        response = client.post('/eval', json={"a": 1, "b": 2, "c": 3})
        self.assertEqual(200, response.status_code)
        self.assertEqual(12, response.json())


if __name__ == '__main__':
    unittest.main()

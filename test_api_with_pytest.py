import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import MyMath


@pytest.fixture(scope="function")
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(MyMath().myRouter)
    yield app


@pytest.fixture(scope="function")
def client(app) -> TestClient:
    with TestClient(app) as client:
        yield client


def test_params_and_add(client):
    response = client.get('/params')
    assert 200 == response.status_code
    assert [] == response.json()

    response = client.post('/add_val_1')
    assert 200 == response.status_code
    assert response.json() is None

    response = client.get('/params')
    assert 200 == response.status_code
    assert [] == response.json()

    response = client.post('/add_par_a')
    assert 200 == response.status_code
    assert response.json() is None

    response = client.post('/add_par_b')
    assert 200 == response.status_code
    assert response.json() is None

    response = client.get('/params')
    assert 200 == response.status_code
    assert ['a', 'b'] == response.json()


def test_eval(client):
    client.post('/add_val_1')
    client.post('/add_val_2')
    client.post('/add_val_3')

    client.post('/add_par_a')
    client.post('/add_par_b')
    client.post('/add_par_c')

    response = client.post('/eval', json={"a": 1, "b": 2, "c": 3})
    assert 200 == response.status_code
    assert 12 == response.json()

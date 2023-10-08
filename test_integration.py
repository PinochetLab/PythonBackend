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


def test_big(client):
    assert [] == client.get('/params').json()
    assert client.post('/add_val_1').json() is None
    assert [] == client.get('/params').json()
    assert 1 == client.post('/eval', json={}).json()
    assert 404 == client.post('/add_var_a').status_code
    assert client.post('/add_par_a').json() is None
    assert ['a'] == client.get('/params').json()
    assert 2 == client.post('/eval', json={'a': 1}).json()

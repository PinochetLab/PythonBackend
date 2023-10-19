import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import Service


@pytest.fixture(scope="function")
def app() -> FastAPI:
    app = FastAPI()
    for router in Service().routers:
        app.include_router(router)
    yield app


@pytest.fixture(scope="function")
def client(app) -> TestClient:
    with TestClient(app) as client:
        yield client


def test_status(client):
    response = client.get('/authorization')
    assert 200 == response.status_code
    assert {"status": "not authorized", "name": "not authorized"} == response.json()


def test_register(client):
    response = client.post("/authorization/register", json={'name': 'userA', 'password': 'passwordA'})
    assert 200 == response.status_code
    response = client.get('/authorization')
    assert 200 == response.status_code
    assert {"status": "authorized", "name": "userA"} == response.json()


def test_login(client):
    response = client.post("/authorization/login", json={'name': 'userA', 'password': 'passwordA'})
    assert 401 == response.status_code
    response = client.post("/authorization/register", json={'name': 'userA', 'password': 'passwordA'})
    assert 200 == response.status_code
    response = client.get('/authorization')
    assert 200 == response.status_code
    assert {"status": "authorized", "name": "userA"} == response.json()


def test_logout(client):
    response = client.post("/authorization/register", json={'name': 'userA', 'password': 'passwordA'})
    assert 200 == response.status_code
    response = client.post("authorization/logout")
    assert 200 == response.status_code
    response = client.get('/authorization')
    assert 200 == response.status_code
    assert {"status": "not authorized", "name": "not authorized"} == response.json()


def test_delete_account(client):
    response = client.post("/authorization/register", json={'name': 'userA', 'password': 'passwordA'})
    assert 200 == response.status_code
    response = client.post("authorization/delete_account")
    assert 200 == response.status_code
    response = client.get('/authorization')
    assert 200 == response.status_code
    assert {"status": "not authorized", "name": "not authorized"} == response.json()
    response = client.post("/authorization/login", json={'name': 'userA', 'password': 'passwordA'})
    assert 401 == response.status_code


def test_chat(client):
    response = client.get("/chat/sent")
    assert 401 == response.status_code
    response = client.post("/authorization/register", json={'name': 'userA', 'password': 'passwordA'})
    assert 200 == response.status_code
    response = client.post("authorization/logout")
    assert 200 == response.status_code
    response = client.post("/authorization/register", json={'name': 'userB', 'password': 'passwordB'})
    assert 200 == response.status_code
    response = client.post("/chat/send", json={'receiverName': 'userB', 'text': 'Hi'})
    assert 401 == response.status_code
    response = client.post("/chat/send", json={'receiverName': 'userA', 'text': 'Hi'})
    assert 200 == response.status_code
    response = client.get("/chat/sent")
    assert 200 == response.status_code
    assert [{'sender': 'userB', 'receiver': 'userA', 'text': 'Hi'}] == response.json()
    response = client.get("/chat/received")
    assert 200 == response.status_code
    assert [] == response.json()
